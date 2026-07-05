"""
Optimasi EMA Crossover -- PURE PYTHON, tanpa numpy/pandas.
Mencoba banyak kombinasi fast/slow, lalu menampilkan yang terbaik.
Kompatibel dengan Termux standar tanpa instalasi library tambahan.

Cara pakai:
    python3 backtest.py                          # auto-scan semua .csv di folder ini, ringkasan pendek
    python3 backtest.py --detail                 # auto-scan semua .csv, tampilkan detail penuh + ringkasan
    python3 backtest.py <file_csv>                # satu file, ringkasan pendek
    python3 backtest.py <file_csv> --detail       # satu file, detail penuh
    python3 backtest.py <file_csv_1> <file_csv_2> # banyak file spesifik, ringkasan pendek

Contoh:
    python3 backtest.py
    python3 backtest.py btcusdt_1d.csv ethusdt_1d.csv --detail
"""
import csv
import glob
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

# Grid pencarian -- bisa diubah sesuai kebutuhan
FAST_CANDIDATES = [5, 8, 9, 10, 12, 15, 20, 25, 30, 40]
SLOW_CANDIDATES = [20, 26, 30, 40, 50, 75, 100, 150, 200]

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

def ema_series(closes, span):
    alpha = 2 / (span + 1)
    ema = [closes[0]]
    for price in closes[1:]:
        ema.append(alpha * price + (1 - alpha) * ema[-1])
    return ema

def backtest_dual_ema(closes, fast, slow):
    n = len(closes)
    ema_fast = ema_series(closes, fast)
    ema_slow = ema_series(closes, slow)
    above = [ema_fast[i] > ema_slow[i] for i in range(n)]

    trades = []
    position = None
    entry_price = None

    for i in range(slow, n):
        if position is None and (not above[i-1]) and above[i]:
            position = 'LONG'
            entry_price = closes[i]
        elif position == 'LONG' and above[i-1] and (not above[i]):
            gross = (closes[i] - entry_price) / entry_price * 100
            trades.append(gross - 2 * FEE_PCT)
            position = None

    if position == 'LONG':
        gross = (closes[-1] - entry_price) / entry_price * 100
        trades.append(gross - 2 * FEE_PCT)

    if len(trades) < 3:
        return None

    equity = 1.0
    peak = 1.0
    max_dd = 0.0
    wins = 0

    for pnl in trades:
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

    return {
        'fast': fast, 'slow': slow,
        'n_trades': len(trades),
        'win_rate': win_rate,
        'total_return_pct': total_return,
        'max_dd_pct': max_dd,
        'calmar': calmar,
    }

def run_one_file(path, verbose=True):
    """Jalankan optimasi penuh untuk satu file CSV, return (path, best_result_or_None, bh_return)."""
    rows = load_csv(path)
    closes = [r['close'] for r in rows]

    bh_return = (closes[-1] - closes[0]) / closes[0] * 100

    if verbose:
        if HAS_RICH:
            console.print(f"\n[bold cyan]File[/bold cyan]        : {path}")
            console.print(f"[bold cyan]Total candle[/bold cyan]: {len(rows)}")
            console.print(f"[bold cyan]Fee[/bold cyan]         : {FEE_PCT}% per sisi ({2*FEE_PCT}% round-trip)")
            console.print(f"[bold cyan]Buy & Hold[/bold cyan]  : {bh_return:.2f}%")
            console.print(f"Mencoba {len(FAST_CANDIDATES) * len(SLOW_CANDIDATES)} kombinasi EMA...\n")
        else:
            print(f"File        : {path}")
            print(f"Total candle: {len(rows)}")
            print(f"Fee         : {FEE_PCT}% per sisi ({2*FEE_PCT}% round-trip)")
            print(f"Buy & Hold  : {bh_return:.2f}%")
            print(f"Mencoba {len(FAST_CANDIDATES) * len(SLOW_CANDIDATES)} kombinasi EMA...\n")

    results = []
    for fast in FAST_CANDIDATES:
        for slow in SLOW_CANDIDATES:
            if fast >= slow:
                continue
            r = backtest_dual_ema(closes, fast, slow)
            if r:
                results.append(r)

    if not results:
        if verbose:
            msg = "Tidak ada kombinasi yang menghasilkan trade cukup."
            console.print(f"[red]{msg}[/red]") if HAS_RICH else print(msg)
        return path, None, bh_return

    results.sort(key=lambda x: x['total_return_pct'], reverse=True)

    if verbose:
        if HAS_RICH:
            _print_rich_table("TOP 10 berdasarkan Total Return", results[:10])
            results_calmar = sorted(results, key=lambda x: x['calmar'], reverse=True)
            _print_rich_table("TOP 10 berdasarkan Calmar (risk-adjusted)", results_calmar[:10])
        else:
            print("=== TOP 10 berdasarkan Total Return ===")
            print(f"{'Fast':>5} {'Slow':>5} {'Trades':>7} {'WinRate':>8} {'Return%':>12} {'MaxDD%':>9} {'Calmar':>8}")
            for r in results[:10]:
                print(f"{r['fast']:>5} {r['slow']:>5} {r['n_trades']:>7} {r['win_rate']:>7.1f}% {r['total_return_pct']:>11.2f}% {r['max_dd_pct']:>8.2f}% {r['calmar']:>8.2f}")

            print("\n=== TOP 10 berdasarkan Calmar (risk-adjusted) ===")
            results_calmar = sorted(results, key=lambda x: x['calmar'], reverse=True)
            print(f"{'Fast':>5} {'Slow':>5} {'Trades':>7} {'WinRate':>8} {'Return%':>12} {'MaxDD%':>9} {'Calmar':>8}")
            for r in results_calmar[:10]:
                print(f"{r['fast']:>5} {r['slow']:>5} {r['n_trades']:>7} {r['win_rate']:>7.1f}% {r['total_return_pct']:>11.2f}% {r['max_dd_pct']:>8.2f}% {r['calmar']:>8.2f}")

        best = results[0]
        rekomendasi = f"\n>> Rekomendasi (return tertinggi): EMA {best['fast']}/{best['slow']}"
        console.print(f"[bold green]{rekomendasi}[/bold green]") if HAS_RICH else print(rekomendasi)

    return path, results[0], bh_return


def _print_rich_table(title, rows):
    """Cetak satu tabel rich untuk daftar hasil backtest (dipakai mode --detail)."""
    table = Table(title=title, box=box.SIMPLE_HEAVY, show_lines=False)
    table.add_column("Fast", justify="right", style="cyan")
    table.add_column("Slow", justify="right", style="cyan")
    table.add_column("Trades", justify="right")
    table.add_column("WinRate", justify="right")
    table.add_column("Return%", justify="right")
    table.add_column("MaxDD%", justify="right")
    table.add_column("Calmar", justify="right")

    for r in rows:
        return_style = "green" if r['total_return_pct'] > 0 else "red"
        table.add_row(
            str(r['fast']), str(r['slow']), str(r['n_trades']),
            f"{r['win_rate']:.1f}%",
            f"[{return_style}]{r['total_return_pct']:.2f}%[/{return_style}]",
            f"[red]{r['max_dd_pct']:.2f}%[/red]",
            f"{r['calmar']:.2f}",
        )
    console.print(table)


def main():
    args = sys.argv[1:]
    detail_mode = False
    if "--detail" in args:
        detail_mode = True
        args.remove("--detail")

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
        p, best, bh = run_one_file(path, verbose=detail_mode)
        summary.append((p, best, bh))

    if detail_mode:
        if HAS_RICH:
            console.rule("[bold]RINGKASAN -- semua file yang diuji[/bold]")
        else:
            print("\n" + "=" * 78)
            print("RINGKASAN -- semua file yang diuji")
            print("=" * 78)

    if HAS_RICH:
        table = Table(title="Result", box=box.ROUNDED, show_lines=True, title_style="bold magenta")
        table.add_column("Pair", style="bold cyan", no_wrap=True)
        table.add_column("Timeframe", style="cyan")
        table.add_column("EMA", justify="center", style="yellow")
        table.add_column("Return%", justify="right")
        table.add_column("MaxDD%", justify="right", style="red")
        table.add_column("B&H%", justify="right")
        table.add_column("vs B&H", justify="center")

        for path, best, bh in summary:
            pair, tf_label = parse_filename(path)
            if best is None:
                table.add_row(pair, tf_label, "--/--", "-", "-", f"{bh:.2f}%", "-")
                continue
            return_style = "bold green" if best['total_return_pct'] > 0 else "bold red"
            beats_bh = best['total_return_pct'] > bh
            vs_bh_label = "[green]MENANG[/green]" if beats_bh else "[red]KALAH[/red]"
            table.add_row(
                pair,
                tf_label,
                f"{best['fast']}/{best['slow']}",
                f"[{return_style}]{best['total_return_pct']:.2f}%[/{return_style}]",
                f"{best['max_dd_pct']:.2f}%",
                f"{bh:.2f}%",
                vs_bh_label,
            )
        console.print()
        console.print(table)
    else:
        print("\nResult:")
        for path, best, bh in summary:
            pair, tf_label = parse_filename(path)
            if best is None:
                print(f"{pair} Timeframe {tf_label}: (data tidak cukup untuk uji)")
            else:
                print(f"{pair} Timeframe {tf_label}: EMA {best['fast']}/{best['slow']}  "
                      f"| Return {best['total_return_pct']:.2f}%  | MaxDD {best['max_dd_pct']:.2f}%  | B&H {bh:.2f}%")

if __name__ == "__main__":
    main()


