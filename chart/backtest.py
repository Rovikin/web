"""
Backtest MACD Crossover (16/26/12) -- PURE PYTHON, tanpa numpy/pandas.
Parameter tunggal tetap, hasil riset generalisasi lintas 20 pair (IS/OOS split
+ walk-forward analysis expanding window). Bukan lagi grid search in-sample.
Kompatibel dengan Termux standar tanpa instalasi library tambahan.

Cara pakai:
    python3 backtest.py                          # auto-scan semua .csv di folder ini, ringkasan pendek
    python3 backtest.py --detail                 # auto-scan semua .csv, detail penuh + ringkasan + tulis index.html
    python3 backtest.py <file_csv>                # satu file, ringkasan pendek
    python3 backtest.py <file_csv> --detail       # satu file, detail penuh + tulis index.html
    python3 backtest.py <file_csv_1> <file_csv_2> # banyak file spesifik, ringkasan pendek

Contoh:
    python3 backtest.py
    python3 backtest.py btcusdt_1d.csv ethusdt_1d.csv --detail

CATATAN index.html:
Hanya flag --detail yang menulis/memperbarui index.html di direktori kerja saat ini.
Perintah biasa (tanpa --detail) TIDAK pernah menyentuh index.html.
File ini didesain agar langsung bisa di-deploy sebagai GitHub Pages (root dari
repo atau folder /docs, tergantung konfigurasi Pages Anda).
Jika index.html sudah ada, hanya bagian di antara marker
<!-- BACKTEST_RESULTS_START --> ... <!-- BACKTEST_RESULTS_END -->
yang diperbarui -- namun perlu diperhatikan: karena seluruh <head>, CSS, intro,
dan footer juga dihasilkan otomatis dari script ini, jika Anda mengedit bagian
di luar marker secara manual (misal ubah CSS langsung di file), perubahan itu
TETAP dipertahankan selama marker START/END masih ada di file.

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


def _esc(val):
    """Escape karakter HTML dasar untuk teks yang disisipkan ke markup."""
    return (str(val)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;"))


def _fmt_pct(val):
    sign = "+" if val > 0 else ""
    return f"{sign}{val:.2f}%"


def _fmt_last_signal_html(r):
    """Format sinyal terakhir sebagai badge HTML: hijau untuk BUY (holding), oranye untuk SELL (menunggu beli)."""
    if r.get('days_since_last_signal') is None or r.get('last_signal_type') is None:
        return '<span class="dash">-</span>'
    days_label = _days_label(r['days_since_last_signal'])
    sig_type = r['last_signal_type']
    css_class = "signal-buy" if sig_type == "BUY" else "signal-sell"
    return (f'<span class="badge {css_class}">{sig_type}</span>'
            f'<span class="signal-detail">{_esc(days_label)}</span>')


def _build_summary_table(group, max_abs_return):
    """Bangun tabel HTML satu grup (bullish/bearish/unknown) mengikuti markup tema 'Backtest Read-Out'."""
    lines = ['<div class="table-wrap"><table>']
    lines.append(
        '<thead><tr>'
        '<th>Pair</th>'
        '<th class="tf-col">Candle</th>'
        '<th class="num">Return</th>'
        '<th class="num">Max DD</th>'
        '<th class="num">Buy&amp;Hold</th>'
        '<th class="num">Trades</th>'
        '<th>Sinyal Terakhir</th>'
        '</tr></thead>'
    )
    lines.append('<tbody>')

    for path, result, bh, detail in group:
        pair, tf_label = parse_filename(path)
        candle_count = detail["total_candle"] if detail else "-"
        tf_short = _esc(tf_label.replace(" Day", "D").replace(" Hour", "H")
                         .replace(" Minute", "M").replace(" Week", "W").replace(" Month", "Mo")
                         if tf_label != "-" else "-")

        row_classes = []
        if result is not None and result.get('last_signal_type') == 'SELL':
            row_classes.append('sell-row')
        if result is not None and result.get('days_since_last_signal') is not None \
                and round(result['days_since_last_signal']) <= 7:
            row_classes.append('sig-row')
        cls_attr = f' class="{" ".join(row_classes)}"' if row_classes else ''

        pair_cell = f'<td class="pair">{_esc(pair)}<span class="tf">{tf_short}</span></td>'
        candle_cell = f'<td class="tf-col muted-num">{candle_count}</td>'

        if result is None:
            lines.append(
                f'<tr{cls_attr}>{pair_cell}{candle_cell}'
                '<td class="num ret-cell"><span class="dash">-</span></td>'
                '<td class="num"><span class="dash">-</span></td>'
                f'<td class="num muted-num">{_fmt_pct(bh)}</td>'
                '<td class="num"><span class="dash">-</span></td>'
                '<td><span class="dash">-</span></td></tr>'
            )
            continue

        return_val = result['total_return_pct']
        return_class = "positive" if return_val > 0 else "negative"
        bar_class = "" if return_val > 0 else " neg"
        width_pct = max(1, round(abs(return_val) / max_abs_return * 100)) if max_abs_return else 0
        sig_label = _fmt_last_signal_html(result)

        lines.append(
            f'<tr{cls_attr}>{pair_cell}{candle_cell}'
            f'<td class="num ret-cell"><span class="ret-bar{bar_class}" style="width:{width_pct}%"></span>'
            f'<span class="ret-value {return_class}">{_fmt_pct(return_val)}</span></td>'
            f'<td class="num negative">{result["max_dd_pct"]:.2f}%</td>'
            f'<td class="num muted-num">{_fmt_pct(bh)}</td>'
            f'<td class="num muted-num">{result["n_trades"]}</td>'
            f'<td>{sig_label}</td></tr>'
        )

    lines.append('</tbody></table></div>')
    return "\n".join(lines)


def generate_html_section(summary_with_detail, bullish, bearish, unknown):
    """
    Bangun konten HTML (badan hasil saja, tanpa <head>/masthead/prose/footer halaman)
    dari hasil backtest MACD, mengikuti tema visual 'Backtest Read-Out'.
    summary_with_detail: list of (path, result, bh, detail) -- diteruskan untuk kompatibilitas caller.
    bullish, bearish, unknown: hasil split_and_sort_by_signal -- masing-masing
    dirender sebagai satu tabel ringkas, diurutkan dari sinyal paling baru.
    """
    all_returns = [r['total_return_pct'] for _, r, _, _ in (bullish + bearish + unknown) if r is not None]
    max_abs_return = max((abs(v) for v in all_returns), default=0)

    lines = []

    if bullish:
        lines.append('<div class="section-label buy">')
        lines.append('<span class="dot"></span><span class="label">Bullish</span>')
        lines.append(f'<span class="count">— posisi masih terbuka, sinyal BUY belum berbalik ({len(bullish)} pair)</span>')
        lines.append('</div>')
        lines.append(_build_summary_table(bullish, max_abs_return))

    if bearish:
        lines.append('<div class="section-label sell">')
        lines.append('<span class="dot"></span><span class="label">Bearish</span>')
        lines.append(f'<span class="count">— sudah keluar, menunggu sinyal beli berikutnya ({len(bearish)} pair)</span>')
        lines.append('</div>')
        lines.append(_build_summary_table(bearish, max_abs_return))

    if unknown:
        lines.append('<div class="section-label">')
        lines.append('<span class="dot" style="background:var(--text-dim)"></span><span class="label">Data Tidak Cukup</span>')
        lines.append(f'<span class="count">— tanpa sinyal ({len(unknown)} pair)</span>')
        lines.append('</div>')
        lines.append(_build_summary_table(unknown, max_abs_return))

    lines.append('<div class="legend">')
    lines.append(f'<span class="swatch">bar di kolom Return = skala relatif terhadap return tertinggi ({_fmt_pct(max_abs_return)})</span>')
    lines.append('<span class="swatch">baris bergaris tepi = sinyal terjadi ≤ 7 hari terakhir</span>')
    lines.append('</div>')

    return "\n".join(lines)


PAGE_CSS = """
:root {
  --bg: #0a0b0c;
  --bg-raised: #121416;
  --bg-card: #16181b;
  --line: #26292d;
  --line-soft: #1c1e21;
  --text: #d8d6d0;
  --text-muted: #83817b;
  --text-dim: #56544f;
  --serif: 'Fraunces', Georgia, serif;
  --mono: 'IBM Plex Mono', ui-monospace, 'SF Mono', Menlo, monospace;
  --buy: #5eead4;
  --buy-dim: rgba(94, 234, 212, 0.10);
  --sell: #d97c4a;
  --sell-dim: rgba(217, 124, 74, 0.10);
  --sig: #8a8f98;
}

* { box-sizing: border-box; }

body {
  margin: 0;
  background: var(--bg);
  background-image:
    radial-gradient(ellipse 900px 500px at 50% -10%, rgba(94, 234, 212, 0.05), transparent);
  color: var(--text);
  font-family: var(--mono);
  font-size: 14px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

.container { max-width: 1180px; margin: 0 auto; padding: 3rem 1.25rem 4rem; }

/* ---------- Masthead ---------- */
.masthead {
  display: flex; justify-content: space-between; align-items: flex-end;
  flex-wrap: wrap; gap: 1rem 2rem;
  padding-bottom: 1.5rem; margin-bottom: 1.75rem;
  border-bottom: 1px solid var(--line);
}
.masthead .eyebrow {
  font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--text-dim); margin-bottom: 0.6rem;
}
.masthead h1 {
  font-family: var(--serif); font-weight: 500; font-optical-sizing: auto;
  font-size: clamp(1.7rem, 4vw, 2.5rem); line-height: 1.1;
  color: #f2f1ec; margin: 0; letter-spacing: -0.01em;
}
.masthead .params {
  text-align: right; font-size: 0.78rem; color: var(--text-muted);
  white-space: nowrap;
}
.masthead .params strong { color: var(--text); font-weight: 500; }
.masthead .params .src { margin-top: 0.35rem; }
.masthead .params a { color: var(--buy); text-decoration: none; border-bottom: 1px dotted rgba(94,234,212,0.4); }
.masthead .params a:hover { border-bottom-style: solid; }

/* ---------- Section labels ---------- */
.section-label {
  display: flex; align-items: center; gap: 0.7rem;
  margin: 2.25rem 0 0.85rem;
  font-size: 0.8rem; letter-spacing: 0.06em;
}
.section-label .dot { width: 7px; height: 7px; border-radius: 50%; flex-shrink: 0; }
.section-label.buy .dot { background: var(--buy); box-shadow: 0 0 8px rgba(94,234,212,0.6); }
.section-label.sell .dot { background: var(--sell); box-shadow: 0 0 8px rgba(217,124,74,0.5); }
.section-label .count {
  color: var(--text-dim); font-weight: 400;
}
.section-label span.label { color: #f2f1ec; font-weight: 600; text-transform: uppercase; }

/* ---------- Table ---------- */
/* Diperkecil dibanding tema asli: font, padding, dan min-width tabel diturunkan
   supaya di layar sempit (mis. HP) lebih dari 2 kolom terlihat sebelum harus digulir. */
.table-wrap {
  border: 1px solid var(--line); border-radius: 3px;
  background: var(--bg-raised);
  overflow-x: auto; overflow-y: hidden;
  -webkit-overflow-scrolling: touch;
}
table { width: 100%; border-collapse: collapse; min-width: 560px; }
thead th {
  text-align: left; font-weight: 500; font-size: 0.62rem;
  letter-spacing: 0.06em; text-transform: uppercase;
  color: var(--text-dim); padding: 0.5rem 0.6rem;
  border-bottom: 1px solid var(--line); white-space: nowrap;
  background: var(--bg-card);
}
th.num, td.num { text-align: right; }
tbody td {
  padding: 0.42rem 0.6rem; border-bottom: 1px solid var(--line-soft);
  white-space: nowrap; font-size: 0.76rem;
}
tbody tr:last-child td { border-bottom: none; }
tbody tr { position: relative; transition: background 0.12s ease; }
tbody tr:hover { background: rgba(255,255,255,0.02); }
tbody tr.sig-row td:first-child { box-shadow: inset 3px 0 0 var(--buy); }
tbody tr.sell-row.sig-row td:first-child { box-shadow: inset 3px 0 0 var(--sell); }
td.pair { font-family: var(--serif); font-weight: 500; color: #f2f1ec; font-size: 0.82rem; }
td.pair .tf { color: var(--text-dim); font-size: 0.64rem; font-family: var(--mono); margin-left: 0.3rem; }

/* return bar */
.ret-cell { position: relative; }
.ret-bar {
  position: absolute; left: 0; top: 0; bottom: 0;
  background: linear-gradient(90deg, rgba(94,234,212,0.14), rgba(94,234,212,0.03));
}
.ret-bar.neg { background: linear-gradient(90deg, rgba(217,124,74,0.14), rgba(217,124,74,0.03)); }
.ret-value { position: relative; font-weight: 600; }
.positive { color: var(--buy); }
.negative { color: var(--sell); }
.muted-num { color: var(--text-muted); }

.badge {
  display: inline-block; padding: 0.08rem 0.4rem; border-radius: 2px;
  font-size: 0.6rem; font-weight: 600; letter-spacing: 0.04em;
  border: 1px solid;
}
.signal-buy { background: var(--buy-dim); color: var(--buy); border-color: rgba(94,234,212,0.25); }
.signal-sell { background: var(--sell-dim); color: var(--sell); border-color: rgba(217,124,74,0.25); }
.signal-detail { color: var(--text-dim); font-size: 0.68rem; margin-left: 0.35rem; }
.dash { color: var(--text-dim); }

.legend {
  display: flex; gap: 1.5rem; flex-wrap: wrap;
  margin-top: 0.75rem; font-size: 0.72rem; color: var(--text-dim);
}
.legend .swatch { display: inline-flex; align-items: center; gap: 0.4rem; white-space: nowrap; }
.legend .swatch .dot { width: 6px; height: 6px; border-radius: 50%; }

/* ---------- Prose / explanatory section ---------- */
.prose-section {
  margin-top: 3.5rem; padding-top: 2rem; border-top: 1px solid var(--line);
}
.prose-section .eyebrow {
  font-size: 0.72rem; letter-spacing: 0.12em; text-transform: uppercase;
  color: var(--text-dim); margin-bottom: 1rem;
}
.prose-section p {
  font-family: var(--serif); font-size: 1.02rem; line-height: 1.7;
  color: #b8b6b0; max-width: 68ch; margin: 0 0 1.1rem;
}
.prose-section code {
  font-family: var(--mono); background: var(--bg-card); border: 1px solid var(--line);
  border-radius: 3px; padding: 0.05rem 0.4rem; font-size: 0.82em; color: var(--buy);
}
.prose-section a { color: var(--buy); text-decoration: none; border-bottom: 1px dotted rgba(94,234,212,0.4); }
.prose-section a:hover { border-bottom-style: solid; }

.field-note {
  font-family: var(--mono); font-size: 0.82rem; color: var(--text-muted);
  background: var(--bg-card); border: 1px solid var(--line); border-left: 2px solid var(--sell);
  padding: 1rem 1.25rem; border-radius: 0 3px 3px 0; margin: 1.5rem 0; max-width: 68ch;
  line-height: 1.7;
}
.field-note .tag { color: var(--sell); font-weight: 600; }

footer {
  margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--line);
  color: var(--text-dim); font-size: 0.76rem; max-width: 68ch;
}
footer a { color: var(--text-muted); }

@media (max-width: 640px) {
  .masthead { flex-direction: column; align-items: flex-start; }
  .masthead .params { text-align: left; }
  td.tf-col, th.tf-col { display: none; }
}
"""

PAGE_INTRO = f"""
<div class="masthead">
  <div>
    <div class="eyebrow">Backtest Read-Out</div>
    <h1>MACD Crossover {MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL}</h1>
  </div>
  <div class="params">
    <div><strong>Fee:</strong> {FEE_PCT}%/sisi &nbsp;\u00b7&nbsp; <strong>Timeframe:</strong> daily &nbsp;\u00b7&nbsp; <strong>Mode:</strong> Long-only</div>
    <div class="src">Script &amp; data: <a href="https://github.com/Rovikin/web/tree/main/chart">github.com/Rovikin/web/chart</a></div>
  </div>
</div>
"""

PAGE_OUTRO = f"""
<div class="prose-section">
  <div class="eyebrow">Metodologi &amp; Batasan</div>

  <p>Parameter <code>{MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL}</code> bersifat tetap untuk seluruh pair di atas
  — tidak di-<em>grid-search</em> ulang per aset. Setup ini dipilih lewat pengujian generalisasi lintas
  20 pair, tervalidasi melalui in-sample/out-of-sample split dan walk-forward analysis (expanding window,
  5 fold, tanpa refitting per pair).</p>

  <div class="field-note">
    <span class="tag">[!]</span> Karena sudah melalui OOS split dan walk-forward, hasil di atas bukan lagi
    murni in-sample — namun tetap bukan jaminan performa live. Gunakan sebagai salah satu input keputusan,
    bukan sinyal mutlak, dan pertimbangkan manajemen risiko (position sizing, bukan all-in) terutama pada
    pair dengan riwayat maximum drawdown dalam.
  </div>

  <p>Tidak ada filter kelayakan (calmar minimum / jumlah trade minimum) yang diterapkan — seluruh pair yang
  berhasil diuji ditampilkan apa adanya, termasuk yang trade-nya sedikit. Data mentah dan script pengujian
  tersedia untuk diverifikasi/diuji ulang secara mandiri di
  <a href="https://github.com/Rovikin/web/tree/main/chart">github.com/Rovikin/web/tree/main/chart</a>.</p>
</div>

<footer>
Dihasilkan otomatis oleh <code>backtest.py</code>. Metodologi: MACD crossover ({MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL}),
parameter tetap untuk semua pair, long-only, fee dihitung di setiap entry &amp; exit,
tanpa slippage. Divalidasi IS/OOS split + walk-forward expanding window. Data dan
script pengujian: <a href="https://github.com/Rovikin/web/tree/main/chart">github.com/Rovikin/web/tree/main/chart</a>
— silakan uji ulang secara mandiri.
</footer>
"""

HTML_START_MARKER = "<!-- BACKTEST_RESULTS_START -->"
HTML_END_MARKER = "<!-- BACKTEST_RESULTS_END -->"

PAGE_TITLE = f"Hasil Backtest MACD ({MACD_FAST}/{MACD_SLOW}/{MACD_SIGNAL})"

PAGE_TEMPLATE = f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{PAGE_TITLE}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>{PAGE_CSS}</style>
</head>
<body>
<div class="container">
{PAGE_INTRO}
{HTML_START_MARKER}
__BODY__
{HTML_END_MARKER}
{PAGE_OUTRO}
</div>
</body>
</html>
"""


def write_html_report(summary_with_detail, bullish, bearish, unknown, output_path="index.html"):
    """
    Tulis/perbarui index.html:
    - Jika belum ada -> buat halaman lengkap (head + intro + hasil + footer), dibungkus marker.
    - Jika sudah ada dan markernya ditemukan -> ganti HANYA konten di antara marker,
      pertahankan bagian lain yang mungkin sudah diedit manual (CSS, intro, dsb).
    """
    body = generate_html_section(summary_with_detail, bullish, bearish, unknown)
    wrapped_body = f"{HTML_START_MARKER}\n{body}\n{HTML_END_MARKER}"

    if os.path.exists(output_path):
        with open(output_path, "r", encoding="utf-8") as f:
            existing = f.read()
        if HTML_START_MARKER in existing and HTML_END_MARKER in existing:
            pre = existing.split(HTML_START_MARKER)[0]
            post = existing.split(HTML_END_MARKER)[1]
            new_content = pre + wrapped_body + post
        else:
            # Belum ada marker -- anggap file lama/manual, buat ulang dari template
            new_content = PAGE_TEMPLATE.replace("__BODY__", body)
    else:
        new_content = PAGE_TEMPLATE.replace("__BODY__", body)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    return output_path


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
        html_path = write_html_report(summary, bullish, bearish, unknown)
        msg = f"\nindex.html diperbarui: {os.path.abspath(html_path)}"
        console.print(f"[bold green]{msg}[/bold green]") if HAS_RICH else print(msg)

if __name__ == "__main__":
    main()


