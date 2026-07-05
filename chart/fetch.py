#!/usr/bin/env python3
"""
fetch_sync.py -- Unduh & sinkronisasi data historis OHLCV dari Binance SPOT API.

CATATAN: versi ini memakai endpoint SPOT (api.binance.com), BUKAN Futures.
Dipakai untuk riset teknikal murni (misal pengujian EMA crossover) yang tidak
terikat pada instrumen Futures tertentu -- Spot punya histori jauh lebih panjang
untuk banyak aset (BTC Spot listing 2017, sementara BTC Futures baru 2019) dan
tidak mengandung distorsi funding rate/leverage yang ada di kontrak Futures.

Menggabungkan:
- Fleksibilitas fetch_klines.py: flag --pair / --timeframe untuk aset & interval apapun.
- Pola incremental sync sim.py: jika file lokal sudah ada, hanya mengunduh candle BARU
  sejak candle terakhir tersimpan (seperti sync blockchain) -- bukan unduh ulang dari nol.

TANPA library eksternal (hanya urllib bawaan Python) -- kompatibel Termux standar.

Penggunaan:
    python3 fetch_sync.py --pair BTCUSDT --timeframe 1d
    python3 fetch_sync.py -p ETHUSDT -tf 4h
    python3 fetch_sync.py -p SOLUSDT -tf 1h
    python3 fetch_sync.py -p BTCUSDT -tf 1d --resync   # paksa unduh ulang penuh dari listing awal

Nama file output otomatis: <pair_lowercase>_<timeframe>.csv
Interval valid (sama seperti Binance): 1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M
"""

import argparse
import csv
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

BASE_URL = "https://api.binance.com/api/v3/klines"  # Binance SPOT public endpoint, tanpa API key
LIMIT = 1000  # maksimum per request di endpoint Spot (Futures maksimum 1500, Spot maksimum 1000)
VALID_INTERVALS = ["1m","3m","5m","15m","30m","1h","2h","4h","6h","8h","12h","1d","3d","1w","1M"]

FIELDNAMES = ["open_time", "open", "high", "low", "close", "close_time", "is_closed"]


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def fetch_klines_batch(symbol, interval, start_time_ms):
    """Satu request ke Binance Spot klines endpoint."""
    url = f"{BASE_URL}?symbol={symbol}&interval={interval}&limit={LIMIT}&startTime={start_time_ms}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        log(f"ERROR HTTP {e.code} dari Binance: {body}")
        sys.exit(1)
    except urllib.error.URLError as e:
        log(f"ERROR koneksi: {e}")
        sys.exit(1)


def fetch_klines_full(symbol, interval, start_time_ms):
    """
    Pagination penuh mulai dari start_time_ms sampai waktu sekarang.
    Berhenti hanya ketika batch kosong ATAU candle terakhir batch sudah >= sekarang,
    supaya tidak berhenti prematur akibat batch parsial di tengah histori (pola sim.py).
    """
    all_klines = []
    now_ms = int(time.time() * 1000)
    effective_start = start_time_ms

    while True:
        batch = fetch_klines_batch(symbol, interval, effective_start)

        if isinstance(batch, dict) and "code" in batch:
            log(f"ERROR dari Binance API: {batch}")
            sys.exit(1)

        if not batch:
            break

        all_klines.extend(batch)
        last_open_time = batch[-1][0]
        log(f"  ... diterima {len(batch)} candle, terakhir: "
            f"{datetime.fromtimestamp(last_open_time/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')}, "
            f"total sejauh ini: {len(all_klines)}")

        if last_open_time <= effective_start and len(batch) <= 1:
            break  # pengaman anti infinite-loop

        if last_open_time >= now_ms:
            break

        effective_start = last_open_time + 1
        time.sleep(0.25)  # jaga rate limit

    return all_klines


def klines_to_rows(klines):
    """Convert raw kline array -> dict rows, tandai is_closed berdasarkan close_time < sekarang."""
    now_ms = int(time.time() * 1000)
    rows = []
    for k in klines:
        open_time, open_p, high_p, low_p, close_p, _volume, close_time = k[0], k[1], k[2], k[3], k[4], k[5], k[6]
        rows.append({
            "open_time": int(open_time),
            "open": float(open_p),
            "high": float(high_p),
            "low": float(low_p),
            "close": float(close_p),
            "close_time": int(close_time),
            "is_closed": close_time < now_ms,
        })
    return rows


def load_local_data(path):
    """Load data lokal jika sudah ada. Return list of dict, sorted by open_time. [] jika belum ada file."""
    if not os.path.exists(path):
        return []
    rows = []
    with open(path, "r", newline="") as f:
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


def save_local_data(path, rows):
    rows.sort(key=lambda x: x["open_time"])
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def sync_data(pair, interval, output_file):
    """
    Sinkronisasi data lokal ala 'sync blockchain':
    - Jika file belum ada -> unduh penuh dari awal listing (startTime=0).
    - Jika file sudah ada -> unduh HANYA candle baru sejak candle terakhir tersimpan,
      lalu gabungkan (replace candle terakhir yang mungkin belum closed saat sync sebelumnya).
    """
    existing = load_local_data(output_file)

    if not existing:
        log(f"Data lokal belum ada untuk {pair} [{interval}]. Mengunduh seluruh histori dari Binance Spot...")
        klines = fetch_klines_full(pair, interval, start_time_ms=0)
        rows = klines_to_rows(klines)
        rows = [r for r in rows if r["is_closed"]]  # hanya simpan candle yang sudah closed
        save_local_data(output_file, rows)
        log(f"Selesai. Total {len(rows)} candle baru tersimpan di {output_file}")
        return rows

    last_stored = existing[-1]
    start_ms = last_stored["open_time"]

    log(f"Data lokal ditemukan ({len(existing)} candle, {output_file}).")
    log(f"Sinkronisasi: mengecek candle baru sejak "
        f"{datetime.fromtimestamp(start_ms/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')}...")

    klines = fetch_klines_full(pair, interval, start_time_ms=start_ms)
    new_rows = klines_to_rows(klines)
    new_rows = [r for r in new_rows if r["is_closed"]]

    # Merge: candle terakhir lama di-refresh (jaga-jaga waktu sync sebelumnya belum closed), sisanya ditambahkan
    merged = {r["open_time"]: r for r in existing[:-1]}
    for r in new_rows:
        merged[r["open_time"]] = r
    # Pastikan candle terakhir lama tetap ada kalau tidak ter-refresh oleh new_rows
    if last_stored["open_time"] not in merged:
        merged[last_stored["open_time"]] = last_stored

    final_rows = sorted(merged.values(), key=lambda x: x["open_time"])
    added = len(final_rows) - len(existing)

    save_local_data(output_file, final_rows)
    log(f"Selesai. {added} candle baru ditambahkan. Total sekarang: {len(final_rows)} candle di {output_file}")
    return final_rows


def main():
    parser = argparse.ArgumentParser(
        description="Unduh & sinkronisasi data historis OHLCV dari Binance Spot (incremental, tanpa API key)."
    )
    parser.add_argument("-p", "--pair", type=str, required=True,
                         help="Nama pair, contoh: BTCUSDT, ETHUSDT, SOLUSDT")
    parser.add_argument("-tf", "--timeframe", type=str, required=True,
                         help=f"Interval candle. Pilihan: {', '.join(VALID_INTERVALS)}")
    parser.add_argument("--resync", action="store_true",
                         help="Paksa unduh ulang PENUH dari listing paling awal, menimpa file lokal yang ada. "
                              "Gunakan ini jika curiga data lokal tidak lengkap dari awal listing.")
    args = parser.parse_args()

    pair = args.pair.upper()
    interval = args.timeframe.lower() if args.timeframe.lower() != "1m".upper() else args.timeframe
    interval = args.timeframe
    if interval not in VALID_INTERVALS:
        log(f"ERROR: timeframe '{interval}' tidak valid. Pilihan: {', '.join(VALID_INTERVALS)}")
        sys.exit(1)

    output_file = f"{pair.lower()}_{interval}.csv"

    if args.resync and os.path.exists(output_file):
        log(f"--resync aktif: menghapus data lokal lama {output_file} dan mengunduh penuh dari awal listing...")
        os.remove(output_file)

    log(f"Target: pair={pair} | timeframe={interval} | file={output_file}")
    rows = sync_data(pair, interval, output_file)

    if rows:
        start_label = datetime.fromtimestamp(rows[0]["open_time"]/1000, tz=timezone.utc).strftime("%Y-%m-%d")
        end_label = datetime.fromtimestamp(rows[-1]["open_time"]/1000, tz=timezone.utc).strftime("%Y-%m-%d")
        log(f"Rentang data tersimpan: {start_label} s/d {end_label} ({len(rows)} candle)")


if __name__ == "__main__":
    main()

