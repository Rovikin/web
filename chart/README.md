# Hasil Pengujian EMA Crossover

Repositori ini berisi hasil pengujian sistematis strategi *dual EMA crossover*
(beli saat EMA cepat memotong ke atas EMA lambat, jual saat memotong ke bawah)
pada berbagai aset kripto, timeframe daily, dengan asumsi fee trading 0,15% per sisi.

Pengujian dilakukan dengan grid search murni (mencoba banyak kombinasi EMA fast/slow),
mengambil kombinasi dengan return tertinggi sebagai representasi tiap aset. Hasil ini
bersifat in-sample (belum divalidasi walk-forward out-of-sample) kecuali disebutkan lain,
sehingga sebaiknya tidak dijadikan dasar tunggal untuk keputusan trading nyata.

Data & hasil di bawah ini dihasilkan otomatis oleh `backtest.py` dan diperbarui
setiap kali script dijalankan dengan flag `--detail`.

---

<!-- BACKTEST_RESULTS_START -->

**Fee yang digunakan:** 0.15% per sisi (0.3% round-trip)
**Parameter MACD (tetap, semua pair):** `16/26/12`

**Sinyal Terakhir** menunjukkan sudah berapa hari sejak crossover MACD terakhir terjadi, dihitung sampai candle paling akhir di data (BUY = masih dalam posisi terbuka, SELL = sudah keluar dan menunggu sinyal beli berikutnya). Kedua tabel di bawah diurutkan dari sinyal paling baru ke paling lama.

## Result -- Bullish (Sinyal BUY)

| Pair | Timeframe | Total Candle | Return | Max DD | Buy & Hold | Trades | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| **BNBUSDT** | 1 Day | 3167 | +1655.47% | -47.34% | +36097.33% | 86 | 🟢 **4 hari lalu** (BUY, masih holding) |
| **HBARUSDT** | 1 Day | 2475 | +206.94% | -90.50% | +95.05% | 77 | 🟢 **4 hari lalu** (BUY, masih holding) |
| **DOGEUSDT** | 1 Day | 2561 | +3051.64% | -73.14% | +1771.53% | 65 | 🟢 **5 hari lalu** (BUY, masih holding) |
| **ZECUSDT** | 1 Day | 2667 | +2743.66% | -79.91% | +745.10% | 74 | 🟢 **5 hari lalu** (BUY, masih holding) |
| **LINKUSDT** | 1 Day | 2731 | +2553.02% | -67.71% | +1460.98% | 81 | 🟢 **6 hari lalu** (BUY, masih holding) |
| **PAXGUSDT** | 1 Day | 2141 | +20.24% | -16.37% | +105.92% | 70 | 🟢 **6 hari lalu** (BUY, masih holding) |
| **XMRUSD** | 1 Day | 725 | +109.16% | -13.14% | +99.97% | 20 | 🟢 **6 hari lalu** (BUY, masih holding) |
| **XRPUSDT** | 1 Day | 2988 | +3924.89% | -55.54% | +22.58% | 78 | 🟢 **6 hari lalu** (BUY, masih holding) |
| **AVAXUSDT** | 1 Day | 2116 | +1739.44% | -73.10% | +21.73% | 54 | 🟢 **15 hari lalu** (BUY, masih holding) |
| **TRXUSDT** | 1 Day | 2950 | +440.55% | -74.68% | +578.72% | 91 | 🟢 **17 hari lalu** (BUY, masih holding) |
| **ADAUSDT** | 1 Day | 3005 | +1331.55% | -79.87% | -31.12% | 81 | 🟢 **21 hari lalu** (BUY, masih holding) |
| **SUIUSDT** | 1 Day | 1163 | -61.33% | -69.68% | -49.27% | 36 | 🟢 **22 hari lalu** (BUY, masih holding) |
| **BCHUSDT** | 1 Day | 2415 | -12.65% | -81.17% | +8.27% | 78 | 🟢 **23 hari lalu** (BUY, masih holding) |
| **BTCUSDT** | 1 Day | 3248 | +4143.00% | -54.75% | +1353.65% | 92 | 🟢 **23 hari lalu** (BUY, masih holding) |
| **ETHUSDT** | 1 Day | 3248 | +2711.25% | -59.34% | +477.33% | 91 | 🟢 **23 hari lalu** (BUY, masih holding) |
| **LTCUSDT** | 1 Day | 3130 | -87.40% | -90.68% | -84.95% | 97 | 🟢 **23 hari lalu** (BUY, masih holding) |
| **SOLUSDT** | 1 Day | 2158 | +15198.77% | -69.89% | +2259.56% | 54 | 🟢 **23 hari lalu** (BUY, masih holding) |
| **UNIUSDT** | 1 Day | 2121 | -21.65% | -89.26% | -5.25% | 66 | 🟢 **23 hari lalu** (BUY, masih holding) |

## Result -- Bearish (Sinyal SELL)

| Pair | Timeframe | Total Candle | Return | Max DD | Buy & Hold | Trades | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| **NEARUSDT** | 1 Day | 2094 | +376.01% | -68.88% | +61.92% | 60 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| **XLMUSDT** | 1 Day | 2961 | +451.92% | -70.84% | -38.68% | 86 | 🔴 **1 hari lalu** (SELL, menunggu sinyal beli) |


<!-- BACKTEST_RESULTS_END -->

---

_Dihasilkan otomatis oleh `backtest.py`. Metodologi: dual EMA crossover, long-only,
fee dihitung di setiap entry & exit, tanpa slippage. Hasil in-sample murni --
lihat catatan walk-forward terpisah untuk validasi out-of-sample._
