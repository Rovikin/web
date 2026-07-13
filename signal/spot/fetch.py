#!/usr/bin/env python3

import csv
import glob
import json
import os
import re
import sys
import threading
import time
import urllib.request
import urllib.error
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone


SPOT_BASE_URL = "https://api.binance.com/api/v3/klines"
SPOT_TICKER_URL = "https://api.binance.com/api/v3/ticker/24hr"
SPOT_LIMIT = 1000

TIMEFRAME = "1d"
INTERVAL_MS = 86_400_000

TOP_N_PAIRS = 100
PRUNE_MAX_CANDLES = 730

MAX_WORKERS = 10

FIELDNAMES = ["open_time", "open", "high", "low", "close", "close_time", "is_closed"]

CACHE_DIR = ".backtest_cache"

_log_lock = threading.Lock()


def log(msg):
    with _log_lock:
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


def die(msg):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


STABLECOIN_BASES = {
    "USDC", "FDUSD", "BUSD", "TUSD", "USD1", "DAI", "USDP", "PYUSD",
    "EURI", "AEUR", "XUSD", "USDE", "RLUSD", "GUSD", "FRAX", "USDD",
}


def _is_stablecoin_pair(symbol):
    base = symbol[:-len("USDT")] if symbol.endswith("USDT") else symbol
    return base.upper() in STABLECOIN_BASES


def fetch_top_pairs(n=TOP_N_PAIRS):
    req = urllib.request.Request(SPOT_TICKER_URL, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError) as e:
        die(f"Gagal mengambil daftar ticker dari Binance Spot: {e}")

    usdt_pairs = [d for d in data if d.get("symbol", "").endswith("USDT")]

    excluded = [d["symbol"] for d in usdt_pairs if _is_stablecoin_pair(d["symbol"])]
    if excluded:
        log(f"Dikecualikan (pair stablecoin-vs-stablecoin): {', '.join(sorted(excluded))}")
    usdt_pairs = [d for d in usdt_pairs if not _is_stablecoin_pair(d["symbol"])]

    usdt_pairs.sort(key=lambda d: float(d.get("quoteVolume", 0)), reverse=True)
    return [d["symbol"] for d in usdt_pairs[:n]]



def next_candle_due_at(last_open_time_ms):
    return last_open_time_ms + (2 * INTERVAL_MS)


def spot_fetch_batch(symbol, start_time_ms):
    safe_symbol = urllib.parse.quote(symbol, safe="")
    url = f"{SPOT_BASE_URL}?symbol={safe_symbol}&interval={TIMEFRAME}&limit={SPOT_LIMIT}&startTime={start_time_ms}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode(errors="ignore")
        log(f"  ERROR HTTP {e.code} dari Binance Spot: {body}")
        return None
    except urllib.error.URLError as e:
        log(f"  ERROR koneksi ke Binance Spot: {e}")
        return None


def spot_fetch_full(symbol, start_time_ms):
    all_klines = []
    now_ms = int(time.time() * 1000)
    effective_start = start_time_ms

    while True:
        batch = spot_fetch_batch(symbol, effective_start)

        if batch is None:
            return None

        if isinstance(batch, dict) and "code" in batch:
            log(f"  ERROR dari Binance Spot API: {batch}")
            return None

        if not batch:
            break

        all_klines.extend(batch)
        last_open_time = batch[-1][0]

        if last_open_time <= effective_start and len(batch) <= 1:
            break
        if last_open_time >= now_ms:
            break

        effective_start = last_open_time + 1
        time.sleep(0.2)

    return all_klines


def klines_to_rows(klines):
    now_ms = int(time.time() * 1000)
    rows = []
    for k in klines:
        open_time, open_p, high_p, low_p, close_p, close_time = k[0], k[1], k[2], k[3], k[4], k[6]
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
    if len(rows) > PRUNE_MAX_CANDLES:
        rows = rows[-PRUNE_MAX_CANDLES:]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    return rows


def output_filename(pair):
    return f"{pair.lower()}_{TIMEFRAME}.csv"



def cleanup_stale_pairs(current_pairs):
    current_files = {output_filename(p) for p in current_pairs}
    local_files = set(glob.glob(f"*_{TIMEFRAME}.csv"))
    stale_files = local_files - current_files

    if not stale_files:
        return 0

    for f in sorted(stale_files):
        try:
            os.remove(f)
            log(f"Dibuang (sudah tidak top-{TOP_N_PAIRS}): {f}")
        except OSError as e:
            log(f"  Gagal menghapus {f}: {e}")
            continue

        safe_base = re.sub(r'[^A-Za-z0-9_.-]', '_', f)
        cache_file = os.path.join(CACHE_DIR, f"{safe_base}.json")
        if os.path.exists(cache_file):
            try:
                os.remove(cache_file)
            except OSError:
                pass

    return len(stale_files)



def sync_pair(pair, output_file):
    existing = load_local_data(output_file)

    if not existing:
        now_ms = int(time.time() * 1000)
        start_ms = now_ms - (PRUNE_MAX_CANDLES + 5) * INTERVAL_MS
        log(f"  Data lokal belum ada. Mengunduh ~{PRUNE_MAX_CANDLES} candle terakhir...")
        klines = spot_fetch_full(pair, start_ms)
        if klines is None:
            log(f"  GAGAL mengunduh {pair} -- dilewati.")
            return None
        rows = klines_to_rows(klines)
        rows = [r for r in rows if r["is_closed"]]

        if not rows:
            log(f"  Tidak ada data candle untuk {pair} (kemungkinan sudah "
                f"delisted/tidak tradable) -- dilewati, tidak menyimpan file kosong.")
            return []

        rows = save_local_data(output_file, rows)
        log(f"  Selesai. {len(rows)} candle tersimpan di {output_file}")
        return rows

    last_stored = existing[-1]
    start_ms = last_stored["open_time"]

    due_at = next_candle_due_at(start_ms)
    now_ms = int(time.time() * 1000)
    if now_ms < due_at:
        wait_hr = (due_at - now_ms) / 3_600_000
        log(f"  Sudah up-to-date ({len(existing)} candle) -- candle berikutnya "
            f"~{wait_hr:.1f} jam lagi. Request dilewati.")
        return existing

    klines = spot_fetch_full(pair, start_ms)
    if klines is None:
        log(f"  GAGAL sync {pair} -- data lokal lama tetap dipakai.")
        return existing

    new_rows = klines_to_rows(klines)
    new_rows = [r for r in new_rows if r["is_closed"]]

    merged = {r["open_time"]: r for r in existing}
    for r in new_rows:
        merged[r["open_time"]] = r

    final_rows = sorted(merged.values(), key=lambda x: x["open_time"])
    added = len(final_rows) - len(existing)
    final_rows = save_local_data(output_file, final_rows)

    log(f"  Selesai. {added} candle baru, {len(final_rows)} candle tersimpan (pruned) di {output_file}")
    return final_rows



def main():
    if len(sys.argv) > 1:
        die("fetch.py tidak menerima argumen. Cukup jalankan: python3 fetch.py")

    log(f"Mengambil daftar top {TOP_N_PAIRS} pair USDT Spot berdasarkan volume 24 jam...")
    pairs = fetch_top_pairs(TOP_N_PAIRS)
    log(f"Ditemukan {len(pairs)} pair. Timeframe: {TIMEFRAME} | Mode: pruned (maks {PRUNE_MAX_CANDLES} candle/pair) "
        f"| Worker paralel: {MAX_WORKERS}")

    removed = cleanup_stale_pairs(pairs)
    if removed:
        log(f"Pruned by ranking: {removed} pair lama (sudah tidak top-{TOP_N_PAIRS}) dibuang dari lokal.")
    print()

    ok_count = 0
    fail_count = 0
    skipped_count = 0

    def _job(pair):
        output_file = output_filename(pair)
        try:
            rows = sync_pair(pair, output_file)
            if rows is None:
                return pair, "fail"
            if len(rows) == 0:
                return pair, "skip"
            return pair, "ok"
        except Exception as e:
            log(f"  GAGAL sync {pair}: {e}")
            return pair, "fail"

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {executor.submit(_job, pair): pair for pair in pairs}
        for i, future in enumerate(as_completed(futures), 1):
            pair, success = future.result()
            log(f"[{i}/{len(pairs)}] selesai: {pair}")
            if success:
                ok_count += 1
            else:
                fail_count += 1

    print()
    log(f"Sync selesai. Berhasil: {ok_count} | Gagal: {fail_count} | Total: {len(pairs)}")


if __name__ == "__main__":
    main()

