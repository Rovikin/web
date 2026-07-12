"""
Backtest MACD Crossover (16/26/12) -- PURE PYTHON, tanpa numpy/pandas.
Parameter tunggal tetap, hasil riset generalisasi lintas 20 pair (IS/OOS split
+ walk-forward analysis expanding window). Bukan grid search in-sample.
Kompatibel dengan Termux standar tanpa instalasi library tambahan.

Cara pakai:
    python3 backtest.py                          # auto-scan semua .csv di folder ini, tabel CLI
    python3 backtest.py --detail                  # auto-scan + tulis/perbarui manifest.json
    python3 backtest.py <file_csv>                # satu file, tabel CLI
    python3 backtest.py <file_csv_1> <file_csv_2> --detail # banyak file spesifik + manifest.json

Hanya pair dengan SINYAL TERBARU (terjadi HARI INI) yang ditampilkan --
baik di tabel CLI maupun di manifest.json. Pair yang datanya belum cukup
untuk menghasilkan sinyal, atau sinyal terakhirnya terjadi kemarin atau
lebih lama, tidak ditampilkan sama sekali di kedua mode.

Konteks: Binance Spot, timeframe 1D, long-only (beli lalu jual -- tidak ada
short). Sinyal ditampilkan sebagai BUY (crossover naik, entry/holding) atau
SELL (crossover turun, exit -- menunggu sinyal BUY berikutnya).

CATATAN manifest.json / index.html:
Skrip ini TIDAK LAGI menulis HTML sama sekali. Flag --detail menulis
.backtest_cache/manifest.json -- satu file JSON teragregasi berisi seluruh
hasil (bullish + bearish, sudah difilter freshness). index.html (statis,
terpisah, dikelola manual) meng-fetch manifest.json ini via app.js dan
merender tabel di browser. Pemisahan ini membuat index.html jarang berubah
(diff git kecil & stabil), sementara manifest.json yang berubah tiap run
adalah data terstruktur murni -- diff-nya jauh lebih rapi dibanding diff
HTML seperti pada versi sebelumnya.

CATATAN METODE:
Parameter MACD 16/26/12 dipakai tetap untuk semua pair, hasil dari riset
terpisah yang menguji generalisasi 1 parameter tunggal lintas 20 pair
memakai IS/OOS split dan walk-forward analysis (expanding window, 5 fold).
Tidak ada filter kelayakan (MIN_CALMAR/MIN_TRADES) -- semua pair dengan
sinyal terbaru ditampilkan apa adanya.
"""
import csv
import glob
import hashlib
import json
import os
import re
import sys

try:
    from rich.console import Console
    from rich.table import Table
    from rich import box
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

FEE_PCT = 0.15

# Parameter MACD tetap -- hasil riset generalisasi lintas 20 pair (IS/OOS +
# walk-forward expanding window, 5 fold). Setup ini menang di semua metrik
# walk-forward genuine dibanding kandidat lain (termasuk default klasik 12/26/9):
# 90% pair dengan return WF rata-rata positif, median Sharpe per fold 0.368,
# median Calmar per fold 0.126, 65% pair signifikan pada uji bootstrap (p<0.05).
# TIDAK di-grid-search ulang per pair -- sengaja satu parameter untuk semua,
# supaya bot live punya satu codepath sederhana dan tidak overfit per aset.
MACD_FAST = 16
MACD_SLOW = 26
MACD_SIGNAL = 12

# Hanya sinyal yang terjadi dalam jendela ini (hari) yang ditampilkan.
# 0 = hanya sinyal HARI INI; sinyal 1 hari lalu ke atas dianggap kadaluarsa.
SIGNAL_FRESHNESS_DAYS = 0


def _freshness_label():
    """Teks deskriptif untuk jendela freshness saat ini, dipakai di semua
    tempat (CLI & HTML) supaya kalimatnya selalu benar secara bahasa,
    baik untuk kasus 0 hari ('hari ini') maupun N hari ('N hari terakhir')."""
    if SIGNAL_FRESHNESS_DAYS <= 0:
        return "hari ini"
    return f"{SIGNAL_FRESHNESS_DAYS} hari terakhir"

# Direktori cache -- menyimpan hasil backtest per file CSV agar tidak
# dihitung ulang jika file sumber belum berubah.
CACHE_DIR = ".backtest_cache"
CACHE_VERSION = 2  # dinaikkan saat parameter/logic berubah -- membuat cache lama otomatis basi

# Label timeframe untuk ditampilkan di ringkasan (dari kode interval Binance/umum)
TIMEFRAME_LABELS = {
    "1m": "1 Minute", "3m": "3 Minute", "5m": "5 Minute", "15m": "15 Minute", "30m": "30 Minute",
    "1h": "1 Hour", "2h": "2 Hour", "4h": "4 Hour", "6h": "6 Hour", "8h": "8 Hour", "12h": "12 Hour",
    "1d": "1 Day", "daily": "1 Day", "3d": "3 Day",
    "1w": "1 Week", "weekly": "1 Week",
    "1M": "1 Month", "monthly": "1 Month",
}


def parse_filename(path):
    """
    Coba tebak nama pair & timeframe dari nama file, mengikuti pola umum:
    <pair>_<timeframe>.csv
    Contoh: btcusdt_1d.csv -> ('BTCUSDT', '1 Day')
    Jika tidak bisa ditebak, kembalikan nama file apa adanya sebagai pair, timeframe '-'.
    """
    base = os.path.basename(path)
    name = re.sub(r'\.csv$', '', base, flags=re.IGNORECASE)
    parts = name.split('_')

    if not parts:
        return base, "-"

    pair_guess = parts[0].upper()

    tf_label = "-"
    for part in parts[1:]:
        key = part.lower()
        if key in TIMEFRAME_LABELS:
            tf_label = TIMEFRAME_LABELS[key]
            break

    return pair_guess, tf_label


def find_csv_files():
    """Cari semua file .csv di direktori kerja saat ini (tidak rekursif ke subfolder)."""
    return sorted(glob.glob("*.csv"))


def load_csv(path):
    rows = []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                'open_time': int(r['open_time']),
                'close': float(r['close']),
            })
    rows.sort(key=lambda x: x['open_time'])
    return rows


def ema_series(closes, span):
    alpha = 2 / (span + 1)
    ema = [closes[0]]
    for price in closes[1:]:
        ema.append(alpha * price + (1 - alpha) * ema[-1])
    return ema


def macd_series(closes, fast, slow, signal):
    """Hitung garis MACD (EMA cepat - EMA lambat) dan garis sinyal (EMA dari MACD)."""
    ema_fast = ema_series(closes, fast)
    ema_slow = ema_series(closes, slow)
    macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
    signal_line = ema_series(macd_line, signal)
    return macd_line, signal_line


def backtest_macd(closes, fast, slow, signal, open_times=None):
    """
    Strategi long-only spot: beli saat crossover naik, jual saat crossover
    turun. 'BUY' = crossover naik (entry/holding), 'SELL' = crossover turun
    (exit, menunggu sinyal BUY berikutnya).
    """
    n = len(closes)
    macd_line, signal_line = macd_series(closes, fast, slow, signal)
    above = [macd_line[i] > signal_line[i] for i in range(n)]

    trades = []
    position = None
    entry_price = None

    last_signal_idx = None   # index candle saat crossover TERAKHIR terjadi (beli atau jual)
    last_signal_type = None  # "BUY" atau "SELL"

    for i in range(slow, n):
        if position is None and (not above[i-1]) and above[i]:
            position = 'LONG'
            entry_price = closes[i]
            last_signal_idx = i
            last_signal_type = "BUY"
        elif position == 'LONG' and above[i-1] and (not above[i]):
            gross = (closes[i] - entry_price) / entry_price * 100
            trades.append({"pnl": gross - 2 * FEE_PCT})
            position = None
            last_signal_idx = i
            last_signal_type = "SELL"

    if position == 'LONG':
        gross = (closes[-1] - entry_price) / entry_price * 100
        trades.append({"pnl": gross - 2 * FEE_PCT})

    if len(trades) < 3:
        return None

    equity = 1.0
    peak = 1.0
    max_dd = 0.0
    wins = 0

    for t in trades:
        pnl = t["pnl"]
        equity *= (1 + pnl / 100)
        if equity > peak:
            peak = equity
        dd = (equity - peak) / peak * 100
        if dd < max_dd:
            max_dd = dd
        if pnl > 0:
            wins += 1

    total_return = (equity - 1) * 100
    win_rate = wins / len(trades) * 100
    calmar = total_return / abs(max_dd) if max_dd != 0 else 0

    days_since_last_signal = None
    if open_times is not None and last_signal_idx is not None:
        days_since_last_signal = (open_times[-1] - open_times[last_signal_idx]) / 86_400_000  # ms -> hari

    return {
        'fast': fast, 'slow': slow, 'signal': signal,
        'n_trades': len(trades),
        'win_rate': win_rate,
        'total_return_pct': total_return,
        'max_dd_pct': max_dd,
        'calmar': calmar,
        'last_signal_type': last_signal_type,
        'days_since_last_signal': days_since_last_signal,
    }


def _days_label(days):
    """Format angka hari: 0 -> 'Hari ini', selain itu '<N> hari lalu'."""
    rounded = round(days)
    if rounded <= 0:
        return "Hari ini"
    return f"{rounded} hari lalu"


def _fmt_last_signal(r):
    """Format ringkas plain-text: 'Hari ini (BUY)' atau '<N> hari lalu (BUY)'."""
    if r.get('days_since_last_signal') is None or r.get('last_signal_type') is None:
        return "-"
    return f"{_days_label(r['days_since_last_signal'])} ({r['last_signal_type']})"


def _fmt_last_signal_rich(r):
    """Format dengan warna rich: hijau untuk BUY (holding), merah untuk SELL (menunggu entry)."""
    if r.get('days_since_last_signal') is None or r.get('last_signal_type') is None:
        return "-"
    sig_type = r['last_signal_type']
    color = "green" if sig_type == "BUY" else "red"
    text = f"{_days_label(r['days_since_last_signal'])} ({sig_type})"
    return f"[{color}]{text}[/{color}]"


def is_signal_fresh(result):
    """True jika result punya sinyal dan sinyal itu, setelah dibulatkan
    dengan cara yang sama seperti label tampilan (_days_label), termasuk
    dalam SIGNAL_FRESHNESS_DAYS hari (default: hanya 'Hari ini', yaitu
    round(days) <= 0). Memakai round() -- bukan raw float -- supaya pair
    yang labelnya tertulis 'Hari ini' tidak pernah tersaring keluar oleh
    filter ini, dan sebaliknya."""
    if result is None:
        return False
    days = result.get('days_since_last_signal')
    if days is None:
        return False
    return round(days) <= SIGNAL_FRESHNESS_DAYS


def _file_fingerprint(path):
    """
    Hitung fingerprint file CSV berdasarkan ukuran + hash konten (blake2b),
    dikombinasikan dengan parameter & versi cache supaya cache otomatis basi
    kalau file berubah ATAU parameter/logic berubah.
    """
    stat = os.stat(path)
    hasher = hashlib.blake2b(digest_size=16)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            hasher.update(chunk)
    content_hash = hasher.hexdigest()

    param_signature = json.dumps(
        {"fast": MACD_FAST, "slow": MACD_SLOW, "signal": MACD_SIGNAL, "fee": FEE_PCT, "v": CACHE_VERSION},
        sort_keys=True,
    )
    param_hash = hashlib.blake2b(param_signature.encode("utf-8"), digest_size=8).hexdigest()

    return f"{content_hash}_{param_hash}_{stat.st_size}"


def _cache_path_for(path):
    base = os.path.basename(path)
    safe_base = re.sub(r'[^A-Za-z0-9_.-]', '_', base)
    return os.path.join(CACHE_DIR, f"{safe_base}.json")


def _load_cache(path, fingerprint):
    """Coba muat hasil dari cache. Return dict hasil atau None jika cache tidak ada/tidak valid."""
    cache_file = _cache_path_for(path)
    if not os.path.exists(cache_file):
        return None
    try:
        with open(cache_file, "r", encoding="utf-8") as f:
            cached = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    if cached.get("fingerprint") != fingerprint:
        return None

    return cached


def _save_cache(path, fingerprint, bh_return, result, total_candle):
    """Simpan hasil backtest MACD (parameter tunggal) ke cache sebagai JSON."""
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_file = _cache_path_for(path)
    payload = {
        "fingerprint": fingerprint,
        "bh_return": bh_return,
        "total_candle": total_candle,
        "result": result,
    }
    tmp_file = cache_file + ".tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        json.dump(payload, f)
    os.replace(tmp_file, cache_file)


def run_one_file(path, use_cache=True):
    """
    Jalankan backtest MACD (parameter tetap 16/26/12) untuk satu file CSV.
    Return (path, result_or_None, bh_return).
    Tidak ada filter kelayakan -- result dihitung apa adanya; penyaringan
    "hanya sinyal segar" dilakukan di pemanggil (main), bukan di sini.
    """
    fingerprint = _file_fingerprint(path) if use_cache else None
    cached = _load_cache(path, fingerprint) if use_cache else None

    if cached is not None:
        bh_return = cached["bh_return"]
        result = cached["result"]
        return path, result, bh_return

    rows = load_csv(path)
    closes = [r['close'] for r in rows]
    open_times = [r['open_time'] for r in rows]
    total_candle = len(rows)

    bh_return = (closes[-1] - closes[0]) / closes[0] * 100

    result = backtest_macd(closes, MACD_FAST, MACD_SLOW, MACD_SIGNAL, open_times=open_times)

    if result is not None and use_cache:
        _save_cache(path, fingerprint, bh_return, result, total_candle)

    return path, result, bh_return


def split_and_sort_by_signal(summary):
    """
    Pisahkan hasil jadi dua grup berdasarkan jenis sinyal terakhir:
    - bullish_group: sinyal terakhir BUY (posisi masih terbuka)
    - bearish_group: sinyal terakhir SELL (menunggu sinyal beli berikutnya)
    Item TANPA sinyal segar (<= SIGNAL_FRESHNESS_DAYS hari) sudah difilter
    keluar sebelum fungsi ini dipanggil.
    Setiap grup diurutkan dari sinyal PALING BARU (hari lebih kecil) ke yang lebih lama.
    """
    bullish, bearish = [], []
    for item in summary:
        path, best, bh = item
        if best['last_signal_type'] == 'BUY':
            bullish.append(item)
        else:
            bearish.append(item)

    bullish.sort(key=lambda item: item[1]['days_since_last_signal'])
    bearish.sort(key=lambda item: item[1]['days_since_last_signal'])
    return bullish, bearish
# ---------------------------------------------------------------------------
# Manifest untuk index.html (mode --detail)
#
# backtest.py TIDAK LAGI menulis HTML. Sebagai gantinya, mode --detail
# menulis satu file manifest JSON (MANIFEST_PATH) berisi seluruh hasil
# (bullish + bearish + metadata), yang di-fetch oleh index.html/app.js di
# sisi browser untuk dirender jadi tabel.
#
# Keuntungan dibanding generate-HTML langsung:
# - index.html jadi file statis yang nyaris tidak pernah berubah -> diff
#   git kecil dan stabil; hanya style.css/app.js yang berubah kalau desain
#   diubah.
# - Yang berubah tiap run backtest cuma manifest.json -- satu file JSON
#   terstruktur, diff-nya jauh lebih rapi & predictable dibanding diff HTML.
# - Filter "hanya sinyal segar" tetap dihitung di Python (source of truth
#   metodologi), tapi presentasi (badge, warna, tabel) sepenuhnya jadi
#   urusan app.js -- pemisahan data vs tampilan yang lebih bersih.
# ---------------------------------------------------------------------------

MANIFEST_PATH = os.path.join(CACHE_DIR, "manifest.json")


def _manifest_row(path, result, bh_return):
    """Satu baris data mentah untuk manifest -- tanpa styling/formatting,
    murni angka & label supaya app.js bebas menentukan tampilannya sendiri."""
    pair, tf_label = parse_filename(path)
    return {
        "pair": pair,
        "timeframe": tf_label,
        "last_signal_type": result.get("last_signal_type"),
        "days_since_last_signal": result.get("days_since_last_signal"),
        "n_trades": result.get("n_trades"),
        "win_rate": result.get("win_rate"),
        "total_return_pct": result.get("total_return_pct"),
        "max_dd_pct": result.get("max_dd_pct"),
        "calmar": result.get("calmar"),
        "bh_return": bh_return,
    }


def _now_iso():
    import datetime
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def write_manifest(bullish, bearish, output_path=MANIFEST_PATH):
    """
    Tulis .backtest_cache/manifest.json: satu file berisi seluruh hasil
    (bullish + bearish, sudah difilter freshness & terurut) plus metadata
    parameter, supaya index.html cukup 1 fetch untuk merender seluruh
    halaman. File ini SELALU ditulis ulang penuh (bukan marker-replace) --
    karena isinya murni data terstruktur (bukan markup), ini aman dan
    diff git-nya tetap rapi.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    payload = {
        "generated_at": _now_iso(),
        "params": {
            "fast": MACD_FAST,
            "slow": MACD_SLOW,
            "signal": MACD_SIGNAL,
            "fee_pct": FEE_PCT,
            "signal_freshness_days": SIGNAL_FRESHNESS_DAYS,
            "freshness_label": _freshness_label(),
        },
        "bullish": [_manifest_row(p, r, bh) for p, r, bh in bullish],
        "bearish": [_manifest_row(p, r, bh) for p, r, bh in bearish],
    }

    tmp_path = output_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")
    os.replace(tmp_path, output_path)

    return output_path

def main():
    args = sys.argv[1:]

    detail_mode = False
    if "--detail" in args:
        detail_mode = True
        args.remove("--detail")

    use_cache = True
    if "--no-cache" in args:
        use_cache = False
        args.remove("--no-cache")

    if args:
        paths = args
    else:
        paths = find_csv_files()
        if not paths:
            msg = "Tidak ada file .csv ditemukan di direktori ini."
            usage = "Cara pakai: python3 backtest.py [<file_csv> ...]"
            if HAS_RICH:
                console.print(f"[red]{msg}[/red]")
                console.print(usage)
            else:
                print(msg)
                print(usage)
            sys.exit(1)

    summary = []
    for path in paths:
        p, best, bh = run_one_file(path, use_cache=use_cache)
        if is_signal_fresh(best):
            summary.append((p, best, bh))

    bullish, bearish = split_and_sort_by_signal(summary)

    def _build_rich_table(title, group, border_style):
        table = Table(title=title, box=box.ROUNDED, show_lines=True, title_style="bold magenta", border_style=border_style)
        table.add_column("Pair", style="bold cyan", no_wrap=True)
        table.add_column("Timeframe", style="cyan")
        table.add_column("Sinyal Terakhir", justify="right")

        for path, best, bh in group:
            pair, tf_label = parse_filename(path)
            row = [pair, tf_label, _fmt_last_signal_rich(best)]
            table.add_row(*row)
        return table

    def _print_plain_group(title, group):
        print(f"\n{title}")
        for path, best, bh in group:
            pair, tf_label = parse_filename(path)
            sig = _fmt_last_signal(best)
            print(f"{pair} Timeframe {tf_label}: Sinyal Terakhir {sig}")

    if not bullish and not bearish:
        msg = f"Tidak ada pair dengan sinyal {_freshness_label()}."
        console.print(f"[yellow]{msg}[/yellow]") if HAS_RICH else print(msg)
        if detail_mode:
            manifest_path = write_manifest(bullish, bearish)
            note = f"\nmanifest.json diperbarui (kosong -- tidak ada sinyal segar): {os.path.abspath(manifest_path)}"
            console.print(f"[bold yellow]{note}[/bold yellow]") if HAS_RICH else print(note)
        return

    if HAS_RICH:
        console.print()
        if bullish:
            console.print(_build_rich_table("Sinyal Terbaru -- Bullish (BUY)", bullish, "green"))
        if bearish:
            console.print()
            console.print(_build_rich_table("Sinyal Terbaru -- Bearish (SELL)", bearish, "red"))
    else:
        if bullish:
            _print_plain_group("Sinyal Terbaru -- Bullish (BUY):", bullish)
        if bearish:
            _print_plain_group("Sinyal Terbaru -- Bearish (SELL):", bearish)

    if detail_mode:
        manifest_path = write_manifest(bullish, bearish)
        msg = f"\nmanifest.json diperbarui: {os.path.abspath(manifest_path)}"
        console.print(f"[bold green]{msg}[/bold green]") if HAS_RICH else print(msg)


if __name__ == "__main__":
    main()

