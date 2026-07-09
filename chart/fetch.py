#!/usr/bin/env python3
"""
fetch.py -- Unduh & sinkronisasi data historis OHLCV.

Mendukung DUA sumber data:
  1. Binance Spot API (api.binance.com)   -- untuk semua pair *USDT/*BUSD dsb.
  2. Kraken Public API (api.kraken.com)   -- KHUSUS pair XMR (Monero, di-delisting
     dari Binance Februari 2024, sehingga tidak tersedia di Binance sama sekali).

MODE PENGGUNAAN:

  1) Sync SEMUA file .csv yang sudah ada di direktori ini sekaligus (default,
     tanpa argumen apapun). Script mengenali sumber data tiap file secara
     otomatis dari namanya (pair XMR -> Kraken, selain itu -> Binance Spot):

       python3 fetch.py

  2) Unduh/sync SATU pair + timeframe spesifik (perilaku lama, tetap sama):

       python3 fetch.py --pair BTCUSDT --timeframe 1d
       python3 fetch.py -p ETHUSDT -tf 4h
       python3 fetch.py -p XMRUSD -tf 1d          # otomatis pakai Kraken
       python3 fetch.py -p BTCUSDT -tf 1d --resync  # paksa unduh ulang penuh

  3) Bantuan:

       python3 fetch.py --help

CATATAN SUMBER DATA:
- Binance Spot: histori panjang (BTC sejak 2017), tanpa distorsi funding rate/
  leverage seperti kontrak Futures. Pagination penuh, unlimited ke belakang.
- Kraken (khusus XMR): endpoint OHLC Kraken HANYA PERNAH mengembalikan maksimal
  720 candle TERBARU, apapun parameter yang dikirim -- ini batasan resmi Kraken,
  bukan bug di script ini. Sync di sini bermakna: setiap dijalankan, ambil
  snapshot 720 candle terbaru lalu GABUNGKAN dengan data lokal (candle lama
  tidak hilang, hanya candle baru yang ditambahkan). Menjalankan script ini
  rutin dari waktu ke waktu akan mengakumulasi histori lebih panjang dari
  720 hari, karena tiap hari ada 1 candle baru yang "terkunci" secara lokal
  sebelum keluar dari jendela 720 hari milik Kraken.

TANPA library eksternal (hanya urllib bawaan Python) -- kompatibel Termux standar.

Nama file output otomatis:
    Binance : <pair_lowercase>_<timeframe>.csv          (mis. btcusdt_1d.csv)
    Kraken  : <pair_lowercase>_<timeframe>_kraken.csv    (mis. xmrusd_1d_kraken.csv)

Interval valid Binance : 1m,3m,5m,15m,30m,1h,2h,4h,6h,8h,12h,1d,3d,1w,1M
Interval Kraken (XMR)  : hanya 1d yang didukung script ini saat ini.
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# Konfigurasi umum
# ---------------------------------------------------------------------------

BINANCE_BASE_URL = "https://api.binance.com/api/v3/klines"
BINANCE_LIMIT = 1000
VALID_INTERVALS = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h",
                    "12h", "1d", "3d", "1w", "1M"]

# Durasi tiap interval dalam milidetik -- dipakai untuk menghitung kapan candle
# BERIKUTNYA seharusnya closed, supaya sync_binance/sync_kraken bisa melewati
# request jaringan sepenuhnya jika dipastikan belum ada candle baru yang mungkin
# closed sejak data lokal terakhir disimpan. (1M didekati 30 hari -- cukup untuk
# tujuan ini karena hanya dipakai sebagai ambang MINIMUM sebelum re-check ke
# server, bukan untuk keakuratan kalender penuh.)
INTERVAL_MS = {
    "1m": 60_000, "3m": 3*60_000, "5m": 5*60_000, "15m": 15*60_000, "30m": 30*60_000,
    "1h": 3_600_000, "2h": 2*3_600_000, "4h": 4*3_600_000, "6h": 6*3_600_000,
    "8h": 8*3_600_000, "12h": 12*3_600_000,
    "1d": 86_400_000, "3d": 3*86_400_000, "1w": 7*86_400_000, "1M": 30*86_400_000,
}

KRAKEN_BASE_URL = "https://api.kraken.com/0/public/OHLC"
KRAKEN_INTERVAL_MAP = {"1d": 1440}  # baru dukung daily untuk saat ini

FIELDNAMES = ["open_time", "open", "high", "low", "close", "close_time", "is_closed"]

# Pair yang HARUS lewat Kraken karena sudah di-delisting dari Binance
KRAKEN_ONLY_PAIRS = {"XMRUSD", "XMRUSDT"}


def next_candle_due_at(last_open_time_ms, interval):
    """
    Hitung kapan (epoch ms) candle BERIKUTNYA setelah last_open_time_ms
    seharusnya closed. Dipakai sebagai syarat sebelum melakukan request
    jaringan sama sekali -- jika waktu sekarang belum melewati titik ini,
    dipastikan tidak ada candle baru yang bisa closed, sehingga request ke
    server (Binance/Kraken) bisa dilewati sepenuhnya.

    last_open_time_ms adalah open_time candle TERAKHIR yang sudah tersimpan
    (dan sudah dipastikan closed). Candle berikutnya closed tepat 1 step
    setelah ia dibuka, yaitu di last_open_time_ms + 2*step (buka di +1*step,
    tutup di +2*step). Tidak ada buffer tambahan -- begitu waktu sekarang
    melewati titik itu, candle berikutnya dipastikan sudah closed dan aman
    untuk direquest. (Sebelumnya ada buffer 1% dari step sebagai toleransi
    jeda jam server, tapi untuk interval besar seperti harian itu berarti
    ~14 menit tambahan yang tidak perlu -- dihapus atas masukan langsung:
    perbandingan waktu closed yang eksak sudah cukup, tanpa perlu buffer.)
    """
    step = INTERVAL_MS.get(interval)
    if step is None:
        return None  # interval tak dikenal -- aman: selalu request seperti biasa
    return last_open_time_ms + (2 * step)



def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def die(msg, parser=None):
    """Cetak pesan error yang rapi + petunjuk --help, lalu keluar (bukan traceback Python)."""
    print(f"ERROR: {msg}\n", file=sys.stderr)
    if parser is not None:
        parser.print_help(sys.stderr)
    else:
        print("Jalankan 'python3 fetch.py --help' untuk melihat cara pakai.", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Sumber data: Binance Spot
# ---------------------------------------------------------------------------

def binance_fetch_batch(symbol, interval, start_time_ms):
    url = f"{BINANCE_BASE_URL}?symbol={symbol}&interval={interval}&limit={BINANCE_LIMIT}&startTime={start_time_ms}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        log(f"ERROR HTTP {e.code} dari Binance: {body}")
        return None
    except urllib.error.URLError as e:
        log(f"ERROR koneksi ke Binance: {e}")
        return None


def binance_fetch_full(symbol, interval, start_time_ms):
    all_klines = []
    now_ms = int(time.time() * 1000)
    effective_start = start_time_ms

    while True:
        batch = binance_fetch_batch(symbol, interval, effective_start)

        if batch is None:
            return None  # error jaringan/HTTP, sudah dilog di fungsi batch

        if isinstance(batch, dict) and "code" in batch:
            log(f"ERROR dari Binance API: {batch}")
            return None

        if not batch:
            break

        all_klines.extend(batch)
        last_open_time = batch[-1][0]
        log(f"  ... diterima {len(batch)} candle, terakhir: "
            f"{datetime.fromtimestamp(last_open_time/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')}, "
            f"total sejauh ini: {len(all_klines)}")

        if last_open_time <= effective_start and len(batch) <= 1:
            break

        if last_open_time >= now_ms:
            break

        effective_start = last_open_time + 1
        time.sleep(0.25)

    return all_klines


def binance_klines_to_rows(klines):
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


def sync_binance(pair, interval, output_file):
    """Sync satu pair Binance Spot (logic identik dengan versi fetch.py sebelumnya)."""
    existing = load_local_data(output_file)

    if not existing:
        log(f"Data lokal belum ada untuk {pair} [{interval}]. Mengunduh seluruh histori dari Binance Spot...")
        klines = binance_fetch_full(pair, interval, start_time_ms=0)
        if klines is None:
            log(f"GAGAL mengunduh {pair} [{interval}] -- dilewati.")
            return None
        rows = binance_klines_to_rows(klines)
        rows = [r for r in rows if r["is_closed"]]
        save_local_data(output_file, rows)
        log(f"Selesai. Total {len(rows)} candle baru tersimpan di {output_file}")
        return rows

    last_stored = existing[-1]
    start_ms = last_stored["open_time"]

    # Cek dulu: apakah candle BERIKUTNYA sudah mungkin closed? Jika belum,
    # tidak ada gunanya melakukan request ke Binance sama sekali -- hasilnya
    # dipastikan kosong (candle terakhir yang tersimpan masih yang terbaru
    # yang mungkin closed). Ini menghindari request jaringan sia-sia setiap
    # kali script dijalankan berulang dalam rentang waktu pendek.
    due_at = next_candle_due_at(start_ms, interval)
    now_ms = int(time.time() * 1000)
    if due_at is not None and now_ms < due_at:
        wait_min = (due_at - now_ms) / 60_000
        log(f"Data lokal {pair} [{interval}] sudah up-to-date -- candle berikutnya "
            f"baru mungkin closed dalam ~{wait_min:.0f} menit lagi. Request ke Binance dilewati.")
        return existing

    log(f"Data lokal ditemukan ({len(existing)} candle, {output_file}).")
    log(f"Sinkronisasi: mengecek candle baru sejak "
        f"{datetime.fromtimestamp(start_ms/1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M')}...")

    klines = binance_fetch_full(pair, interval, start_time_ms=start_ms)
    if klines is None:
        log(f"GAGAL sync {pair} [{interval}] -- data lokal lama tetap dipakai, dilewati.")
        return existing

    new_rows = binance_klines_to_rows(klines)
    new_rows = [r for r in new_rows if r["is_closed"]]

    merged = {r["open_time"]: r for r in existing[:-1]}
    for r in new_rows:
        merged[r["open_time"]] = r
    if last_stored["open_time"] not in merged:
        merged[last_stored["open_time"]] = last_stored

    final_rows = sorted(merged.values(), key=lambda x: x["open_time"])
    added = len(final_rows) - len(existing)

    save_local_data(output_file, final_rows)
    log(f"Selesai. {added} candle baru ditambahkan. Total sekarang: {len(final_rows)} candle di {output_file}")
    return final_rows


# ---------------------------------------------------------------------------
# Sumber data: Kraken (khusus XMR)
# ---------------------------------------------------------------------------

def kraken_fetch_ohlc(pair, kraken_interval):
    url = f"{KRAKEN_BASE_URL}?pair={pair}&interval={kraken_interval}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(url_req_or_req(req), timeout=15) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        log(f"ERROR koneksi ke Kraken: {e}")
        return None


def url_req_or_req(req):
    # helper kecil supaya mudah diuji/mock -- tidak mengubah perilaku
    return req


def sync_kraken(pair, interval, output_file):
    """
    Sync khusus XMR dari Kraken. interval hanya mendukung '1d' untuk saat ini.
    Selalu mengambil snapshot 720 candle terbaru & merge dengan file lokal (lihat
    penjelasan lengkap di docstring atas file).
    """
    if interval not in KRAKEN_INTERVAL_MAP:
        log(f"ERROR: timeframe '{interval}' belum didukung untuk Kraken/XMR. "
            f"Yang didukung saat ini: {', '.join(KRAKEN_INTERVAL_MAP.keys())}")
        return None

    kraken_interval = KRAKEN_INTERVAL_MAP[interval]
    existing_list = load_local_data(output_file)
    existing = {r["open_time"]: r for r in existing_list}
    is_first_run = len(existing) == 0

    if is_first_run:
        log(f"Data lokal belum ada untuk {pair} [{interval}] (Kraken). Unduhan pertama.")
    else:
        oldest = min(existing.keys())
        newest = max(existing.keys())
        log(f"Data lokal ditemukan: {len(existing)} candle tersimpan di {output_file}.")
        log(f"  Rentang tersimpan saat ini: {time.strftime('%Y-%m-%d', time.gmtime(oldest/1000))} "
            f"s/d {time.strftime('%Y-%m-%d', time.gmtime(newest/1000))}")

        # Sama seperti sync_binance: lewati request ke Kraken sepenuhnya jika
        # dipastikan belum ada candle baru yang mungkin closed sejak data
        # lokal terakhir. Kraken hanya mendukung interval harian saat ini,
        # tapi tetap dihitung generik lewat INTERVAL_MS/next_candle_due_at.
        due_at = next_candle_due_at(newest, interval)
        now_ms = int(time.time() * 1000)
        if due_at is not None and now_ms < due_at:
            wait_min = (due_at - now_ms) / 60_000
            log(f"Data lokal {pair} [{interval}] sudah up-to-date -- candle berikutnya "
                f"baru mungkin closed dalam ~{wait_min:.0f} menit lagi. Request ke Kraken dilewati.")
            return existing_list

    log(f"Mengambil snapshot {720} candle terbaru {pair} dari Kraken...")
    data = kraken_fetch_ohlc(pair, kraken_interval)
    if data is None:
        log(f"GAGAL mengambil data {pair} dari Kraken -- dilewati.")
        return existing_list if existing_list else None

    if data.get("error"):
        log(f"Error dari Kraken: {data['error']}")
        return existing_list if existing_list else None

    result = data.get("result", {})
    pair_key = [k for k in result.keys() if k != "last"]
    if not pair_key:
        log("Tidak ada data ditemukan dari Kraken. Kemungkinan nama pair salah.")
        return existing_list if existing_list else None

    ohlc_raw = result[pair_key[0]]
    fetched_count = len(ohlc_raw)
    new_count = 0
    now_ms = int(time.time() * 1000)

    for entry in ohlc_raw:
        ts, o, h, l, c, vwap, vol, count = entry
        open_time = int(ts) * 1000
        close_time = open_time + (kraken_interval * 60 * 1000) - 1

        if open_time not in existing:
            new_count += 1

        existing[open_time] = {
            "open_time": open_time,
            "open": o, "high": h, "low": l, "close": c,
            "close_time": close_time,
            # Kraken tidak memberi status closed/belum secara eksplisit --
            # candle dianggap closed HANYA jika close_time (dihitung manual di
            # atas) sudah lewat waktu sekarang. Sebelumnya nilai ini di-hardcode
            # True, sehingga candle hari berjalan (harga belum final) ikut
            # tersimpan seolah sudah closed -- match dengan temuan empiris
            # sebelumnya (candle terakhir berubah nilainya antar unduhan).
            "is_closed": close_time < now_ms,
        }

    final_rows = sorted(existing.values(), key=lambda x: x["open_time"])
    # Buang candle yang belum closed sebelum disimpan -- konsisten dengan
    # perlakuan binance_klines_to_rows() untuk sumber Binance.
    final_rows = [r for r in final_rows if r["is_closed"]]
    save_local_data(output_file, final_rows)

    log(f"Snapshot Kraken: {fetched_count} candle diterima, {new_count} di antaranya baru.")
    log(f"Selesai. Total sekarang: {len(final_rows)} candle di {output_file}")

    if is_first_run:
        log("Catatan: unduhan pertama dari Kraken dibatasi jendela 720 hari terakhir. "
            "Jalankan ulang script ini secara rutin agar histori lokal terus terakumulasi.")

    return final_rows


# ---------------------------------------------------------------------------
# Penyimpanan lokal (format sama untuk kedua sumber data)
# ---------------------------------------------------------------------------

def load_local_data(path):
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
    rows = sorted(rows, key=lambda x: x["open_time"])
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


# ---------------------------------------------------------------------------
# Deteksi sumber data & parsing nama file (untuk mode sync-all)
# ---------------------------------------------------------------------------

def is_kraken_filename(filename):
    """File hasil Kraken selalu diberi akhiran _kraken.csv oleh script ini."""
    return filename.lower().endswith("_kraken.csv")


def parse_existing_filename(filename):
    """
    Tebak (pair, timeframe, source) dari nama file yang sudah ada di direktori.
    Pola yang didukung:
        <pair>_<timeframe>.csv            -> Binance
        <pair>_<timeframe>_kraken.csv     -> Kraken
    Contoh: btcusdt_1d.csv -> ('BTCUSDT', '1d', 'binance')
            xmrusd_1d_kraken.csv -> ('XMRUSD', '1d', 'kraken')
    Return None jika pola tidak dikenali (file diabaikan saat sync-all).
    """
    base = re.sub(r'\.csv$', '', filename, flags=re.IGNORECASE)

    if is_kraken_filename(filename):
        base_no_kraken = re.sub(r'_kraken$', '', base, flags=re.IGNORECASE)
        parts = base_no_kraken.split('_')
        if len(parts) < 2:
            return None
        pair = parts[0].upper()
        timeframe = '_'.join(parts[1:])
        # Normalisasi label lama seperti "daily" -> "1d"
        timeframe = {"daily": "1d", "weekly": "1w", "monthly": "1M"}.get(timeframe.lower(), timeframe)
        return pair, timeframe, "kraken"

    parts = base.split('_')
    if len(parts) < 2:
        return None
    pair = parts[0].upper()
    timeframe = '_'.join(parts[1:])
    timeframe = {"daily": "1d", "weekly": "1w", "monthly": "1M"}.get(timeframe.lower(), timeframe)

    if timeframe not in VALID_INTERVALS:
        return None  # nama file tidak mengikuti pola yang kita kenali, aman untuk diabaikan

    return pair, timeframe, "binance"


def find_existing_csv_files():
    return sorted([f for f in os.listdir(".") if f.lower().endswith(".csv")])


def determine_source(pair):
    """Tentukan sumber data yang harus dipakai untuk sebuah pair."""
    return "kraken" if pair.upper() in KRAKEN_ONLY_PAIRS else "binance"


def output_filename(pair, timeframe, source):
    if source == "kraken":
        return f"{pair.lower()}_{timeframe}_kraken.csv"
    return f"{pair.lower()}_{timeframe}.csv"


# ---------------------------------------------------------------------------
# Mode: sync satu pair spesifik
# ---------------------------------------------------------------------------

def run_single(pair, timeframe, resync, parser):
    pair = pair.upper()

    if timeframe not in VALID_INTERVALS and not (pair in KRAKEN_ONLY_PAIRS and timeframe in KRAKEN_INTERVAL_MAP):
        die(f"timeframe '{timeframe}' tidak valid. Pilihan: {', '.join(VALID_INTERVALS)}", parser)

    source = determine_source(pair)
    output_file = output_filename(pair, timeframe, source)

    if resync and os.path.exists(output_file):
        log(f"--resync aktif: menghapus data lokal lama {output_file} dan mengunduh penuh dari awal...")
        os.remove(output_file)

    log(f"Target: pair={pair} | timeframe={timeframe} | sumber={source} | file={output_file}")

    if source == "kraken":
        rows = sync_kraken(pair, timeframe, output_file)
    else:
        rows = sync_binance(pair, timeframe, output_file)

    if rows:
        start_label = datetime.fromtimestamp(rows[0]["open_time"]/1000, tz=timezone.utc).strftime("%Y-%m-%d")
        end_label = datetime.fromtimestamp(rows[-1]["open_time"]/1000, tz=timezone.utc).strftime("%Y-%m-%d")
        log(f"Rentang data tersimpan: {start_label} s/d {end_label} ({len(rows)} candle)")
    else:
        log(f"Tidak ada data tersimpan untuk {pair} [{timeframe}].")


# ---------------------------------------------------------------------------
# Mode: sync semua file .csv yang sudah ada (default, tanpa argumen)
# ---------------------------------------------------------------------------

def run_sync_all():
    files = find_existing_csv_files()

    if not files:
        log("Tidak ada file .csv ditemukan di direktori ini.")
        log("Untuk mengunduh data baru, gunakan: python3 fetch.py --pair <PAIR> --timeframe <TF>")
        log("Jalankan 'python3 fetch.py --help' untuk info lengkap.")
        return

    jobs = []
    skipped = []
    for f in files:
        parsed = parse_existing_filename(f)
        if parsed is None:
            skipped.append(f)
            continue
        jobs.append((f, *parsed))  # (filename, pair, timeframe, source)

    log(f"Ditemukan {len(files)} file .csv, {len(jobs)} di antaranya dikenali untuk sync otomatis.")
    if skipped:
        log(f"Dilewati (nama file tidak dikenali polanya): {', '.join(skipped)}")

    if not jobs:
        log("Tidak ada file yang polanya dikenali. Tidak ada yang disinkronkan.")
        return

    print()
    ok_count = 0
    fail_count = 0

    for i, (filename, pair, timeframe, source) in enumerate(jobs, 1):
        log(f"[{i}/{len(jobs)}] Sync {pair} [{timeframe}] via {source} -> {filename}")
        try:
            if source == "kraken":
                rows = sync_kraken(pair, timeframe, filename)
            else:
                rows = sync_binance(pair, timeframe, filename)
            if rows:
                ok_count += 1
            else:
                fail_count += 1
        except Exception as e:
            log(f"GAGAL sync {filename}: {e}")
            fail_count += 1
        print()

    log(f"Sync-all selesai. Berhasil: {ok_count} | Gagal/dilewati: {fail_count} | Total: {len(jobs)}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        prog="fetch.py",
        description=(
            "Unduh & sinkronisasi data historis OHLCV dari Binance Spot dan Kraken "
            "(khusus XMR), tanpa API key."
        ),
        epilog=(
            "Tanpa argumen sama sekali: sinkronkan SEMUA file .csv yang sudah ada "
            "di direktori ini sekaligus.\n\n"
            "Contoh:\n"
            "  python3 fetch.py\n"
            "  python3 fetch.py --pair BTCUSDT --timeframe 1d\n"
            "  python3 fetch.py -p ETHUSDT -tf 4h\n"
            "  python3 fetch.py -p XMRUSD -tf 1d\n"
            "  python3 fetch.py -p BTCUSDT -tf 1d --resync"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("-p", "--pair", type=str, default=None,
                         help="Nama pair, contoh: BTCUSDT, ETHUSDT, SOLUSDT, XMRUSD. "
                              "Wajib diisi bersama --timeframe jika ingin sync satu pair spesifik.")
    parser.add_argument("-tf", "--timeframe", type=str, default=None,
                         help=f"Interval candle. Pilihan Binance: {', '.join(VALID_INTERVALS)}. "
                              f"Untuk XMR/Kraken saat ini hanya didukung: {', '.join(KRAKEN_INTERVAL_MAP.keys())}")
    parser.add_argument("--resync", action="store_true",
                         help="Paksa unduh ulang PENUH dari awal, menimpa file lokal yang ada. "
                              "Hanya berlaku saat --pair & --timeframe diisi (mode satu pair).")
    return parser


def main():
    parser = build_parser()

    # argparse akan otomatis menangani -h/--help dan keluar dengan pesan rapi.
    # Kita tangkap error parsing argumen (mis. flag tidak dikenal) supaya tidak
    # menampilkan traceback Python mentah ke pengguna.
    try:
        args = parser.parse_args()
    except SystemExit as e:
        # argparse sendiri sudah mencetak pesan usage yang rapi untuk -h/--help
        # maupun untuk argumen tidak valid; cukup teruskan exit code-nya.
        raise

    pair_given = args.pair is not None
    tf_given = args.timeframe is not None

    if not pair_given and not tf_given:
        # Mode default: sync semua file yang sudah ada
        run_sync_all()
        return

    if pair_given != tf_given:
        die("--pair dan --timeframe harus diisi BERSAMA-SAMA untuk sync satu pair spesifik. "
            "Atau jalankan tanpa argumen sama sekali untuk sync semua file .csv yang ada.",
            parser)

    run_single(args.pair, args.timeframe, args.resync, parser)


if __name__ == "__main__":
    main()

