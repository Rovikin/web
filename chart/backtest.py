"""
Backtest MACD Crossover (16/26/12) -- PURE PYTHON, tanpa numpy/pandas.
Parameter tunggal tetap, hasil riset generalisasi lintas 20 pair (IS/OOS split
+ walk-forward analysis expanding window). Bukan lagi grid search in-sample.
Kompatibel dengan Termux standar tanpa instalasi library tambahan.

Cara pakai:
    python3 backtest.py                          # auto-scan semua .csv di folder ini, ringkasan pendek
    python3 backtest.py --detail                 # auto-scan semua .csv, detail penuh + ringkasan + tulis README.md
    python3 backtest.py <file_csv>                # satu file, ringkasan pendek
    python3 backtest.py <file_csv> --detail       # satu file, detail penuh + tulis README.md
    python3 backtest.py <file_csv_1> <file_csv_2> # banyak file spesifik, ringkasan pendek

Contoh:
    python3 backtest.py
    python3 backtest.py btcusdt_1d.csv ethusdt_1d.csv --detail

CATATAN README.md:
Hanya flag --detail yang menulis/memperbarui README.md di direktori kerja saat ini.
Perintah biasa (tanpa --detail) TIDAK pernah menyentuh README.md.
Jika README.md sudah ada, hanya bagian di antara marker
<!-- BACKTEST_RESULTS_START --> ... <!-- BACKTEST_RESULTS_END -->
yang diperbarui -- konten lain yang Anda tulis manual di luar marker tetap aman.

CATATAN METODE:
Versi ini TIDAK lagi melakukan grid search EMA in-sample. Parameter MACD
16/26/12 dipakai tetap untuk semua pair, hasil dari riset terpisah yang
menguji generalisasi 1 parameter tunggal lintas 20 pair memakai IS/OOS split
dan walk-forward analysis (expanding window, 5 fold). Tidak ada lagi filter
kelayakan (MIN_CALMAR/MIN_TRADES) -- semua pair ditampilkan apa adanya.
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

# Direktori cache -- menyimpan hasil backtest per file CSV agar tidak
# dihitung ulang jika file sumber belum berubah.
CACHE_DIR = ".backtest_cache"
CACHE_VERSION = 2  # dinaikkan: format/logic berubah dari grid EMA ke MACD tetap

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
    <pair>_<timeframe>.csv  atau  <pair>usd_<timeframe>_<sumber>.csv, dst.
    Contoh: btcusdt_1d.csv -> ('BTCUSDT', '1 Day')
            xmrusd_daily_kraken.csv -> ('XMRUSD', '1 Day')
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
    files = sorted(glob.glob("*.csv"))
    return files


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


def detect_market_condition(rows):
    """
    Tentukan kondisi bull/bear keseluruhan periode data berdasarkan:
    - Perubahan harga close awal vs akhir (arah utama)
    - Persentase waktu harga berada di atas EMA 200 (proxy tren jangka panjang)
    Return dict: {label, price_change_pct, pct_time_above_ema200}
    """
    closes = [r['close'] for r in rows]
    n = len(closes)

    price_change_pct = (closes[-1] - closes[0]) / closes[0] * 100

    if n > 200:
        ema200 = ema_series(closes, 200)
        above_count = sum(1 for i in range(200, n) if closes[i] > ema200[i])
        pct_time_above = above_count / (n - 200) * 100
    else:
        pct_time_above = None

    # Klasifikasi sederhana: gabungan arah harga keseluruhan + dominasi waktu di atas EMA200
    if pct_time_above is not None:
        if price_change_pct > 0 and pct_time_above >= 50:
            label = "Bullish"
        elif price_change_pct < 0 and pct_time_above < 50:
            label = "Bearish"
        else:
            label = "Sideways/Mixed"
    else:
        label = "Bullish" if price_change_pct > 0 else "Bearish"

    return {
        "label": label,
        "price_change_pct": price_change_pct,
        "pct_time_above_ema200": pct_time_above,
    }

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
    n = len(closes)
    macd_line, signal_line = macd_series(closes, fast, slow, signal)
    above = [macd_line[i] > signal_line[i] for i in range(n)]

    trades = []
    position = None
    entry_price = None
    entry_idx = None

    last_signal_idx = None   # index candle saat crossover TERAKHIR terjadi (buy atau sell)
    last_signal_type = None  # "BUY" atau "SELL"

    for i in range(slow, n):
        if position is None and (not above[i-1]) and above[i]:
            position = 'LONG'
            entry_price = closes[i]
            entry_idx = i
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
    current_position_status = "SELL (menunggu sinyal BUY)" if position is None else "BUY (masih holding)"
    if open_times is not None and last_signal_idx is not None:
        days_since_last_signal = (open_times[-1] - open_times[last_signal_idx]) / 86400000  # ms -> hari

    return {
        'fast': fast, 'slow': slow, 'signal': signal,
        'n_trades': len(trades),
        'win_rate': win_rate,
        'total_return_pct': total_return,
        'max_dd_pct': max_dd,
        'calmar': calmar,
        'last_signal_type': last_signal_type,
        'days_since_last_signal': days_since_last_signal,
        'current_position_status': current_position_status,
    }

def _fmt_pct_plain(val):
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.2f}%"


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
    """Format dengan warna rich: hijau untuk BUY (holding), merah untuk SELL (menunggu beli)."""
    if r.get('days_since_last_signal') is None or r.get('last_signal_type') is None:
        return "-"
    sig_type = r['last_signal_type']
    color = "green" if sig_type == "BUY" else "red"
    text = f"{_days_label(r['days_since_last_signal'])} ({sig_type})"
    return f"[{color}]{text}[/{color}]"


def _file_fingerprint(path):
    """
    Hitung fingerprint file CSV berdasarkan ukuran + hash konten (blake2b),
    dikombinasikan dengan grid EMA & versi cache supaya cache otomatis basi
    kalau file berubah ATAU grid parameter/logic berubah.
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


def run_one_file(path, verbose=True, collect_detail=False, use_cache=True):
    """
    Jalankan backtest MACD (parameter tetap 16/26/12) untuk satu file CSV.
    Return (path, result_or_None, bh_return, detail_dict_or_None).
    Tidak ada lagi filter kelayakan -- result ditampilkan apa adanya, termasuk
    pair dengan jumlah trade sedikit.
    """
    fingerprint = _file_fingerprint(path) if use_cache else None
    cached = _load_cache(path, fingerprint) if use_cache else None

    if cached is not None:
        bh_return = cached["bh_return"]
        total_candle = cached["total_candle"]
        result = cached["result"]
        from_cache = True
    else:
        from_cache = False
        rows = load_csv(path)
        closes = [r['close'] for r in rows]
        open_times = [r['open_time'] for r in rows]
        total_candle = len(rows)

        bh_return = (closes[-1] - closes[0]) / closes[0] * 100

    if verbose:
        cache_note = " [dari cache]" if from_cache else ""
        if HAS_RICH:
            console.print(f"\n[bold cyan]File[/bold cyan]        : {path}{cache_note}")
            console.print(f"[bold cyan]Total candle[/bold cyan]: {total_candle}")
            console.print(f"[bold cyan]Fee[/bold cyan]         : {FEE_PCT}% per sisi ({2*FEE_PCT}% round-trip)")
            console.print(f"[bold cyan]Buy & Hold[/bold cyan]  : {bh_return:.2f}%")
            console.print(f"[bold cyan]MACD[/bold cyan]        : {MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL}")
        else:
            print(f"File        : {path}{cache_note}")
            print(f"Total candle: {total_candle}")
            print(f"Fee         : {FEE_PCT}% per sisi ({2*FEE_PCT}% round-trip)")
            print(f"Buy & Hold  : {bh_return:.2f}%")
            print(f"MACD        : {MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL}")

    if not from_cache:
        result = backtest_macd(closes, MACD_FAST, MACD_SLOW, MACD_SIGNAL, open_times=open_times)

        if result is None:
            if verbose:
                msg = "Data tidak cukup untuk menghasilkan trade (minimal 3 trade closed)."
                console.print(f"[red]{msg}[/red]") if HAS_RICH else print(msg)
            return path, None, bh_return, {"total_candle": total_candle} if collect_detail else None

        if use_cache:
            _save_cache(path, fingerprint, bh_return, result, total_candle)

    if verbose and result is not None:
        sig = _fmt_last_signal(result)
        ringkasan = (f"\n>> MACD {result['fast']}/{result['slow']}/{result['signal']}  "
                     f"Trades={result['n_trades']}  WinRate={result['win_rate']:.1f}%  "
                     f"Return={result['total_return_pct']:.2f}%  MaxDD={result['max_dd_pct']:.2f}%  "
                     f"Calmar={result['calmar']:.2f}  SinyalTerakhir={sig}")
        console.print(f"[bold green]{ringkasan}[/bold green]") if HAS_RICH else print(ringkasan)

    detail = None
    if collect_detail:
        detail = {"total_candle": total_candle}

    return path, result, bh_return, detail


def _md_table(headers, rows):
    """Bangun tabel markdown standar dari header dan list-of-list baris."""
    lines = []
    lines.append("| " + " | ".join(headers) + " |")
    lines.append("|" + "|".join(["---"] * len(headers)) + "|")
    for row in rows:
        lines.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(lines)


def _fmt_pct(val):
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.2f}%"


def _fmt_last_signal_md(r):
    """Format untuk markdown: emoji bulat hijau untuk BUY (masih holding), merah untuk SELL (menunggu beli)."""
    if r.get('days_since_last_signal') is None or r.get('last_signal_type') is None:
        return "-"
    days_label = _days_label(r['days_since_last_signal'])
    sig_type = r['last_signal_type']
    status = "masih holding" if sig_type == "BUY" else "menunggu sinyal beli"
    dot = "🟢" if sig_type == "BUY" else "🔴"
    return f'{dot} **{days_label}** ({sig_type}, {status})'


def generate_markdown_section(summary_with_detail, bullish, bearish, unknown):
    """
    Bangun konten markdown (tanpa header/footer README) dari hasil backtest MACD.
    summary_with_detail: list of (path, result, bh, detail) -- tidak dipakai untuk
    detail per-aset lagi (dihapus), hanya diteruskan untuk kompatibilitas caller.
    bullish, bearish, unknown: hasil split_and_sort_by_signal -- masing-masing
    dirender sebagai satu tabel ringkas, diurutkan dari sinyal paling baru.
    """
    lines = []
    lines.append(f"**Fee yang digunakan:** {FEE_PCT}% per sisi ({2*FEE_PCT}% round-trip)")
    lines.append(f"**Parameter MACD (tetap, semua pair):** `{MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL}`")
    lines.append("")
    lines.append("**Sinyal Terakhir** menunjukkan sudah berapa hari sejak crossover MACD terakhir "
                 "terjadi, dihitung sampai candle paling akhir di data "
                 "(BUY = masih dalam posisi terbuka, SELL = sudah keluar dan menunggu sinyal beli berikutnya). "
                 "Kedua tabel di bawah diurutkan dari sinyal paling baru ke paling lama.")
    lines.append("")

    headers = ["Pair", "Timeframe", "Total Candle",
               "Return", "Max DD", "Buy & Hold", "Trades", "Sinyal Terakhir"]

    def _build_summary_table(group):
        table_rows = []
        for path, result, bh, detail in group:
            pair, tf_label = parse_filename(path)
            candle_count = detail["total_candle"] if detail else "-"
            if result is None:
                table_rows.append([pair, tf_label, candle_count, "-", "-", _fmt_pct(bh), "-", "-"])
            else:
                sig_label = _fmt_last_signal_md(result)
                table_rows.append([
                    f"**{pair}**", tf_label, candle_count,
                    _fmt_pct(result['total_return_pct']),
                    f"{result['max_dd_pct']:.2f}%",
                    _fmt_pct(bh),
                    str(result['n_trades']),
                    sig_label,
                ])
        return _md_table(headers, table_rows)

    if bullish:
        lines.append("## Result -- Bullish (Sinyal BUY)")
        lines.append("")
        lines.append(_build_summary_table(bullish))
        lines.append("")

    if bearish:
        lines.append("## Result -- Bearish (Sinyal SELL)")
        lines.append("")
        lines.append(_build_summary_table(bearish))
        lines.append("")

    if unknown:
        lines.append("## Result -- Data Tidak Cukup / Tanpa Sinyal")
        lines.append("")
        lines.append(_build_summary_table(unknown))
        lines.append("")

    return "\n".join(lines)


README_INTRO = f"""# Hasil Pengujian MACD Crossover ({MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL})

Repositori ini berisi hasil pengujian strategi *MACD crossover* (beli saat garis
MACD memotong ke atas garis sinyal, jual saat memotong ke bawah) pada berbagai
aset kripto, timeframe daily, dengan asumsi fee trading 0,15% per sisi.

Parameter `{MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL}` bersifat **tetap untuk semua pair**
(tidak di-grid-search ulang per aset). Parameter ini dipilih lewat pengujian
yang menguji generalisasi satu setup tunggal lintas 16 pair, tervalidasi melalui
in-sample/out-of-sample split dan walk-forward analysis (expanding window, 5 fold,
tanpa refitting per pair). Setup ini unggul di seluruh metrik walk-forward genuine
dibanding kandidat lain yang diuji, termasuk default klasik 12/26/9.

Karena sudah melalui OOS split dan walk-forward, hasil di bawah ini bukan lagi
murni in-sample -- namun tetap bukan jaminan performa live. Walk-forward genuine
menunjukkan hanya ~52% fold individual yang positif dan ~65% pair yang signifikan
secara statistik (bootstrap p<0,05); artinya edge ada tapi tidak seragam di semua
pair maupun di semua periode. Gunakan sebagai salah satu input keputusan, bukan
sinyal mutlak, dan pertimbangkan manajemen risiko (position sizing, bukan all-in)
terutama pada pair dengan riwayat maximum drawdown dalam.

Data mentah dan script pengujian tersedia untuk diverifikasi/diuji ulang secara
mandiri di [github.com/Rovikin/web/tree/main/chart](https://github.com/Rovikin/web/tree/main/chart).

Tidak ada lagi filter kelayakan (calmar minimum / jumlah trade minimum) -- seluruh
pair yang berhasil diuji ditampilkan apa adanya, termasuk yang trade-nya sedikit.

Data & hasil di bawah ini dihasilkan otomatis oleh `backtest.py` dan diperbarui
setiap kali script dijalankan dengan flag `--detail`.

---

"""

README_OUTRO = f"""

---

_Dihasilkan otomatis oleh `backtest.py`. Metodologi: MACD crossover ({MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL}),
parameter tetap untuk semua pair, long-only, fee dihitung di setiap entry & exit,
tanpa slippage. Divalidasi IS/OOS split + walk-forward expanding window. Data dan
script pengujian: [github.com/Rovikin/web/tree/main/chart](https://github.com/Rovikin/web/tree/main/chart) --
silakan uji ulang secara mandiri._
"""

README_START_MARKER = "<!-- BACKTEST_RESULTS_START -->"
README_END_MARKER = "<!-- BACKTEST_RESULTS_END -->"


def write_readme(summary_with_detail, bullish, bearish, unknown, readme_path="README.md"):
    """
    Tulis/perbarui README.md:
    - Jika belum ada -> buat dengan intro + hasil + outro, dibungkus marker.
    - Jika sudah ada -> ganti HANYA konten di antara marker, pertahankan bagian lain
      yang mungkin sudah ditulis manual oleh pengguna di luar marker.
    """
    body = generate_markdown_section(summary_with_detail, bullish, bearish, unknown)
    wrapped_body = f"{README_START_MARKER}\n\n{body}\n\n{README_END_MARKER}"

    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            existing = f.read()
        if README_START_MARKER in existing and README_END_MARKER in existing:
            pre = existing.split(README_START_MARKER)[0]
            post = existing.split(README_END_MARKER)[1]
            new_content = pre + wrapped_body + post
        else:
            # Belum ada marker -- anggap file lama, tambahkan hasil baru di akhir
            new_content = existing.rstrip() + "\n\n" + wrapped_body + "\n"
    else:
        new_content = README_INTRO + wrapped_body + README_OUTRO

    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return readme_path


def split_and_sort_by_signal(summary):
    """
    Pisahkan hasil jadi dua grup berdasarkan jenis sinyal terakhir:
    - bullish_group: sinyal terakhir BUY (posisi masih terbuka)
    - bearish_group: sinyal terakhir SELL (menunggu sinyal beli berikutnya)
    Item tanpa best/detail (gagal) atau tanpa info sinyal masuk grup 'unknown'.
    Setiap grup diurutkan dari sinyal PALING BARU (hari lebih kecil) ke yang lebih lama.
    """
    bullish, bearish, unknown = [], [], []
    for item in summary:
        path, best, bh, detail = item
        if best is None or best.get('days_since_last_signal') is None:
            unknown.append(item)
        elif best['last_signal_type'] == 'BUY':
            bullish.append(item)
        else:
            bearish.append(item)

    bullish.sort(key=lambda item: item[1]['days_since_last_signal'])
    bearish.sort(key=lambda item: item[1]['days_since_last_signal'])
    return bullish, bearish, unknown


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
            usage = "Cara pakai: python3 backtest.py [<file_csv> ...] [--detail]"
            if HAS_RICH:
                console.print(f"[red]{msg}[/red]")
                console.print(usage)
            else:
                print(msg)
                print(usage)
            sys.exit(1)

    summary = []

    for i, path in enumerate(paths):
        if detail_mode and i > 0:
            (console.rule() if HAS_RICH else print("\n" + "=" * 78 + "\n"))
        p, best, bh, detail = run_one_file(path, verbose=detail_mode, collect_detail=detail_mode, use_cache=use_cache)
        summary.append((p, best, bh, detail))

    if detail_mode:
        if HAS_RICH:
            console.rule("[bold]RINGKASAN -- semua file yang diuji[/bold]")
        else:
            print("\n" + "=" * 78)
            print("RINGKASAN -- semua file yang diuji")
            print("=" * 78)

    bullish, bearish, unknown = split_and_sort_by_signal(summary)

    def _build_rich_table(title, group, border_style):
        table = Table(title=title, box=box.ROUNDED, show_lines=True, title_style="bold magenta", border_style=border_style)
        table.add_column("Pair", style="bold cyan", no_wrap=True)
        table.add_column("Timeframe", style="cyan")
        table.add_column("Return%", justify="right")
        table.add_column("MaxDD%", justify="right", style="red")
        table.add_column("B&H%", justify="right")
        table.add_column("Trades", justify="right")
        table.add_column("Sinyal Terakhir", justify="right")

        for path, best, bh, detail in group:
            pair, tf_label = parse_filename(path)

            if best is None:
                row = [pair, tf_label, "-", "-", f"{bh:.2f}%", "-", "-"]
                table.add_row(*row)
                continue

            return_style = "bold green" if best['total_return_pct'] > 0 else "bold red"
            row = [pair, tf_label,
                f"[{return_style}]{best['total_return_pct']:.2f}%[/{return_style}]",
                f"{best['max_dd_pct']:.2f}%",
                f"{bh:.2f}%",
                str(best['n_trades']),
                _fmt_last_signal_rich(best),
            ]
            table.add_row(*row)
        return table

    def _print_plain_group(title, group):
        print(f"\n{title}")
        for path, best, bh, detail in group:
            pair, tf_label = parse_filename(path)
            if best is None:
                print(f"{pair} Timeframe {tf_label}: (data tidak cukup untuk uji)")
            else:
                sig = _fmt_last_signal(best)
                print(f"{pair} Timeframe {tf_label}: "
                      f"Return {best['total_return_pct']:.2f}%  | MaxDD {best['max_dd_pct']:.2f}%  "
                      f"| Trades {best['n_trades']}  | Sinyal Terakhir {sig}")

    if HAS_RICH:
        console.print()
        if bullish:
            console.print(_build_rich_table("Result -- Bullish (Sinyal BUY, terbaru di atas)", bullish, "green"))
        if bearish:
            console.print()
            console.print(_build_rich_table("Result -- Bearish (Sinyal SELL, terbaru di atas)", bearish, "red"))
        if unknown:
            console.print()
            console.print(_build_rich_table("Result -- Data tidak cukup / tanpa sinyal", unknown, "white"))
    else:
        if bullish:
            _print_plain_group("Result -- Bullish (Sinyal BUY, terbaru di atas):", bullish)
        if bearish:
            _print_plain_group("Result -- Bearish (Sinyal SELL, terbaru di atas):", bearish)
        if unknown:
            _print_plain_group("Result -- Data tidak cukup / tanpa sinyal:", unknown)

    if detail_mode:
        readme_path = write_readme(summary, bullish, bearish, unknown)
        msg = f"\nREADME.md diperbarui: {os.path.abspath(readme_path)}"
        console.print(f"[bold green]{msg}[/bold green]") if HAS_RICH else print(msg)

if __name__ == "__main__":
    main()


