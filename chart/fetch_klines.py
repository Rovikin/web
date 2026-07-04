"""
Fetch data historis OHLCV dari Binance Futures API -> simpan ke CSV.
Jalankan di Termux: python3 fetch_klines.py
"""
import urllib.request
import json
import csv
import time
import sys

SYMBOL = "BTCUSDT"
INTERVAL = "15m"          # ganti sesuai kebutuhan: 1m, 5m, 15m, 1h, 4h, 1d
BASE_URL = "https://fapi.binance.com/fapi/v1/klines"  # Futures endpoint (sesuai bot Anda)
LIMIT = 1500              # max per request di endpoint futures
OUTPUT_FILE = f"{SYMBOL.lower()}_{INTERVAL}.csv"

def fetch_klines(symbol, interval, start_time=None, end_time=None, limit=1500):
    url = f"{BASE_URL}?symbol={symbol}&interval={interval}&limit={limit}"
    if start_time:
        url += f"&startTime={start_time}"
    if end_time:
        url += f"&endTime={end_time}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read().decode())

def main():
    all_rows = []
    # mulai dari waktu paling awal Binance Futures BTCUSDT listing (Sept 2019), aman mulai dari 0
    start_time = 1569888000000  # 2019-10-01 00:00:00 UTC dalam ms
    end_time = int(time.time() * 1000)

    print(f"Mengunduh {SYMBOL} interval {INTERVAL} dari Binance Futures...")

    while start_time < end_time:
        try:
            klines = fetch_klines(SYMBOL, INTERVAL, start_time=start_time, limit=LIMIT)
        except Exception as e:
            print(f"Error: {e} -- retry dalam 3 detik...")
            time.sleep(3)
            continue

        if not klines:
            break

        for k in klines:
            all_rows.append({
                "open_time": k[0],
                "open": k[1],
                "high": k[2],
                "low": k[3],
                "close": k[4],
                "close_time": k[6],
                "is_closed": True
            })

        last_open_time = klines[-1][0]
        print(f"  Terkumpul {len(all_rows)} candle | terakhir: {time.strftime('%Y-%m-%d %H:%M', time.gmtime(last_open_time/1000))}")

        # next start = candle terakhir + 1ms untuk hindari duplikat
        start_time = last_open_time + 1

        if len(klines) < LIMIT:
            break  # sudah mencapai data terbaru

        time.sleep(0.3)  # hindari rate limit

    # tulis ke CSV
    with open(OUTPUT_FILE, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["open_time","open","high","low","close","close_time","is_closed"])
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"\nSelesai. Total {len(all_rows)} candle disimpan ke {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
