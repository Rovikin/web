#!/usr/bin/env python3
"""
sim.py - Simulasi strategi "flip signal" pembelian BTC/USDT (Spot Binance, multi-timeframe)

Logika:
- BUY  : candle HIJAU (close > open) pertama setelah candle MERAH -> eksekusi di CLOSE candle hijau.
- SELL : candle MERAH pertama setelah candle HIJAU (posisi terbuka) -> eksekusi di CLOSE candle merah.
- Fund bersifat compounding: hasil SELL (setelah fee) menjadi modal BUY berikutnya.
- Fee 0.15% dikenakan pada setiap sisi transaksi (BUY dan SELL).

Timeframe:
- daily (d)   -> data disimpan di btcusdt_daily.csv
- weekly (w)  -> data disimpan di btcusdt_weekly.csv
- monthly (m) -> data disimpan di btcusdt_monthly.csv (default)

Data:
- Data kline diunduh dari Binance public REST API (/api/v3/klines) tanpa API key.
- Data disimpan lokal per timeframe di file CSV terpisah. Jika file sudah ada, script hanya
  mengunduh data baru (incremental update) berdasarkan candle terakhir yang tersimpan.

Penggunaan:
    python sim.py --fund 100
    python sim.py -f 100 -tf w -s 2021
    python sim.py --timeframe d --fund 500 --start 2023
"""

import argparse
import csv
import os
import sys
import time
from datetime import datetime, timezone

import requests

BINANCE_KLINES_URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
FEE_RATE = 0.0015  # 0.15%
LIMIT = 1000  # max klines per request (Binance limit)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

TIMEFRAME_CONFIG = {
    "d": {"interval": "1d", "file": os.path.join(SCRIPT_DIR, "btcusdt_daily.csv"), "label": "Daily"},
    "w": {"interval": "1w", "file": os.path.join(SCRIPT_DIR, "btcusdt_weekly.csv"), "label": "Weekly"},
    "m": {"interval": "1M", "file": os.path.join(SCRIPT_DIR, "btcusdt_monthly.csv"), "label": "Monthly"},
}


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def fetch_klines(interval, start_time_ms=None):
    """Fetch klines from Binance public API, paginated, starting from start_time_ms (inclusive).

    PENTING: jika start_time_ms None (unduhan awal), kita eksplisit set startTime=0 (epoch).
    Pagination berlanjut selama batch tidak kosong DAN open_time candle terakhir dalam batch
    masih lebih kecil dari waktu sekarang. Ini menghindari loop berhenti prematur hanya karena
    satu batch kebetulan mengembalikan kurang dari LIMIT (misal karena pembatasan lain di sisi
    Binance untuk kombinasi startTime/limit tertentu).
    """
    all_klines = []
    effective_start = start_time_ms if start_time_ms is not None else 0
    now_ms = int(time.time() * 1000)
    params = {
        "symbol": SYMBOL,
        "interval": interval,
        "limit": LIMIT,
        "startTime": effective_start,
    }

    while True:
        try:
            resp = requests.get(BINANCE_KLINES_URL, params=params, timeout=15)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            log(f"ERROR saat mengambil data dari Binance: {e}")
            sys.exit(1)

        batch = resp.json()
        if isinstance(batch, dict) and "code" in batch:
            log(f"ERROR dari Binance API: {batch}")
            sys.exit(1)

        if not batch:
            break

        all_klines.extend(batch)
        last_open_time = batch[-1][0]
        log(f"  ... diterima {len(batch)} candle (batch), terakhir: "
            f"{datetime.fromtimestamp(last_open_time/1000, tz=timezone.utc).strftime('%Y-%m-%d')}, "
            f"total sejauh ini: {len(all_klines)}")

        if last_open_time <= effective_start and len(batch) <= 1:
            # Pengaman: startTime tidak maju sama sekali, hentikan agar tidak infinite loop.
            break

        # Berhenti hanya jika candle terakhir dalam batch sudah mencapai/melewati waktu sekarang.
        # Ini menjamin loop tidak berhenti prematur akibat batch parsial di tengah histori.
        if last_open_time >= now_ms:
            break

        params["startTime"] = last_open_time + 1
        effective_start = params["startTime"]
        time.sleep(0.2)  # jaga rate limit

    return all_klines


def load_local_data(data_file):
    """Load candle data tersimpan lokal. Return list of dict, sorted by open_time."""
    if not os.path.exists(data_file):
        return []

    rows = []
    with open(data_file, "r", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "open_time": int(r["open_time"]),
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"]),
                "close_time": int(r["close_time"]),
                "is_closed": r["is_closed"] == "True",
            })
    rows.sort(key=lambda x: x["open_time"])
    return rows


def save_local_data(data_file, rows):
    rows.sort(key=lambda x: x["open_time"])
    with open(data_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["open_time", "open", "high", "low", "close", "close_time", "is_closed"])
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def klines_to_rows(klines):
    """Convert raw Binance kline arrays to dict rows. Menandai candle yang sudah closed (close_time < now)."""
    now_ms = int(time.time() * 1000)
    rows = []
    for k in klines:
        open_time, open_p, high_p, low_p, close_p, volume, close_time = k[0], k[1], k[2], k[3], k[4], k[5], k[6]
        is_closed = close_time < now_ms
        rows.append({
            "open_time": int(open_time),
            "open": float(open_p),
            "high": float(high_p),
            "low": float(low_p),
            "close": float(close_p),
            "close_time": int(close_time),
            "is_closed": is_closed,
        })
    return rows


def update_local_data(tf_key):
    """Update data lokal untuk timeframe tertentu: download penuh jika belum ada, atau incremental jika sudah ada."""
    config = TIMEFRAME_CONFIG[tf_key]
    interval = config["interval"]
    data_file = config["file"]
    label = config["label"]

    existing = load_local_data(data_file)

    if not existing:
        log(f"Data lokal {label} belum ada. Mengunduh seluruh histori BTCUSDT ({label}) dari Binance...")
        klines = fetch_klines(interval, start_time_ms=None)
        rows = klines_to_rows(klines)
        # Hanya simpan candle yang sudah closed (candle berjalan/belum closed diabaikan agar konsisten)
        rows = [r for r in rows if r["is_closed"]]
        save_local_data(data_file, rows)
        log(f"Selesai. Total {len(rows)} candle {label.lower()} tersimpan di {data_file}")
        return rows

    # Cari apakah candle terakhir yang tersimpan sudah pasti closed; jika belum, re-fetch dari situ juga.
    last_stored = existing[-1]
    start_ms = last_stored["open_time"]

    log(f"Data lokal {label} ditemukan ({len(existing)} candle). Mengecek data baru sejak "
        f"{datetime.fromtimestamp(start_ms/1000, tz=timezone.utc).strftime('%Y-%m-%d')}...")
    klines = fetch_klines(interval, start_time_ms=start_ms)
    new_rows = klines_to_rows(klines)
    new_rows = [r for r in new_rows if r["is_closed"]]

    # Merge: replace existing[-1] jika ada di new_rows, tambahkan sisanya
    existing_map = {r["open_time"]: r for r in existing[:-1]}  # exclude last, akan di-refresh
    for r in new_rows:
        existing_map[r["open_time"]] = r

    merged = list(existing_map.values())
    merged.sort(key=lambda x: x["open_time"])

    added = len(merged) - (len(existing) - 1)
    if added > 0:
        log(f"Ditemukan {added} candle baru/terupdate. Menyimpan...")
    else:
        log("Tidak ada candle baru. Data lokal sudah up to date.")

    save_local_data(data_file, merged)
    return merged


def date_label(open_time_ms, tf_key):
    fmt = "%Y-%m-%d" if tf_key == "d" else "%Y-%m-%d" if tf_key == "w" else "%Y-%m"
    return datetime.fromtimestamp(open_time_ms / 1000, tz=timezone.utc).strftime(fmt)


def filter_from_year(candles, start_year):
    """
    Potong daftar candle mulai dari 1 Januari start_year.

    Catatan: candle sebelum start_year TIDAK dipakai untuk deteksi sinyal sama sekali (termasuk
    tidak dipakai sebagai referensi warna 'prev_color'). Ini berarti jika candle pertama di rentang
    hasil filter berwarna hijau, ia TIDAK otomatis dianggap sinyal BUY kecuali candle sebelumnya
    (yang juga ada dalam rentang) berwarna merah. Pendekatan ini disengaja agar simulasi --start
    benar-benar independen dari data di luar rentang yang diminta.
    """
    start_dt = datetime(start_year, 1, 1, tzinfo=timezone.utc)
    start_ms = int(start_dt.timestamp() * 1000)
    filtered = [c for c in candles if c["open_time"] >= start_ms]
    return filtered


def run_simulation(candles, initial_fund, tf_key):
    """
    Jalankan simulasi flip signal.
    - BUY di close candle hijau pertama setelah candle merah (tanpa posisi terbuka).
    - SELL di close candle merah pertama setelah candle hijau (dengan posisi terbuka).
    """
    fund = initial_fund
    position = None  # dict: {btc_qty, buy_price, buy_label, fund_used}
    trades = []

    prev_color = None  # 'green' / 'red'

    for c in candles:
        color = "green" if c["close"] > c["open"] else ("red" if c["close"] < c["open"] else "flat")
        label = date_label(c["open_time"], tf_key)

        if color == "flat":
            # candle doji (close == open): tidak memicu sinyal, tapi tetap update prev_color di akhir loop jika perlu.
            continue

        if position is None:
            # Cari sinyal BUY: hijau setelah merah
            if color == "green" and prev_color == "red":
                buy_price = c["close"]
                fee = fund * FEE_RATE
                net_fund = fund - fee
                btc_qty = net_fund / buy_price
                position = {
                    "btc_qty": btc_qty,
                    "buy_price": buy_price,
                    "buy_label": label,
                    "fund_used": fund,
                    "fee_buy": fee,
                }
        else:
            # Ada posisi terbuka, cari sinyal SELL: merah setelah hijau
            if color == "red" and prev_color == "green":
                sell_price = c["close"]
                gross_proceeds = position["btc_qty"] * sell_price
                fee_sell = gross_proceeds * FEE_RATE
                net_proceeds = gross_proceeds - fee_sell
                pnl = net_proceeds - position["fund_used"]
                pnl_pct = (pnl / position["fund_used"]) * 100

                trades.append({
                    "buy_label": position["buy_label"],
                    "sell_label": label,
                    "buy_price": position["buy_price"],
                    "sell_price": sell_price,
                    "fund_in": position["fund_used"],
                    "fee_buy": position["fee_buy"],
                    "fee_sell": fee_sell,
                    "fund_out": net_proceeds,
                    "pnl": pnl,
                    "pnl_pct": pnl_pct,
                })

                fund = net_proceeds  # compounding
                position = None

        prev_color = color

    return trades, fund, position


def print_report(trades, final_fund, initial_fund, open_position, candles, tf_key, start_year=None):
    tf_label = TIMEFRAME_CONFIG[tf_key]["label"]
    date_col_width = 12 if tf_key in ("d", "w") else 9

    print("\n" + "=" * 78)
    title = f"HASIL SIMULASI FLIP SIGNAL - BTCUSDT {tf_label.upper()}"
    print(f"{title:^78}")
    if candles:
        range_label = f"Rentang data simulasi: {date_label(candles[0]['open_time'], tf_key)} s/d {date_label(candles[-1]['open_time'], tf_key)}"
        if start_year is not None:
            range_label += f"  (--start {start_year})"
        print(f"{range_label:^78}")
    print("=" * 78)

    if not trades:
        print("Tidak ada transaksi yang tereksekusi pada rentang data yang tersedia.")
    else:
        header = (f"{'#':<4}{'Buy':<{date_col_width}}{'Sell':<{date_col_width}}{'Buy Price':>14}"
                  f"{'Sell Price':>14}{'Fund In':>12}{'Fund Out':>12}{'PnL':>12}{'PnL%':>9}")
        print(header)
        print("-" * len(header))
        for i, t in enumerate(trades, 1):
            print(
                f"{i:<4}{t['buy_label']:<{date_col_width}}{t['sell_label']:<{date_col_width}}"
                f"{t['buy_price']:>14,.2f}{t['sell_price']:>14,.2f}"
                f"{t['fund_in']:>12,.2f}{t['fund_out']:>12,.2f}"
                f"{t['pnl']:>12,.2f}{t['pnl_pct']:>8.2f}%"
            )
        print("-" * len(header))

    win_trades = [t for t in trades if t["pnl"] > 0]
    lose_trades = [t for t in trades if t["pnl"] <= 0]
    total_fee = sum(t["fee_buy"] + t["fee_sell"] for t in trades)

    print(f"\nTotal transaksi selesai   : {len(trades)}")
    if trades:
        print(f"Menang / Kalah            : {len(win_trades)} / {len(lose_trades)}")
        print(f"Win rate                  : {len(win_trades)/len(trades)*100:.2f}%")
        print(f"Total fee terbayar        : {total_fee:,.4f} USDT")

    if open_position is not None:
        last_close = candles[-1]["close"]
        unrealized_value = open_position["btc_qty"] * last_close
        unrealized_fee = unrealized_value * FEE_RATE
        unrealized_net = unrealized_value - unrealized_fee
        unrealized_pnl = unrealized_net - open_position["fund_used"]
        print(f"\nPosisi masih TERBUKA sejak {open_position['buy_label']}:")
        print(f"  BTC qty            : {open_position['btc_qty']:.8f} BTC")
        print(f"  Buy price          : {open_position['buy_price']:,.2f} USDT")
        print(f"  Mark price (close terakhir) : {last_close:,.2f} USDT")
        print(f"  Unrealized PnL (jika ditutup sekarang, net fee) : {unrealized_pnl:,.2f} USDT")
        print(f"\nFund awal              : {initial_fund:,.2f} USDT")
        print(f"Fund kas saat ini (belum termasuk posisi terbuka) : {final_fund:,.2f} USDT")
    else:
        total_return = final_fund - initial_fund
        total_return_pct = (total_return / initial_fund) * 100
        print(f"\nFund awal              : {initial_fund:,.2f} USDT")
        print(f"Fund akhir (compounding): {final_fund:,.2f} USDT")
        print(f"Total return            : {total_return:,.2f} USDT ({total_return_pct:.2f}%)")

    print("=" * 78 + "\n")


def main():
    parser = argparse.ArgumentParser(description="Simulasi flip signal BTC/USDT Spot Binance (multi-timeframe)")
    parser.add_argument("-f", "--fund", type=float, default=100.0, help="Fund awal dalam USDT (default: 100)")
    parser.add_argument("-tf", "--timeframe", type=str, default="m", choices=["d", "w", "m"],
                         help="Timeframe: d (daily), w (weekly), m (monthly). Default: m")
    parser.add_argument("-s", "--start", type=int, default=None,
                         help="Tahun mulai simulasi, dihitung sejak 1 Januari tahun tersebut (contoh: 2021). "
                              "Default: pakai data paling awal yang tersedia.")
    args = parser.parse_args()

    if args.fund <= 0:
        log("ERROR: --fund harus lebih besar dari 0.")
        sys.exit(1)

    tf_key = args.timeframe.lower()

    current_year = datetime.now(tz=timezone.utc).year
    if args.start is not None and (args.start < 2017 or args.start > current_year):
        log(f"ERROR: --start harus berada dalam rentang 2017 sampai {current_year}.")
        sys.exit(1)

    candles = update_local_data(tf_key)

    if args.start is not None:
        candles = filter_from_year(candles, args.start)
        if len(candles) < 2:
            log(f"ERROR: Data candle tidak cukup untuk simulasi mulai tahun {args.start} "
                f"(hanya {len(candles)} candle tersedia sejak tanggal tersebut).")
            sys.exit(1)

    if len(candles) < 2:
        log("Data candle tidak cukup untuk simulasi (minimal 2 candle closed).")
        sys.exit(1)

    tf_label = TIMEFRAME_CONFIG[tf_key]["label"]
    log(f"Menjalankan simulasi [{tf_label}] dengan fund awal {args.fund:,.2f} USDT, fee {FEE_RATE*100:.2f}% per sisi"
        + (f", mulai dari {args.start}-01..." if args.start else "..."))
    trades, final_fund, open_position = run_simulation(candles, args.fund, tf_key)
    print_report(trades, final_fund, args.fund, open_position, candles, tf_key, start_year=args.start)


if __name__ == "__main__":
    main()

