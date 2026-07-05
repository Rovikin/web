"""
fetch_xmr_kraken_sync.py -- Sinkronisasi data historis OHLC XMR/USD dari Kraken Public API.
TANPA API key. Jalankan di Termux: python3 fetch_xmr_kraken_sync.py

CARA KERJA SYNC DI SINI (PENTING -- beda dengan sync Binance):
Endpoint OHLC Kraken HANYA PERNAH mengembalikan maksimal 720 candle TERBARU,
berapapun nilai parameter 'since' yang dikirim -- ini batasan resmi Kraken,
bukan sesuatu yang bisa diatur dari sisi kita. Artinya kita TIDAK BISA
"mengambil candle lama yang belum ada" seperti sync Binance, karena Kraken
tidak pernah menyediakan candle lebih tua dari 720 hari lalu lewat endpoint ini.

Yang script ini lakukan sebagai gantinya:
- Setiap dijalankan, ambil 720 candle terbaru dari Kraken (snapshot hari ini).
- Gabungkan (merge) dengan file lokal yang sudah ada, berdasarkan open_time.
  Candle yang sudah ada di file lokal TIDAK ditimpa duplikat, hanya candle
  BARU yang belum pernah tersimpan yang ditambahkan.
- Dengan menjalankan script ini secara rutin (misal tiap hari), file lokal
  Anda akan mengakumulasi histori lebih panjang dari 720 hari seiring waktu,
  karena setiap hari ada 1 candle baru yang tersimpan dan tidak akan hilang
  lagi meski suatu saat candle itu sudah di luar jendela 720 hari Kraken.
- Jika Anda BARU PERTAMA KALI menjalankan script ini, hasilnya akan sama
  seperti versi non-sync sebelumnya (720 candle). Baru mulai hari berikutnya
  proses akumulasi ini terasa manfaatnya.

Penggunaan:
    python3 fetch_xmr_kraken_sync.py
"""
import urllib.request
import json
import csv
import os
import time

PAIR = "XMRUSD"
INTERVAL = 1440  # 1440 menit = 1 hari (daily)
OUTPUT_FILE = "xmrusd_daily_kraken.csv"
BASE_URL = "https://api.kraken.com/0/public/OHLC"
FIELDNAMES = ["open_time", "open", "high", "low", "close", "close_time", "is_closed"]


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}")


def fetch_ohlc(pair, interval):
    url = f"{BASE_URL}?pair={pair}&interval={interval}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())


def load_local_data(path):
    """Load data lokal jika sudah ada. Return dict {open_time: row}. {} jika file belum ada."""
    if not os.path.exists(path):
        return {}
    rows = {}
    with open(path, "r", newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            open_time = int(r["open_time"])
            rows[open_time] = {
                "open_time": open_time,
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"]),
                "close_time": int(r["close_time"]),
                "is_closed": r["is_closed"] == "True",
            }
    return rows


def save_local_data(path, rows_dict):
    rows = sorted(rows_dict.values(), key=lambda x: x["open_time"])
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return rows


def main():
    existing = load_local_data(OUTPUT_FILE)
    is_first_run = len(existing) == 0

    if is_first_run:
        log(f"Belum ada data lokal ({OUTPUT_FILE}). Ini pengunduhan pertama.")
    else:
        log(f"Data lokal ditemukan: {len(existing)} candle tersimpan di {OUTPUT_FILE}.")
        oldest = min(existing.keys())
        newest = max(existing.keys())
        log(f"  Rentang tersimpan saat ini: {time.strftime('%Y-%m-%d', time.gmtime(oldest/1000))} "
            f"s/d {time.strftime('%Y-%m-%d', time.gmtime(newest/1000))}")

    log(f"Mengambil snapshot 720 candle terbaru {PAIR} dari Kraken...")
    try:
        data = fetch_ohlc(PAIR, INTERVAL)
    except Exception as e:
        log(f"Gagal mengambil data: {e}")
        return

    if data.get("error"):
        log(f"Error dari Kraken: {data['error']}")
        return

    result = data.get("result", {})
    pair_key = [k for k in result.keys() if k != "last"]
    if not pair_key:
        log("Tidak ada data ditemukan. Kemungkinan nama pair salah.")
        log(f"Response penuh: {data}")
        return

    ohlc_raw = result[pair_key[0]]
    fetched_count = len(ohlc_raw)
    new_count = 0

    for entry in ohlc_raw:
        # format Kraken: [time, open, high, low, close, vwap, volume, count]
        ts, o, h, l, c, vwap, vol, count = entry
        open_time = int(ts) * 1000
        close_time = open_time + (INTERVAL * 60 * 1000) - 1

        if open_time not in existing:
            new_count += 1

        # Selalu simpan/refresh -- candle hari ini yang mungkin belum closed saat sync
        # sebelumnya akan ter-update dengan nilai terbaru dari Kraken.
        existing[open_time] = {
            "open_time": open_time,
            "open": o,
            "high": h,
            "low": l,
            "close": c,
            "close_time": close_time,
            "is_closed": True,
        }

    final_rows = save_local_data(OUTPUT_FILE, existing)

    log(f"Snapshot Kraken: {fetched_count} candle diterima, {new_count} di antaranya baru.")
    log(f"Selesai. Total sekarang: {len(final_rows)} candle tersimpan di {OUTPUT_FILE}")
    if final_rows:
        start = time.strftime('%Y-%m-%d', time.gmtime(final_rows[0]['open_time']/1000))
        end = time.strftime('%Y-%m-%d', time.gmtime(final_rows[-1]['open_time']/1000))
        log(f"Rentang data tersimpan: {start} s/d {end}")

    if is_first_run:
        log("\nCatatan: karena ini unduhan pertama, hasilnya masih terbatas pada jendela")
        log("720 hari terakhir yang disediakan Kraken. Jalankan script ini secara rutin")
        log("(misal tiap hari via cron/Termux:Boot) agar histori lokal Anda terus")
        log("bertambah panjang seiring waktu, tidak terbatas 720 hari lagi ke depan.")


if __name__ == "__main__":
    main()

