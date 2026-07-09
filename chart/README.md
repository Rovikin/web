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
**Grid EMA yang diuji:** fast [5, 8, 9, 10, 12, 15, 20, 25, 30, 40] x slow [20, 26, 30, 40, 50, 75, 100, 150, 200]

**Sinyal Terakhir** menunjukkan sudah berapa hari sejak crossover EMA terakhir terjadi pada kombinasi tersebut, dihitung sampai candle paling akhir di data (BUY = masih dalam posisi terbuka, SELL = sudah keluar dan menunggu sinyal beli berikutnya). Kedua tabel di bawah diurutkan dari sinyal paling baru ke paling lama.

## Ringkasan Hasil -- Bullish (Sinyal BUY)

| Pair | Timeframe | Total Candle | EMA Terbaik | Return | Max DD | Buy & Hold | Calmar Rank | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|---|
| **ZECUSDT** | 1 Day | 2667 | `9/20` | +5762.05% | -51.62% | +745.10% | ✅ #8 | 🟢 **2 hari lalu** (BUY, masih holding) |
| **ETHUSDT** | 1 Day | 3248 | `10/20` | +7013.99% | -46.34% | +477.33% | ✅ #5 | 🟢 **3 hari lalu** (BUY, masih holding) |
| **UNIUSDT** | 1 Day | 2121 | `25/26` | +1328.06% | -35.67% | -5.25% | ⚠️ #10 | 🟢 **3 hari lalu** (BUY, masih holding) |
| **SOLUSDT** | 1 Day | 2158 | `9/26` | +18559.89% | -44.22% | +2259.56% | ✅ #2 | 🟢 **7 hari lalu** (BUY, masih holding) |

## Ringkasan Hasil -- Bearish (Sinyal SELL)

| Pair | Timeframe | Total Candle | EMA Terbaik | Return | Max DD | Buy & Hold | Calmar Rank | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|---|
| **XLMUSDT** | 1 Day | 2961 | `5/30` | +362.01% | -66.34% | -38.68% | ⛔ #17 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| **NEARUSDT** | 1 Day | 2094 | `5/26` | +1196.44% | -72.03% | +61.92% | ⚠️ #13 | 🔴 **16 hari lalu** (SELL, menunggu sinyal beli) |
| **BNBUSDT** | 1 Day | 3167 | `10/26` | +30822.68% | -31.91% | +36097.33% | ✅ #1 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| **HBARUSDT** | 1 Day | 2475 | `12/30` | +5226.36% | -34.93% | +95.05% | ✅ #6 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| **TRXUSDT** | 1 Day | 2950 | `12/30` | +1222.82% | -43.96% | +578.72% | ⚠️ #11 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| **DOGEUSDT** | 1 Day | 2561 | `25/30` | +17991.17% | -52.04% | +1771.53% | ✅ #3 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| **SUIUSDT** | 1 Day | 1163 | `5/26` | +408.00% | -50.43% | -49.27% | ⛔ #16 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| **XMRUSD** | 1 Day | 725 | `9/20` | +105.86% | -9.53% | +99.97% | ⚠️ #15 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| **BTCUSDT** | 1 Day | 3248 | `10/30` | +6804.41% | -52.55% | +1353.65% | ✅ #7 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| **ADAUSDT** | 1 Day | 3005 | `15/40` | +9390.82% | -34.42% | -31.12% | ✅ #4 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| **LTCUSDT** | 1 Day | 3130 | `15/40` | +209.25% | -56.14% | -84.95% | ⛔ #18 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| **LINKUSDT** | 1 Day | 2731 | `5/100` | +1614.49% | -71.67% | +1460.98% | ⚠️ #12 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| **PAXGUSDT** | 1 Day | 2141 | `10/40` | +103.60% | -7.56% | +105.92% | ⚠️ #14 | 🔴 **78 hari lalu** (SELL, menunggu sinyal beli) |
| **BCHUSDT** | 1 Day | 2415 | `9/100` | +165.26% | -55.04% | +8.27% | ⛔ #19 | 🔴 **158 hari lalu** (SELL, menunggu sinyal beli) |
| **XRPUSDT** | 1 Day | 2988 | `9/200` | +99.26% | -50.56% | +22.58% | ⛔ #20 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| **AVAXUSDT** | 1 Day | 2116 | `9/100` | +2538.89% | -43.16% | +21.73% | ✅ #9 | 🔴 **269 hari lalu** (SELL, menunggu sinyal beli) |

## Detail per Aset

### ADAUSDT (1 Day)

- **File sumber:** `adausdt_1d.csv`
- **Total candle:** 3005
- **Buy & Hold:** -31.12%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `15/40` → Return +9390.82%, MaxDD -34.42%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **48 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 25 | 40.0% | +9390.82% | -34.42% | 272.84 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 40 | 23 | 39.1% | +7843.51% | -38.26% | 205.03 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 21 | 42.9% | +7288.51% | -35.55% | 205.01 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 25 | 40.0% | +7048.53% | -32.34% | 217.92 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 32 | 37.5% | +6974.95% | -41.99% | 166.12 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 23 | 39.1% | +6464.02% | -42.21% | 153.15 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 20 | 50.0% | +6346.56% | -41.09% | 154.45 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 75 | 26 | 46.2% | +6326.46% | -46.12% | 137.18 | 🔴 **54 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 29 | 37.9% | +6315.59% | -44.41% | 142.22 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 26 | 38.5% | +6309.51% | -37.53% | 168.10 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 25 | 40.0% | +9390.82% | -34.42% | 272.84 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 25 | 40.0% | +7048.53% | -32.34% | 217.92 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 40 | 23 | 39.1% | +7843.51% | -38.26% | 205.03 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 21 | 42.9% | +7288.51% | -35.55% | 205.01 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 75 | 14 | 50.0% | +5778.85% | -30.69% | 188.28 | 🔴 **271 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 26 | 38.5% | +6309.51% | -37.53% | 168.10 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 32 | 37.5% | +6974.95% | -41.99% | 166.12 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 20 | 50.0% | +6346.56% | -41.09% | 154.45 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 23 | 39.1% | +6464.02% | -42.21% | 153.15 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 50 | 33 | 36.4% | +5800.66% | -39.13% | 148.24 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |

### AVAXUSDT (1 Day)

- **File sumber:** `avaxusdt_1d.csv`
- **Total candle:** 2116
- **Buy & Hold:** +21.73%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `9/100` → Return +2538.89%, MaxDD -43.16%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **269 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 75 | 13 | 38.5% | +3356.67% | -33.05% | 101.58 | 🔴 **54 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 15 | 26.7% | +2538.89% | -43.16% | 58.83 | 🔴 **269 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 100 | 14 | 28.6% | +2363.80% | -41.18% | 57.40 | 🔴 **269 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 14 | 28.6% | +2309.05% | -42.99% | 53.71 | 🔴 **53 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 52 | 23.1% | +2258.54% | -59.69% | 37.84 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 12 | 20 | 37 | 29.7% | +2145.24% | -63.60% | 33.73 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 50 | 15 | 33.3% | +2017.64% | -42.82% | 47.12 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 33 | 30.3% | +1977.83% | -66.26% | 29.85 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 75 | 23 | 26.1% | +1976.25% | -59.84% | 33.02 | 🔴 **53 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 40 | 27.5% | +1973.39% | -61.06% | 32.32 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 75 | 13 | 38.5% | +3356.67% | -33.05% | 101.58 | 🔴 **54 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 75 | 10 | 40.0% | +1857.34% | -29.37% | 63.24 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 15 | 26.7% | +2538.89% | -43.16% | 58.83 | 🔴 **269 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 100 | 14 | 28.6% | +2363.80% | -41.18% | 57.40 | 🔴 **269 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 14 | 28.6% | +2309.05% | -42.99% | 53.71 | 🔴 **53 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 50 | 15 | 33.3% | +2017.64% | -42.82% | 47.12 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 100 | 13 | 30.8% | +1540.88% | -36.86% | 41.80 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 100 | 17 | 23.5% | +1687.99% | -43.06% | 39.20 | 🔴 **270 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 10 | 40.0% | +1252.96% | -32.01% | 39.14 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 40 | 13 | 30.8% | +1864.53% | -49.06% | 38.00 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |

### BCHUSDT (1 Day)

- **File sumber:** `bchusdt_1d.csv`
- **Total candle:** 2415
- **Buy & Hold:** +8.27%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `9/100` → Return +165.26%, MaxDD -55.04%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **158 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 75 | 14 | 35.7% | +200.06% | -55.10% | 3.63 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 75 | 11 | 36.4% | +184.31% | -45.26% | 4.07 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 19 | 31.6% | +165.26% | -55.04% | 3.00 | 🔴 **158 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 100 | 12 | 41.7% | +161.33% | -37.10% | 4.35 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 100 | 23 | 30.4% | +141.62% | -50.68% | 2.79 | 🔴 **158 hari lalu** (SELL, menunggu sinyal beli) |
| 40 | 50 | 14 | 35.7% | +139.55% | -53.22% | 2.62 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 100 | 16 | 31.2% | +109.75% | -59.95% | 1.83 | 🔴 **158 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 68 | 29.4% | +108.89% | -66.39% | 1.64 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 15 | 100 | 15 | 33.3% | +101.19% | -61.63% | 1.64 | 🔴 **157 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 22 | 31.8% | +100.11% | -58.51% | 1.71 | 🔴 **159 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 20 | 100 | 12 | 41.7% | +161.33% | -37.10% | 4.35 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 75 | 11 | 36.4% | +184.31% | -45.26% | 4.07 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 14 | 35.7% | +200.06% | -55.10% | 3.63 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 19 | 31.6% | +165.26% | -55.04% | 3.00 | 🔴 **158 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 100 | 23 | 30.4% | +141.62% | -50.68% | 2.79 | 🔴 **158 hari lalu** (SELL, menunggu sinyal beli) |
| 40 | 50 | 14 | 35.7% | +139.55% | -53.22% | 2.62 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 100 | 16 | 31.2% | +109.75% | -59.95% | 1.83 | 🔴 **158 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 22 | 31.8% | +100.11% | -58.51% | 1.71 | 🔴 **159 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 39 | 30.8% | +96.49% | -56.65% | 1.70 | 🔴 **57 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 150 | 23 | 17.4% | +76.82% | -46.67% | 1.65 | 🔴 **135 hari lalu** (SELL, menunggu sinyal beli) |

### BNBUSDT (1 Day)

- **File sumber:** `bnbusdt_1d.csv`
- **Total candle:** 3167
- **Buy & Hold:** +36097.33%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `10/26` → Return +30822.68%, MaxDD -31.91%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **34 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 26 | 46 | 45.7% | +30822.68% | -31.91% | 965.85 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 34 | 47.1% | +27733.76% | -36.73% | 755.10 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 46 | 45.7% | +26606.06% | -35.84% | 742.35 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 35 | 48.6% | +24534.25% | -36.09% | 679.71 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 41 | 46.3% | +21283.08% | -33.21% | 640.81 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 43 | 48.8% | +21137.95% | -33.13% | 638.01 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 52 | 42.3% | +20012.75% | -38.95% | 513.87 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 40 | 37 | 40.5% | +19337.91% | -43.36% | 446.01 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 47 | 46.8% | +19326.85% | -29.22% | 661.39 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 34 | 38.2% | +19029.96% | -41.94% | 453.74 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 26 | 46 | 45.7% | +30822.68% | -31.91% | 965.85 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 34 | 47.1% | +27733.76% | -36.73% | 755.10 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 46 | 45.7% | +26606.06% | -35.84% | 742.35 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 35 | 48.6% | +24534.25% | -36.09% | 679.71 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 47 | 46.8% | +19326.85% | -29.22% | 661.39 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 41 | 46.3% | +21283.08% | -33.21% | 640.81 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 43 | 48.8% | +21137.95% | -33.13% | 638.01 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 35 | 40.0% | +18432.73% | -30.15% | 611.40 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 52 | 42.3% | +20012.75% | -38.95% | 513.87 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 34 | 35.3% | +14590.54% | -30.30% | 481.60 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |

### BTCUSDT (1 Day)

- **File sumber:** `btcusdt_1d.csv`
- **Total candle:** 3248
- **Buy & Hold:** +1353.65%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `10/30` → Return +6804.41%, MaxDD -52.55%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **47 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 30 | 44 | 38.6% | +6804.41% | -52.55% | 129.48 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 51 | 35.3% | +5336.21% | -51.68% | 103.26 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 47 | 36.2% | +4361.34% | -53.73% | 81.17 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 54 | 35.2% | +4300.59% | -57.97% | 74.19 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 58 | 34.5% | +4205.05% | -50.07% | 83.99 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 51 | 33.3% | +4198.99% | -54.14% | 77.56 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 48 | 35.4% | +4156.22% | -53.26% | 78.04 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 26 | 42.3% | +4052.75% | -38.87% | 104.28 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 42 | 38.1% | +3858.53% | -48.75% | 79.14 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 63 | 34.9% | +3828.81% | -61.34% | 62.42 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 30 | 44 | 38.6% | +6804.41% | -52.55% | 129.48 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 26 | 42.3% | +4052.75% | -38.87% | 104.28 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 51 | 35.3% | +5336.21% | -51.68% | 103.26 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 50 | 23 | 43.5% | +3513.43% | -35.28% | 99.58 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 50 | 23 | 39.1% | +3002.00% | -34.93% | 85.95 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 58 | 34.5% | +4205.05% | -50.07% | 83.99 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 47 | 36.2% | +4361.34% | -53.73% | 81.17 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 50 | 25 | 40.0% | +3192.44% | -39.95% | 79.90 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 42 | 38.1% | +3858.53% | -48.75% | 79.14 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 48 | 35.4% | +4156.22% | -53.26% | 78.04 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |

### DOGEUSDT (1 Day)

- **File sumber:** `dogeusdt_1d.csv`
- **Total candle:** 2561
- **Buy & Hold:** +1771.53%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `25/30` → Return +17991.17%, MaxDD -52.04%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **38 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 26 | 30 | 36.7% | +18176.70% | -56.62% | 321.00 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 23 | 34.8% | +17991.17% | -52.04% | 345.72 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 46 | 34.8% | +16696.92% | -60.88% | 274.27 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 26 | 42.3% | +16563.15% | -61.03% | 271.40 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 34 | 35.3% | +15384.36% | -56.27% | 273.41 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 36 | 38.9% | +15257.06% | -56.74% | 268.92 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 35 | 37.1% | +14712.45% | -54.26% | 271.13 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 50 | 36 | 33.3% | +14527.90% | -56.75% | 256.01 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 33 | 36.4% | +14293.26% | -58.29% | 245.19 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 26 | 34.6% | +14266.58% | -62.14% | 229.60 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 30 | 23 | 34.8% | +17991.17% | -52.04% | 345.72 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 30 | 36.7% | +18176.70% | -56.62% | 321.00 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 46 | 34.8% | +16696.92% | -60.88% | 274.27 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 34 | 35.3% | +15384.36% | -56.27% | 273.41 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 26 | 42.3% | +16563.15% | -61.03% | 271.40 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 35 | 37.1% | +14712.45% | -54.26% | 271.13 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 36 | 38.9% | +15257.06% | -56.74% | 268.92 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 50 | 36 | 33.3% | +14527.90% | -56.75% | 256.01 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 37 | 43.2% | +13992.38% | -55.59% | 251.72 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 33 | 36.4% | +14293.26% | -58.29% | 245.19 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |

### ETHUSDT (1 Day)

- **File sumber:** `ethusdt_1d.csv`
- **Total candle:** 3248
- **Buy & Hold:** +477.33%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `10/20` → Return +7013.99%, MaxDD -46.34%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **3 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 20 | 56 | 37.5% | +7013.99% | -46.34% | 151.36 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 20 | 26 | 36 | 38.9% | +6260.66% | -46.42% | 134.88 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 37.7% | +5755.76% | -45.00% | 127.91 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 9 | 20 | 61 | 36.1% | +5704.75% | -49.98% | 114.15 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 12 | 20 | 53 | 37.7% | +5553.24% | -44.52% | 124.74 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 8 | 26 | 55 | 36.4% | +5330.95% | -53.09% | 100.42 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 30 | 40 | 23 | 39.1% | +5079.37% | -38.45% | 132.09 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 34 | 41.2% | +5021.73% | -34.45% | 145.77 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 79 | 32.9% | +4682.20% | -49.33% | 94.92 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 15 | 30 | 36 | 44.4% | +4523.11% | -39.14% | 115.56 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 20 | 56 | 37.5% | +7013.99% | -46.34% | 151.36 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 20 | 30 | 34 | 41.2% | +5021.73% | -34.45% | 145.77 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 36 | 41.7% | +4185.67% | -31.02% | 134.92 | 🔴 **53 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 36 | 38.9% | +6260.66% | -46.42% | 134.88 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 40 | 23 | 39.1% | +5079.37% | -38.45% | 132.09 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 37.7% | +5755.76% | -45.00% | 127.91 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 12 | 20 | 53 | 37.7% | +5553.24% | -44.52% | 124.74 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 15 | 30 | 36 | 44.4% | +4523.11% | -39.14% | 115.56 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 61 | 36.1% | +5704.75% | -49.98% | 114.15 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 25 | 50 | 22 | 40.9% | +4329.65% | -40.37% | 107.26 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |

### HBARUSDT (1 Day)

- **File sumber:** `hbarusdt_1d.csv`
- **Total candle:** 2475
- **Buy & Hold:** +95.05%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `12/30` → Return +5226.36%, MaxDD -34.93%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **35 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 31 | 35.5% | +5226.36% | -34.93% | 149.63 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 42 | 28.6% | +4521.47% | -51.31% | 88.12 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 17 | 52.9% | +3847.93% | -35.20% | 109.30 | 🔴 **286 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 39 | 28.2% | +3814.39% | -45.53% | 83.77 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 32 | 31.2% | +3490.14% | -43.71% | 79.85 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 30 | 36.7% | +3463.12% | -43.61% | 79.41 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 29 | 31.0% | +3451.76% | -43.71% | 78.97 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 18 | 50.0% | +3348.87% | -26.30% | 127.35 | 🔴 **286 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 37 | 29.7% | +3279.28% | -47.68% | 68.78 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 44 | 27.3% | +3122.83% | -52.86% | 59.07 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 31 | 35.5% | +5226.36% | -34.93% | 149.63 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 18 | 50.0% | +3348.87% | -26.30% | 127.35 | 🔴 **286 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 17 | 52.9% | +3847.93% | -35.20% | 109.30 | 🔴 **286 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 42 | 28.6% | +4521.47% | -51.31% | 88.12 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 39 | 28.2% | +3814.39% | -45.53% | 83.77 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 32 | 31.2% | +3490.14% | -43.71% | 79.85 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 30 | 36.7% | +3463.12% | -43.61% | 79.41 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 29 | 31.0% | +3451.76% | -43.71% | 78.97 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 27 | 29.6% | +2636.06% | -36.47% | 72.28 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 37 | 29.7% | +3279.28% | -47.68% | 68.78 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |

### LINKUSDT (1 Day)

- **File sumber:** `linkusdt_1d.csv`
- **Total candle:** 2731
- **Buy & Hold:** +1460.98%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `5/100` → Return +1614.49%, MaxDD -71.67%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **51 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 100 | 27 | 37.0% | +1614.49% | -71.67% | 22.53 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 35 | 34.3% | +1375.37% | -76.61% | 17.95 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 45 | 31.1% | +1347.77% | -64.33% | 20.95 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 43 | 37.2% | +1271.16% | -65.77% | 19.33 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 42 | 35.7% | +1187.78% | -74.26% | 16.00 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 44 | 36.4% | +1179.84% | -77.52% | 15.22 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 39.3% | +1149.00% | -62.79% | 18.30 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 25 | 100 | 14 | 28.6% | +1112.48% | -53.83% | 20.67 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 53 | 26.4% | +1097.85% | -57.62% | 19.05 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 38 | 31.6% | +1093.74% | -72.77% | 15.03 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 100 | 27 | 37.0% | +1614.49% | -71.67% | 22.53 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 45 | 31.1% | +1347.77% | -64.33% | 20.95 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 100 | 14 | 28.6% | +1112.48% | -53.83% | 20.67 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 43 | 37.2% | +1271.16% | -65.77% | 19.33 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 53 | 26.4% | +1097.85% | -57.62% | 19.05 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 39.3% | +1149.00% | -62.79% | 18.30 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 15 | 30 | 35 | 34.3% | +1375.37% | -76.61% | 17.95 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 42 | 35.7% | +1187.78% | -74.26% | 16.00 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 44 | 36.4% | +1179.84% | -77.52% | 15.22 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 88 | 31.8% | +1077.30% | -71.13% | 15.14 | 🟢 **4 hari lalu** (BUY, masih holding) |

### LTCUSDT (1 Day)

- **File sumber:** `ltcusdt_1d.csv`
- **Total candle:** 3130
- **Buy & Hold:** -84.95%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `15/40` → Return +209.25%, MaxDD -56.14%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **49 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 33 | 36.4% | +209.25% | -56.14% | 3.73 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 39 | 25.6% | +190.20% | -65.68% | 2.90 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 50 | 32 | 31.2% | +179.18% | -49.50% | 3.62 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 27 | 25.9% | +135.94% | -52.14% | 2.61 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 39 | 25.6% | +134.28% | -62.38% | 2.15 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 43 | 32.6% | +130.87% | -61.04% | 2.14 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 16 | 37.5% | +128.12% | -61.27% | 2.09 | 🔴 **268 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 75 | 19 | 31.6% | +122.96% | -61.82% | 1.99 | 🔴 **269 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 100 | 18 | 33.3% | +110.24% | -63.59% | 1.73 | 🔴 **268 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 24 | 29.2% | +108.64% | -58.21% | 1.87 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 33 | 36.4% | +209.25% | -56.14% | 3.73 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 50 | 32 | 31.2% | +179.18% | -49.50% | 3.62 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 39 | 25.6% | +190.20% | -65.68% | 2.90 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 27 | 25.9% | +135.94% | -52.14% | 2.61 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 39 | 25.6% | +134.28% | -62.38% | 2.15 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 43 | 32.6% | +130.87% | -61.04% | 2.14 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 16 | 37.5% | +128.12% | -61.27% | 2.09 | 🔴 **268 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 75 | 19 | 31.6% | +122.96% | -61.82% | 1.99 | 🔴 **269 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 24 | 29.2% | +108.64% | -58.21% | 1.87 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 100 | 18 | 33.3% | +110.24% | -63.59% | 1.73 | 🔴 **268 hari lalu** (SELL, menunggu sinyal beli) |

### NEARUSDT (1 Day)

- **File sumber:** `nearusdt_1d.csv`
- **Total candle:** 2094
- **Buy & Hold:** +61.92%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `5/26` → Return +1196.44%, MaxDD -72.03%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **16 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 26 | 47 | 34.0% | +1196.44% | -72.03% | 16.61 | 🔴 **16 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 53 | 37.7% | +1110.02% | -67.00% | 16.57 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 15 | 26 | 27 | 25.9% | +981.09% | -78.71% | 12.46 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 30 | 33.3% | +980.66% | -77.77% | 12.61 | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 41 | 31.7% | +870.03% | -73.02% | 11.92 | 🔴 **15 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 28 | 28.6% | +860.41% | -76.56% | 11.24 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 31 | 35.5% | +795.79% | -78.20% | 10.18 | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 27 | 29.6% | +778.56% | -79.36% | 9.81 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 41 | 39.0% | +700.34% | -75.35% | 9.29 | 🔴 **16 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 27 | 29.6% | +681.83% | -77.10% | 8.84 | 🔴 **12 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 26 | 47 | 34.0% | +1196.44% | -72.03% | 16.61 | 🔴 **16 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 53 | 37.7% | +1110.02% | -67.00% | 16.57 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 10 | 30 | 30 | 33.3% | +980.66% | -77.77% | 12.61 | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 27 | 25.9% | +981.09% | -78.71% | 12.46 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 41 | 31.7% | +870.03% | -73.02% | 11.92 | 🔴 **15 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 28 | 28.6% | +860.41% | -76.56% | 11.24 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 31 | 35.5% | +795.79% | -78.20% | 10.18 | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 27 | 29.6% | +778.56% | -79.36% | 9.81 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 41 | 39.0% | +700.34% | -75.35% | 9.29 | 🔴 **16 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 27 | 29.6% | +681.83% | -77.10% | 8.84 | 🔴 **12 hari lalu** (SELL, menunggu sinyal beli) |

### PAXGUSDT (1 Day)

- **File sumber:** `paxgusdt_1d.csv`
- **Total candle:** 2141
- **Buy & Hold:** +105.92%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `10/40` → Return +103.60%, MaxDD -7.56%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **78 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 20 | 150 | 6 | 50.0% | +130.22% | -8.78% | 14.84 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 100 | 7 | 42.9% | +123.21% | -12.98% | 9.49 | 🔴 **77 hari lalu** (SELL, menunggu sinyal beli) |
| 40 | 75 | 6 | 50.0% | +121.76% | -12.34% | 9.87 | 🔴 **100 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 150 | 6 | 33.3% | +120.47% | -8.33% | 14.47 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 6 | 50.0% | +120.20% | -8.83% | 13.61 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 150 | 6 | 33.3% | +119.26% | -8.95% | 13.33 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 150 | 11 | 36.4% | +119.16% | -9.47% | 12.59 | 🔴 **53 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 6 | 50.0% | +119.13% | -8.68% | 13.72 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 200 | 6 | 50.0% | +118.23% | -9.49% | 12.46 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 150 | 10 | 30.0% | +117.75% | -10.41% | 11.31 | 🔴 **53 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 30 | 75 | 8 | 50.0% | +117.39% | -7.75% | 15.15 | 🔴 **104 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 150 | 6 | 50.0% | +130.22% | -8.78% | 14.84 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 150 | 6 | 33.3% | +120.47% | -8.33% | 14.47 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 6 | 50.0% | +119.13% | -8.68% | 13.72 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 27 | 37.0% | +103.60% | -7.56% | 13.70 | 🔴 **78 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 75 | 16 | 43.8% | +110.35% | -8.10% | 13.62 | 🔴 **110 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 6 | 50.0% | +120.20% | -8.83% | 13.61 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 24 | 33.3% | +104.88% | -7.77% | 13.50 | 🔴 **112 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 150 | 6 | 33.3% | +119.26% | -8.95% | 13.33 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 15 | 46.7% | +106.93% | -8.03% | 13.31 | 🔴 **110 hari lalu** (SELL, menunggu sinyal beli) |

### SOLUSDT (1 Day)

- **File sumber:** `solusdt_1d.csv`
- **Total candle:** 2158
- **Buy & Hold:** +2259.56%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `9/26` → Return +18559.89%, MaxDD -44.22%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **7 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 26 | 37 | 35.1% | +18559.89% | -44.22% | 419.74 | 🟢 **7 hari lalu** (BUY, masih holding) |
| 20 | 150 | 7 | 42.9% | +15636.48% | -25.67% | 609.02 | 🔴 **247 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 42 | 33.3% | +14346.69% | -47.32% | 303.18 | 🟢 **7 hari lalu** (BUY, masih holding) |
| 15 | 20 | 30 | 36.7% | +13841.27% | -42.23% | 327.74 | 🟢 **7 hari lalu** (BUY, masih holding) |
| 12 | 20 | 39 | 35.9% | +13737.16% | -49.84% | 275.60 | 🟢 **7 hari lalu** (BUY, masih holding) |
| 10 | 26 | 35 | 31.4% | +13667.98% | -44.00% | 310.67 | 🟢 **7 hari lalu** (BUY, masih holding) |
| 8 | 30 | 35 | 31.4% | +12260.13% | -55.30% | 221.71 | 🟢 **7 hari lalu** (BUY, masih holding) |
| 5 | 30 | 47 | 27.7% | +11257.24% | -57.19% | 196.82 | 🟢 **7 hari lalu** (BUY, masih holding) |
| 10 | 20 | 43 | 32.6% | +11159.41% | -59.57% | 187.33 | 🟢 **8 hari lalu** (BUY, masih holding) |
| 8 | 150 | 14 | 35.7% | +11095.73% | -32.25% | 344.00 | 🔴 **250 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 20 | 150 | 7 | 42.9% | +15636.48% | -25.67% | 609.02 | 🔴 **247 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 37 | 35.1% | +18559.89% | -44.22% | 419.74 | 🟢 **7 hari lalu** (BUY, masih holding) |
| 25 | 150 | 8 | 37.5% | +10725.07% | -29.91% | 358.62 | 🔴 **246 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 150 | 14 | 35.7% | +10982.59% | -31.29% | 351.03 | 🔴 **250 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 150 | 14 | 35.7% | +11095.73% | -32.25% | 344.00 | 🔴 **250 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 150 | 7 | 42.9% | +10803.29% | -31.57% | 342.18 | 🔴 **245 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 30 | 36.7% | +13841.27% | -42.23% | 327.74 | 🟢 **7 hari lalu** (BUY, masih holding) |
| 10 | 150 | 14 | 35.7% | +10191.77% | -31.15% | 327.16 | 🔴 **250 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 35 | 31.4% | +13667.98% | -44.00% | 310.67 | 🟢 **7 hari lalu** (BUY, masih holding) |
| 8 | 26 | 42 | 33.3% | +14346.69% | -47.32% | 303.18 | 🟢 **7 hari lalu** (BUY, masih holding) |

### SUIUSDT (1 Day)

- **File sumber:** `suiusdt_1d.csv`
- **Total candle:** 1163
- **Buy & Hold:** -49.27%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `5/26` → Return +408.00%, MaxDD -50.43%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **44 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 50 | 12 | 25.0% | +646.47% | -51.10% | 12.65 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 8 | 37.5% | +634.96% | -45.79% | 13.87 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 11 | 27.3% | +634.09% | -49.42% | 12.83 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 14 | 28.6% | +619.83% | -47.17% | 13.14 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 40 | 8 | 37.5% | +581.39% | -40.97% | 14.19 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 11 | 27.3% | +536.57% | -50.05% | 10.72 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 9 | 33.3% | +529.40% | -46.40% | 11.41 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 12 | 25.0% | +484.01% | -51.90% | 9.33 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 50 | 9 | 22.2% | +472.10% | -43.90% | 10.75 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 9 | 33.3% | +472.08% | -44.27% | 10.66 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 8 | 37.5% | +581.39% | -40.97% | 14.19 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 8 | 37.5% | +634.96% | -45.79% | 13.87 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 14 | 28.6% | +619.83% | -47.17% | 13.14 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 11 | 27.3% | +634.09% | -49.42% | 12.83 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 50 | 12 | 25.0% | +646.47% | -51.10% | 12.65 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 7 | 28.6% | +470.51% | -38.92% | 12.09 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 9 | 33.3% | +529.40% | -46.40% | 11.41 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 9 | 33.3% | +446.77% | -40.95% | 10.91 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 50 | 9 | 22.2% | +472.10% | -43.90% | 10.75 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 11 | 27.3% | +536.57% | -50.05% | 10.72 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |

### TRXUSDT (1 Day)

- **File sumber:** `trxusdt_1d.csv`
- **Total candle:** 2950
- **Buy & Hold:** +578.72%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `12/30` → Return +1222.82%, MaxDD -43.96%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **35 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 41 | 39.0% | +1222.82% | -43.96% | 27.81 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 62 | 40.3% | +1035.66% | -38.57% | 26.85 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 12 | 26 | 50 | 38.0% | +1005.38% | -53.45% | 18.81 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 54 | 40.7% | +993.13% | -47.27% | 21.01 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 9 | 20 | 65 | 40.0% | +938.34% | -39.74% | 23.61 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 10 | 26 | 53 | 41.5% | +907.91% | -46.01% | 19.73 | 🟢 **Hari ini** (BUY, masih holding) |
| 15 | 26 | 41 | 39.0% | +873.59% | -47.25% | 18.49 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 48 | 41.7% | +868.70% | -50.94% | 17.05 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 55 | 34.5% | +825.51% | -52.65% | 15.68 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 100 | 17 | 41.2% | +805.98% | -43.78% | 18.41 | 🔴 **26 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 41 | 39.0% | +1222.82% | -43.96% | 27.81 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 62 | 40.3% | +1035.66% | -38.57% | 26.85 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 9 | 20 | 65 | 40.0% | +938.34% | -39.74% | 23.61 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 8 | 75 | 26 | 50.0% | +797.96% | -37.28% | 21.41 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 54 | 40.7% | +993.13% | -47.27% | 21.01 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 9 | 100 | 20 | 45.0% | +718.26% | -36.15% | 19.87 | 🔴 **28 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 24 | 45.8% | +764.58% | -38.57% | 19.82 | 🔴 **29 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 53 | 41.5% | +907.91% | -46.01% | 19.73 | 🟢 **Hari ini** (BUY, masih holding) |
| 9 | 75 | 26 | 46.2% | +694.93% | -35.61% | 19.51 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 50 | 38.0% | +1005.38% | -53.45% | 18.81 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |

### UNIUSDT (1 Day)

- **File sumber:** `uniusdt_1d.csv`
- **Total candle:** 2121
- **Buy & Hold:** -5.25%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `25/26` → Return +1328.06%, MaxDD -35.67%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **3 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 26 | 18 | 50.0% | +1328.06% | -35.67% | 37.23 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 15 | 40 | 20 | 45.0% | +924.34% | -45.23% | 20.43 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 20 | 30 | 22 | 40.9% | +885.97% | -36.69% | 24.15 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 12 | 50 | 21 | 38.1% | +699.43% | -49.67% | 14.08 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 20 | 26 | 27 | 29.6% | +682.39% | -47.74% | 14.29 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 25 | 30 | 18 | 38.9% | +670.42% | -53.19% | 12.61 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 12 | 40 | 24 | 33.3% | +651.14% | -45.45% | 14.33 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 20 | 40 | 17 | 35.3% | +591.63% | -60.34% | 9.80 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 9 | 50 | 23 | 39.1% | +561.85% | -46.83% | 12.00 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 15 | 30 | 26 | 42.3% | +556.04% | -45.14% | 12.32 | 🟢 **5 hari lalu** (BUY, masih holding) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 26 | 18 | 50.0% | +1328.06% | -35.67% | 37.23 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 20 | 30 | 22 | 40.9% | +885.97% | -36.69% | 24.15 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 15 | 40 | 20 | 45.0% | +924.34% | -45.23% | 20.43 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 12 | 40 | 24 | 33.3% | +651.14% | -45.45% | 14.33 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 20 | 26 | 27 | 29.6% | +682.39% | -47.74% | 14.29 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 12 | 50 | 21 | 38.1% | +699.43% | -49.67% | 14.08 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 25 | 30 | 18 | 38.9% | +670.42% | -53.19% | 12.61 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 15 | 30 | 26 | 42.3% | +556.04% | -45.14% | 12.32 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 9 | 50 | 23 | 39.1% | +561.85% | -46.83% | 12.00 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 15 | 26 | 27 | 33.3% | +457.01% | -44.11% | 10.36 | 🟢 **5 hari lalu** (BUY, masih holding) |

### XLMUSDT (1 Day)

- **File sumber:** `xlmusdt_1d.csv`
- **Total candle:** 2961
- **Buy & Hold:** -38.68%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `5/30` → Return +362.01%, MaxDD -66.34%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **Hari ini** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 30 | 61 | 31.1% | +362.01% | -66.34% | 5.46 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 5 | 20 | 79 | 29.1% | +246.46% | -66.91% | 3.68 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 5 | 150 | 21 | 28.6% | +179.79% | -52.86% | 3.40 | 🟢 **6 hari lalu** (BUY, masih holding) |
| 5 | 26 | 74 | 28.4% | +133.77% | -70.64% | 1.89 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 8 | 26 | 57 | 28.1% | +127.45% | -69.07% | 1.85 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 9 | 150 | 18 | 22.2% | +117.40% | -55.29% | 2.12 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 8 | 150 | 19 | 21.1% | +107.90% | -59.99% | 1.80 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 5 | 200 | 24 | 20.8% | +106.49% | -52.68% | 2.02 | 🔴 **1 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 150 | 18 | 22.2% | +98.53% | -54.55% | 1.81 | 🟢 **6 hari lalu** (BUY, masih holding) |
| 9 | 20 | 65 | 27.7% | +93.45% | -67.98% | 1.37 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 30 | 61 | 31.1% | +362.01% | -66.34% | 5.46 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 5 | 20 | 79 | 29.1% | +246.46% | -66.91% | 3.68 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 5 | 150 | 21 | 28.6% | +179.79% | -52.86% | 3.40 | 🟢 **6 hari lalu** (BUY, masih holding) |
| 9 | 150 | 18 | 22.2% | +117.40% | -55.29% | 2.12 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 5 | 200 | 24 | 20.8% | +106.49% | -52.68% | 2.02 | 🔴 **1 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 26 | 74 | 28.4% | +133.77% | -70.64% | 1.89 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 8 | 26 | 57 | 28.1% | +127.45% | -69.07% | 1.85 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 10 | 150 | 18 | 22.2% | +98.53% | -54.55% | 1.81 | 🟢 **6 hari lalu** (BUY, masih holding) |
| 8 | 150 | 19 | 21.1% | +107.90% | -59.99% | 1.80 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 8 | 200 | 17 | 23.5% | +79.93% | -53.42% | 1.50 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |

### XMRUSD (1 Day)

- **File sumber:** `xmrusd_daily_kraken.csv`
- **Total candle:** 725
- **Buy & Hold:** +99.97%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `9/20` → Return +105.86%, MaxDD -9.53%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **46 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 20 | 10 | 50.0% | +167.80% | -10.63% | 15.78 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 11 | 45.5% | +164.23% | -9.43% | 17.42 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 8 | 50.0% | +142.38% | -11.89% | 11.97 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 12 | 58.3% | +138.26% | -9.03% | 15.32 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 10 | 50.0% | +138.24% | -9.43% | 14.66 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 12 | 41.7% | +137.38% | -10.26% | 13.39 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 40 | 8 | 50.0% | +137.22% | -11.89% | 11.54 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 7 | 57.1% | +135.59% | -16.67% | 8.14 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 12 | 41.7% | +127.87% | -9.40% | 13.61 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 9 | 44.4% | +121.99% | -10.55% | 11.56 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 8 | 26 | 11 | 45.5% | +164.23% | -9.43% | 17.42 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 10 | 50.0% | +167.80% | -10.63% | 15.78 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 12 | 58.3% | +138.26% | -9.03% | 15.32 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 150 | 3 | 66.7% | +52.95% | -3.59% | 14.76 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 10 | 50.0% | +138.24% | -9.43% | 14.66 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 12 | 41.7% | +127.87% | -9.40% | 13.61 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 12 | 41.7% | +137.38% | -10.26% | 13.39 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 8 | 50.0% | +142.38% | -11.89% | 11.97 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 12 | 33.3% | +118.62% | -10.08% | 11.76 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 9 | 44.4% | +121.99% | -10.55% | 11.56 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |

### XRPUSDT (1 Day)

- **File sumber:** `xrpusdt_1d.csv`
- **Total candle:** 2988
- **Buy & Hold:** +22.58%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `9/200` → Return +99.26%, MaxDD -50.56%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **267 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 200 | 16 | 25.0% | +99.26% | -50.56% | 1.96 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 200 | 13 | 23.1% | +92.56% | -48.62% | 1.90 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 200 | 10 | 30.0% | +92.12% | -47.52% | 1.94 | 🔴 **260 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 83 | 21.7% | +86.41% | -69.82% | 1.24 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 20 | 30 | 35 | 25.7% | +82.61% | -68.94% | 1.20 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 200 | 16 | 31.2% | +79.38% | -57.81% | 1.37 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 16 | 31.2% | +76.63% | -54.49% | 1.41 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 12 | 25.0% | +58.11% | -57.81% | 1.01 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 64 | 26.6% | +53.68% | -76.57% | 0.70 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 47 | 29.8% | +49.37% | -61.78% | 0.80 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 200 | 16 | 25.0% | +99.26% | -50.56% | 1.96 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 200 | 10 | 30.0% | +92.12% | -47.52% | 1.94 | 🔴 **260 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 200 | 13 | 23.1% | +92.56% | -48.62% | 1.90 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 16 | 31.2% | +76.63% | -54.49% | 1.41 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 200 | 16 | 31.2% | +79.38% | -57.81% | 1.37 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 83 | 21.7% | +86.41% | -69.82% | 1.24 | 🔴 **Hari ini** (SELL, menunggu sinyal beli) |
| 20 | 30 | 35 | 25.7% | +82.61% | -68.94% | 1.20 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 12 | 25.0% | +58.11% | -57.81% | 1.01 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 200 | 11 | 27.3% | +47.08% | -56.08% | 0.84 | 🔴 **263 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 47 | 29.8% | +49.37% | -61.78% | 0.80 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |

### ZECUSDT (1 Day)

- **File sumber:** `zecusdt_1d.csv`
- **Total candle:** 2667
- **Buy & Hold:** +745.10%
- **Rekomendasi (calmar tertinggi, trades >= 15):** EMA `9/20` → Return +5762.05%, MaxDD -51.62%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **2 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 20 | 50 | 38.0% | +5762.05% | -51.62% | 111.63 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 5 | 26 | 59 | 33.9% | +5659.00% | -75.56% | 74.89 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 8 | 20 | 52 | 36.5% | +5079.14% | -55.02% | 92.32 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 5 | 20 | 66 | 33.3% | +4250.79% | -72.86% | 58.34 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 10 | 26 | 42 | 40.5% | +3433.27% | -46.94% | 73.14 | 🟢 **Hari ini** (BUY, masih holding) |
| 8 | 40 | 33 | 42.4% | +3358.87% | -57.52% | 58.39 | 🟢 **Hari ini** (BUY, masih holding) |
| 12 | 26 | 40 | 45.0% | +3094.18% | -57.93% | 53.41 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 52 | 40.4% | +3039.66% | -48.32% | 62.90 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 12 | 20 | 46 | 37.0% | +3002.87% | -49.71% | 60.41 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 8 | 26 | 48 | 33.3% | +2907.79% | -48.66% | 59.76 | 🟢 **1 hari lalu** (BUY, masih holding) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 20 | 50 | 38.0% | +5762.05% | -51.62% | 111.63 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 8 | 20 | 52 | 36.5% | +5079.14% | -55.02% | 92.32 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 5 | 26 | 59 | 33.9% | +5659.00% | -75.56% | 74.89 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 10 | 26 | 42 | 40.5% | +3433.27% | -46.94% | 73.14 | 🟢 **Hari ini** (BUY, masih holding) |
| 10 | 20 | 52 | 40.4% | +3039.66% | -48.32% | 62.90 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 12 | 20 | 46 | 37.0% | +3002.87% | -49.71% | 60.41 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 8 | 26 | 48 | 33.3% | +2907.79% | -48.66% | 59.76 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 15 | 20 | 39 | 46.2% | +2757.55% | -46.94% | 58.74 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 40 | 33 | 42.4% | +3358.87% | -57.52% | 58.39 | 🟢 **Hari ini** (BUY, masih holding) |
| 5 | 20 | 66 | 33.3% | +4250.79% | -72.86% | 58.34 | 🟢 **4 hari lalu** (BUY, masih holding) |


<!-- BACKTEST_RESULTS_END -->

---

_Dihasilkan otomatis oleh `backtest.py`. Metodologi: dual EMA crossover, long-only,
fee dihitung di setiap entry & exit, tanpa slippage. Hasil in-sample murni --
lihat catatan walk-forward terpisah untuk validasi out-of-sample._
