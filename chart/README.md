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

| Pair | Timeframe | Total Candle | EMA Terbaik | Return | Max DD | Buy & Hold | vs B&H | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|---|
| **NEARUSDT** | 1 Day | 2092 | `5/20` | +1213.32% | -67.00% | +75.70% | ✅ Menang | 🟢 **Hari ini** (BUY, masih holding) |
| **ZECUSDT** | 1 Day | 2665 | `9/20` | +5594.37% | -51.62% | +721.00% | ✅ Menang | 🟢 **Hari ini** (BUY, masih holding) |
| **ETHUSDT** | 1 Day | 3246 | `10/20` | +7243.26% | -46.34% | +495.88% | ✅ Menang | 🟢 **1 hari lalu** (BUY, masih holding) |
| **UNIUSDT** | 1 Day | 2119 | `25/26` | +1284.83% | -35.67% | -8.11% | ✅ Menang | 🟢 **1 hari lalu** (BUY, masih holding) |
| **XLMUSDT** | 1 Day | 2959 | `5/30` | +410.08% | -62.84% | -32.33% | ✅ Menang | 🟢 **3 hari lalu** (BUY, masih holding) |
| **SOLUSDT** | 1 Day | 2156 | `9/26` | +19548.22% | -44.22% | +2384.16% | ✅ Menang | 🟢 **5 hari lalu** (BUY, masih holding) |

## Ringkasan Hasil -- Bearish (Sinyal SELL)

| Pair | Timeframe | Total Candle | EMA Terbaik | Return | Max DD | Buy & Hold | vs B&H | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|---|
| **BNBUSDT** | 1 Day | 3165 | `10/26` | +30822.68% | -31.91% | +37201.72% | ❌ Kalah | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| **HBARUSDT** | 1 Day | 2473 | `12/30` | +5226.36% | -34.93% | +106.30% | ✅ Menang | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| **TRXUSDT** | 1 Day | 2948 | `12/30` | +1222.82% | -43.96% | +581.20% | ✅ Menang | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| **SUIUSDT** | 1 Day | 1161 | `5/50` | +646.47% | -51.10% | -46.50% | ✅ Menang | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| **DOGEUSDT** | 1 Day | 2559 | `15/26` | +18176.70% | -56.62% | +1880.83% | ✅ Menang | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| **XMRUSD** | 1 Day | 724 | `12/20` | +167.80% | -10.63% | +103.11% | ✅ Menang | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| **BTCUSDT** | 1 Day | 3246 | `10/30` | +6804.41% | -52.55% | +1394.53% | ✅ Menang | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| **ADAUSDT** | 1 Day | 3003 | `15/40` | +9390.82% | -34.42% | -24.07% | ✅ Menang | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| **LTCUSDT** | 1 Day | 3128 | `15/40` | +209.25% | -56.14% | -84.54% | ✅ Menang | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| **LINKUSDT** | 1 Day | 2729 | `5/100` | +1614.49% | -71.67% | +1538.61% | ✅ Menang | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| **PAXGUSDT** | 1 Day | 2139 | `20/150` | +130.22% | -8.78% | +109.91% | ✅ Menang | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| **AVAXUSDT** | 1 Day | 2114 | `15/75` | +3356.67% | -33.05% | +30.28% | ✅ Menang | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| **BCHUSDT** | 1 Day | 2413 | `25/75` | +200.06% | -55.10% | +11.36% | ✅ Menang | 🔴 **154 hari lalu** (SELL, menunggu sinyal beli) |
| **XRPUSDT** | 1 Day | 2986 | `9/200` | +99.26% | -50.56% | +28.67% | ✅ Menang | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |

## Detail per Aset

### ADAUSDT (1 Day)

- **File sumber:** `adausdt_1d.csv`
- **Total candle:** 3003
- **Buy & Hold:** -24.07%
- **Rekomendasi (return tertinggi):** EMA `15/40` → Return +9390.82%, MaxDD -34.42%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **46 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 25 | 40.0% | +9390.82% | -34.42% | 272.84 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 40 | 23 | 39.1% | +7843.51% | -38.26% | 205.03 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 21 | 42.9% | +7288.51% | -35.55% | 205.01 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 25 | 40.0% | +7048.53% | -32.34% | 217.92 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 32 | 37.5% | +6974.95% | -41.99% | 166.12 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 23 | 39.1% | +6464.02% | -42.21% | 153.15 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 20 | 50.0% | +6346.56% | -41.09% | 154.45 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 75 | 26 | 46.2% | +6326.46% | -46.12% | 137.18 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 29 | 37.9% | +6315.59% | -44.41% | 142.22 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 26 | 38.5% | +6309.51% | -37.53% | 168.10 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 25 | 40.0% | +9390.82% | -34.42% | 272.84 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 25 | 40.0% | +7048.53% | -32.34% | 217.92 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 40 | 23 | 39.1% | +7843.51% | -38.26% | 205.03 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 21 | 42.9% | +7288.51% | -35.55% | 205.01 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 75 | 14 | 50.0% | +5778.85% | -30.69% | 188.28 | 🔴 **269 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 26 | 38.5% | +6309.51% | -37.53% | 168.10 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 32 | 37.5% | +6974.95% | -41.99% | 166.12 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 20 | 50.0% | +6346.56% | -41.09% | 154.45 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 23 | 39.1% | +6464.02% | -42.21% | 153.15 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 50 | 33 | 36.4% | +5800.66% | -39.13% | 148.24 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |

### AVAXUSDT (1 Day)

- **File sumber:** `avaxusdt_1d.csv`
- **Total candle:** 2114
- **Buy & Hold:** +30.28%
- **Rekomendasi (return tertinggi):** EMA `15/75` → Return +3356.67%, MaxDD -33.05%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **52 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 75 | 13 | 38.5% | +3356.67% | -33.05% | 101.58 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 15 | 26.7% | +2538.89% | -43.16% | 58.83 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 52 | 23.1% | +2424.81% | -59.69% | 40.62 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 10 | 100 | 14 | 28.6% | +2363.80% | -41.18% | 57.40 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 14 | 28.6% | +2309.05% | -42.99% | 53.71 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 37 | 29.7% | +2145.24% | -63.60% | 33.73 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 46 | 23.9% | +2024.53% | -56.09% | 36.10 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 20 | 50 | 15 | 33.3% | +2017.64% | -42.82% | 47.12 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 42 | 28.6% | +1991.40% | -62.73% | 31.75 | 🟢 **Hari ini** (BUY, masih holding) |
| 10 | 26 | 33 | 30.3% | +1977.83% | -66.26% | 29.85 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 75 | 13 | 38.5% | +3356.67% | -33.05% | 101.58 | 🔴 **52 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 75 | 10 | 40.0% | +1857.34% | -29.37% | 63.24 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 15 | 26.7% | +2538.89% | -43.16% | 58.83 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 100 | 14 | 28.6% | +2363.80% | -41.18% | 57.40 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 14 | 28.6% | +2309.05% | -42.99% | 53.71 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 50 | 15 | 33.3% | +2017.64% | -42.82% | 47.12 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 100 | 13 | 30.8% | +1540.88% | -36.86% | 41.80 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 52 | 23.1% | +2424.81% | -59.69% | 40.62 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 8 | 100 | 17 | 23.5% | +1687.99% | -43.06% | 39.20 | 🔴 **268 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 10 | 40.0% | +1252.96% | -32.01% | 39.14 | 🔴 **262 hari lalu** (SELL, menunggu sinyal beli) |

### BCHUSDT (1 Day)

- **File sumber:** `bchusdt_1d.csv`
- **Total candle:** 2413
- **Buy & Hold:** +11.36%
- **Rekomendasi (return tertinggi):** EMA `25/75` → Return +200.06%, MaxDD -55.10%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **154 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 75 | 14 | 35.7% | +200.06% | -55.10% | 3.63 | 🔴 **154 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 75 | 11 | 36.4% | +184.31% | -45.26% | 4.07 | 🔴 **153 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 19 | 31.6% | +165.26% | -55.04% | 3.00 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 100 | 12 | 41.7% | +161.33% | -37.10% | 4.35 | 🔴 **154 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 100 | 23 | 30.4% | +141.62% | -50.68% | 2.79 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 40 | 50 | 14 | 35.7% | +139.55% | -53.22% | 2.62 | 🔴 **153 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 68 | 29.4% | +114.86% | -66.39% | 1.73 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 12 | 100 | 16 | 31.2% | +109.75% | -59.95% | 1.83 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 100 | 15 | 33.3% | +101.19% | -61.63% | 1.64 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 22 | 31.8% | +100.11% | -58.51% | 1.71 | 🔴 **157 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 20 | 100 | 12 | 41.7% | +161.33% | -37.10% | 4.35 | 🔴 **154 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 75 | 11 | 36.4% | +184.31% | -45.26% | 4.07 | 🔴 **153 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 14 | 35.7% | +200.06% | -55.10% | 3.63 | 🔴 **154 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 19 | 31.6% | +165.26% | -55.04% | 3.00 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 100 | 23 | 30.4% | +141.62% | -50.68% | 2.79 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 40 | 50 | 14 | 35.7% | +139.55% | -53.22% | 2.62 | 🔴 **153 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 100 | 16 | 31.2% | +109.75% | -59.95% | 1.83 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 68 | 29.4% | +114.86% | -66.39% | 1.73 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 12 | 75 | 22 | 31.8% | +100.11% | -58.51% | 1.71 | 🔴 **157 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 39 | 30.8% | +96.49% | -56.65% | 1.70 | 🔴 **55 hari lalu** (SELL, menunggu sinyal beli) |

### BNBUSDT (1 Day)

- **File sumber:** `bnbusdt_1d.csv`
- **Total candle:** 3165
- **Buy & Hold:** +37201.72%
- **Rekomendasi (return tertinggi):** EMA `10/26` → Return +30822.68%, MaxDD -31.91%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **32 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 26 | 46 | 45.7% | +30822.68% | -31.91% | 965.85 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 34 | 47.1% | +27733.76% | -36.73% | 755.10 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 46 | 45.7% | +26606.06% | -35.84% | 742.35 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 35 | 48.6% | +24534.25% | -36.09% | 679.71 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 41 | 46.3% | +21283.08% | -33.21% | 640.81 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 43 | 48.8% | +21137.95% | -33.13% | 638.01 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 52 | 42.3% | +20012.75% | -38.95% | 513.87 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 40 | 37 | 40.5% | +19337.91% | -43.36% | 446.01 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 47 | 46.8% | +19326.85% | -29.22% | 661.39 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 34 | 38.2% | +19029.96% | -41.94% | 453.74 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 26 | 46 | 45.7% | +30822.68% | -31.91% | 965.85 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 34 | 47.1% | +27733.76% | -36.73% | 755.10 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 46 | 45.7% | +26606.06% | -35.84% | 742.35 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 35 | 48.6% | +24534.25% | -36.09% | 679.71 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 47 | 46.8% | +19326.85% | -29.22% | 661.39 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 41 | 46.3% | +21283.08% | -33.21% | 640.81 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 43 | 48.8% | +21137.95% | -33.13% | 638.01 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 35 | 40.0% | +18432.73% | -30.15% | 611.40 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 52 | 42.3% | +20012.75% | -38.95% | 513.87 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 34 | 35.3% | +14590.54% | -30.30% | 481.60 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |

### BTCUSDT (1 Day)

- **File sumber:** `btcusdt_1d.csv`
- **Total candle:** 3246
- **Buy & Hold:** +1394.53%
- **Rekomendasi (return tertinggi):** EMA `10/30` → Return +6804.41%, MaxDD -52.55%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **45 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 30 | 44 | 38.6% | +6804.41% | -52.55% | 129.48 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 51 | 35.3% | +5336.21% | -51.68% | 103.26 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 47 | 36.2% | +4361.34% | -53.73% | 81.17 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 54 | 35.2% | +4300.59% | -57.97% | 74.19 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 58 | 34.5% | +4205.05% | -50.07% | 83.99 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 51 | 33.3% | +4198.99% | -54.14% | 77.56 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 48 | 35.4% | +4156.22% | -53.26% | 78.04 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 26 | 42.3% | +4052.75% | -38.87% | 104.28 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 42 | 38.1% | +3858.53% | -48.75% | 79.14 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 63 | 34.9% | +3828.81% | -61.34% | 62.42 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 30 | 44 | 38.6% | +6804.41% | -52.55% | 129.48 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 26 | 42.3% | +4052.75% | -38.87% | 104.28 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 51 | 35.3% | +5336.21% | -51.68% | 103.26 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 50 | 23 | 43.5% | +3513.43% | -35.28% | 99.58 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 50 | 23 | 39.1% | +3002.00% | -34.93% | 85.95 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 58 | 34.5% | +4205.05% | -50.07% | 83.99 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 47 | 36.2% | +4361.34% | -53.73% | 81.17 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 50 | 25 | 40.0% | +3192.44% | -39.95% | 79.90 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 42 | 38.1% | +3858.53% | -48.75% | 79.14 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 48 | 35.4% | +4156.22% | -53.26% | 78.04 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |

### DOGEUSDT (1 Day)

- **File sumber:** `dogeusdt_1d.csv`
- **Total candle:** 2559
- **Buy & Hold:** +1880.83%
- **Rekomendasi (return tertinggi):** EMA `15/26` → Return +18176.70%, MaxDD -56.62%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **41 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 26 | 30 | 36.7% | +18176.70% | -56.62% | 321.00 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 23 | 34.8% | +17991.17% | -52.04% | 345.72 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 46 | 34.8% | +16696.92% | -60.88% | 274.27 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 26 | 42.3% | +16563.15% | -61.03% | 271.40 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 34 | 35.3% | +15384.36% | -56.27% | 273.41 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 36 | 38.9% | +15257.06% | -56.74% | 268.92 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 35 | 37.1% | +14712.45% | -54.26% | 271.13 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 50 | 36 | 33.3% | +14527.90% | -56.75% | 256.01 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 33 | 36.4% | +14293.26% | -58.29% | 245.19 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 26 | 34.6% | +14266.58% | -62.14% | 229.60 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 30 | 23 | 34.8% | +17991.17% | -52.04% | 345.72 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 30 | 36.7% | +18176.70% | -56.62% | 321.00 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 46 | 34.8% | +16696.92% | -60.88% | 274.27 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 34 | 35.3% | +15384.36% | -56.27% | 273.41 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 26 | 42.3% | +16563.15% | -61.03% | 271.40 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 35 | 37.1% | +14712.45% | -54.26% | 271.13 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 36 | 38.9% | +15257.06% | -56.74% | 268.92 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 50 | 36 | 33.3% | +14527.90% | -56.75% | 256.01 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 37 | 43.2% | +13992.38% | -55.59% | 251.72 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 33 | 36.4% | +14293.26% | -58.29% | 245.19 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |

### ETHUSDT (1 Day)

- **File sumber:** `ethusdt_1d.csv`
- **Total candle:** 3246
- **Buy & Hold:** +495.88%
- **Rekomendasi (return tertinggi):** EMA `10/20` → Return +7243.26%, MaxDD -46.34%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **1 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 20 | 56 | 39.3% | +7243.26% | -46.34% | 156.31 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 20 | 26 | 36 | 38.9% | +6260.66% | -46.42% | 134.88 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 39.3% | +5944.48% | -45.00% | 132.11 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 9 | 20 | 61 | 37.7% | +5891.83% | -49.98% | 117.89 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 12 | 20 | 53 | 37.7% | +5735.44% | -44.52% | 128.83 | 🟢 **Hari ini** (BUY, masih holding) |
| 8 | 26 | 55 | 36.4% | +5505.99% | -53.09% | 103.71 | 🟢 **Hari ini** (BUY, masih holding) |
| 30 | 40 | 23 | 39.1% | +5079.37% | -38.45% | 132.09 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 34 | 41.2% | +5021.73% | -34.45% | 145.77 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 79 | 34.2% | +4836.32% | -49.33% | 98.05 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 15 | 30 | 36 | 44.4% | +4523.11% | -39.14% | 115.56 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 20 | 56 | 39.3% | +7243.26% | -46.34% | 156.31 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 20 | 30 | 34 | 41.2% | +5021.73% | -34.45% | 145.77 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 36 | 41.7% | +4185.67% | -31.02% | 134.92 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 36 | 38.9% | +6260.66% | -46.42% | 134.88 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 39.3% | +5944.48% | -45.00% | 132.11 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 30 | 40 | 23 | 39.1% | +5079.37% | -38.45% | 132.09 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 53 | 37.7% | +5735.44% | -44.52% | 128.83 | 🟢 **Hari ini** (BUY, masih holding) |
| 9 | 20 | 61 | 37.7% | +5891.83% | -49.98% | 117.89 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 15 | 30 | 36 | 44.4% | +4523.11% | -39.14% | 115.56 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 50 | 22 | 40.9% | +4329.65% | -40.37% | 107.26 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |

### HBARUSDT (1 Day)

- **File sumber:** `hbarusdt_1d.csv`
- **Total candle:** 2473
- **Buy & Hold:** +106.30%
- **Rekomendasi (return tertinggi):** EMA `12/30` → Return +5226.36%, MaxDD -34.93%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **33 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 31 | 35.5% | +5226.36% | -34.93% | 149.63 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 42 | 28.6% | +4521.47% | -51.31% | 88.12 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 17 | 52.9% | +3847.93% | -35.20% | 109.30 | 🔴 **284 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 39 | 28.2% | +3814.39% | -45.53% | 83.77 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 32 | 31.2% | +3490.14% | -43.71% | 79.85 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 30 | 36.7% | +3463.12% | -43.61% | 79.41 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 29 | 31.0% | +3451.76% | -43.71% | 78.97 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 18 | 50.0% | +3348.87% | -26.30% | 127.35 | 🔴 **284 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 37 | 29.7% | +3279.28% | -47.68% | 68.78 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 44 | 27.3% | +3122.83% | -52.86% | 59.07 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 31 | 35.5% | +5226.36% | -34.93% | 149.63 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 18 | 50.0% | +3348.87% | -26.30% | 127.35 | 🔴 **284 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 17 | 52.9% | +3847.93% | -35.20% | 109.30 | 🔴 **284 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 42 | 28.6% | +4521.47% | -51.31% | 88.12 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 39 | 28.2% | +3814.39% | -45.53% | 83.77 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 32 | 31.2% | +3490.14% | -43.71% | 79.85 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 30 | 36.7% | +3463.12% | -43.61% | 79.41 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 29 | 31.0% | +3451.76% | -43.71% | 78.97 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 27 | 29.6% | +2636.06% | -36.47% | 72.28 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 37 | 29.7% | +3279.28% | -47.68% | 68.78 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |

### LINKUSDT (1 Day)

- **File sumber:** `linkusdt_1d.csv`
- **Total candle:** 2729
- **Buy & Hold:** +1538.61%
- **Rekomendasi (return tertinggi):** EMA `5/100` → Return +1614.49%, MaxDD -71.67%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **49 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 100 | 27 | 37.0% | +1614.49% | -71.67% | 22.53 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 35 | 34.3% | +1375.37% | -76.61% | 17.95 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 45 | 31.1% | +1347.77% | -64.33% | 20.95 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 43 | 37.2% | +1271.16% | -65.77% | 19.33 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 39.3% | +1211.31% | -62.79% | 19.29 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 12 | 26 | 42 | 35.7% | +1187.78% | -74.26% | 16.00 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 44 | 36.4% | +1179.84% | -77.52% | 15.22 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 88 | 31.8% | +1136.04% | -71.13% | 15.97 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 25 | 100 | 14 | 28.6% | +1112.48% | -53.83% | 20.67 | 🔴 **262 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 53 | 26.4% | +1097.85% | -57.62% | 19.05 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 100 | 27 | 37.0% | +1614.49% | -71.67% | 22.53 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 45 | 31.1% | +1347.77% | -64.33% | 20.95 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 100 | 14 | 28.6% | +1112.48% | -53.83% | 20.67 | 🔴 **262 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 43 | 37.2% | +1271.16% | -65.77% | 19.33 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 39.3% | +1211.31% | -62.79% | 19.29 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 5 | 40 | 53 | 26.4% | +1097.85% | -57.62% | 19.05 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 35 | 34.3% | +1375.37% | -76.61% | 17.95 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 42 | 35.7% | +1187.78% | -74.26% | 16.00 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 88 | 31.8% | +1136.04% | -71.13% | 15.97 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 15 | 20 | 44 | 36.4% | +1179.84% | -77.52% | 15.22 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |

### LTCUSDT (1 Day)

- **File sumber:** `ltcusdt_1d.csv`
- **Total candle:** 3128
- **Buy & Hold:** -84.54%
- **Rekomendasi (return tertinggi):** EMA `15/40` → Return +209.25%, MaxDD -56.14%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **47 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 33 | 36.4% | +209.25% | -56.14% | 3.73 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 39 | 25.6% | +190.20% | -65.68% | 2.90 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 50 | 32 | 31.2% | +179.18% | -49.50% | 3.62 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 27 | 25.9% | +135.94% | -52.14% | 2.61 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 39 | 25.6% | +134.28% | -62.38% | 2.15 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 43 | 32.6% | +130.87% | -61.04% | 2.14 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 16 | 37.5% | +128.12% | -61.27% | 2.09 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 75 | 19 | 31.6% | +122.96% | -61.82% | 1.99 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 100 | 18 | 33.3% | +110.24% | -63.59% | 1.73 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 24 | 29.2% | +108.64% | -58.21% | 1.87 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 33 | 36.4% | +209.25% | -56.14% | 3.73 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 50 | 32 | 31.2% | +179.18% | -49.50% | 3.62 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 39 | 25.6% | +190.20% | -65.68% | 2.90 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 27 | 25.9% | +135.94% | -52.14% | 2.61 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 39 | 25.6% | +134.28% | -62.38% | 2.15 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 43 | 32.6% | +130.87% | -61.04% | 2.14 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 16 | 37.5% | +128.12% | -61.27% | 2.09 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 75 | 19 | 31.6% | +122.96% | -61.82% | 1.99 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 24 | 29.2% | +108.64% | -58.21% | 1.87 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 100 | 18 | 33.3% | +110.24% | -63.59% | 1.73 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |

### NEARUSDT (1 Day)

- **File sumber:** `nearusdt_1d.csv`
- **Total candle:** 2092
- **Buy & Hold:** +75.70%
- **Rekomendasi (return tertinggi):** EMA `5/20` → Return +1213.32%, MaxDD -67.00%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **Hari ini** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 20 | 53 | 37.7% | +1213.32% | -67.00% | 18.11 | 🟢 **Hari ini** (BUY, masih holding) |
| 5 | 26 | 47 | 34.0% | +1196.44% | -72.03% | 16.61 | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 27 | 25.9% | +981.09% | -78.71% | 12.46 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 30 | 33.3% | +980.66% | -77.77% | 12.61 | 🔴 **12 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 41 | 31.7% | +870.03% | -73.02% | 11.92 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 28 | 28.6% | +860.41% | -76.56% | 11.24 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 31 | 35.5% | +795.79% | -78.20% | 10.18 | 🔴 **12 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 27 | 29.6% | +778.56% | -79.36% | 9.81 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 41 | 39.0% | +700.34% | -75.35% | 9.29 | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 36 | 33.3% | +684.52% | -79.80% | 8.58 | 🟢 **Hari ini** (BUY, masih holding) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 20 | 53 | 37.7% | +1213.32% | -67.00% | 18.11 | 🟢 **Hari ini** (BUY, masih holding) |
| 5 | 26 | 47 | 34.0% | +1196.44% | -72.03% | 16.61 | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 30 | 33.3% | +980.66% | -77.77% | 12.61 | 🔴 **12 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 27 | 25.9% | +981.09% | -78.71% | 12.46 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 41 | 31.7% | +870.03% | -73.02% | 11.92 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 28 | 28.6% | +860.41% | -76.56% | 11.24 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 31 | 35.5% | +795.79% | -78.20% | 10.18 | 🔴 **12 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 27 | 29.6% | +778.56% | -79.36% | 9.81 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 41 | 39.0% | +700.34% | -75.35% | 9.29 | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 27 | 29.6% | +681.83% | -77.10% | 8.84 | 🔴 **10 hari lalu** (SELL, menunggu sinyal beli) |

### PAXGUSDT (1 Day)

- **File sumber:** `paxgusdt_1d.csv`
- **Total candle:** 2139
- **Buy & Hold:** +109.91%
- **Rekomendasi (return tertinggi):** EMA `20/150` → Return +130.22%, MaxDD -8.78%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **50 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 20 | 150 | 6 | 50.0% | +130.22% | -8.78% | 14.84 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 100 | 7 | 42.9% | +123.21% | -12.98% | 9.49 | 🔴 **75 hari lalu** (SELL, menunggu sinyal beli) |
| 40 | 75 | 6 | 50.0% | +121.76% | -12.34% | 9.87 | 🔴 **98 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 150 | 6 | 33.3% | +120.47% | -8.33% | 14.47 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 6 | 50.0% | +120.20% | -8.83% | 13.61 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 150 | 6 | 33.3% | +119.26% | -8.95% | 13.33 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 150 | 11 | 36.4% | +119.16% | -9.47% | 12.59 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 6 | 50.0% | +119.13% | -8.68% | 13.72 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 200 | 6 | 50.0% | +118.23% | -9.49% | 12.46 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 150 | 10 | 30.0% | +117.75% | -10.41% | 11.31 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 30 | 75 | 8 | 50.0% | +117.39% | -7.75% | 15.15 | 🔴 **102 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 150 | 6 | 50.0% | +130.22% | -8.78% | 14.84 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 150 | 6 | 33.3% | +120.47% | -8.33% | 14.47 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 6 | 50.0% | +119.13% | -8.68% | 13.72 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 27 | 37.0% | +103.60% | -7.56% | 13.70 | 🔴 **76 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 75 | 16 | 43.8% | +110.35% | -8.10% | 13.62 | 🔴 **108 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 6 | 50.0% | +120.20% | -8.83% | 13.61 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 24 | 33.3% | +104.88% | -7.77% | 13.50 | 🔴 **110 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 150 | 6 | 33.3% | +119.26% | -8.95% | 13.33 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 15 | 46.7% | +106.93% | -8.03% | 13.31 | 🔴 **108 hari lalu** (SELL, menunggu sinyal beli) |

### SOLUSDT (1 Day)

- **File sumber:** `solusdt_1d.csv`
- **Total candle:** 2156
- **Buy & Hold:** +2384.16%
- **Rekomendasi (return tertinggi):** EMA `9/26` → Return +19548.22%, MaxDD -44.22%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **5 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 26 | 37 | 35.1% | +19548.22% | -44.22% | 442.09 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 20 | 150 | 7 | 42.9% | +15636.48% | -25.67% | 609.02 | 🔴 **245 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 42 | 33.3% | +15111.87% | -47.32% | 319.35 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 15 | 20 | 30 | 36.7% | +14579.68% | -42.23% | 345.23 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 12 | 20 | 39 | 35.9% | +14470.05% | -49.84% | 290.31 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 10 | 26 | 35 | 31.4% | +14397.21% | -44.00% | 327.24 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 8 | 30 | 35 | 31.4% | +12914.79% | -55.30% | 233.55 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 5 | 30 | 47 | 27.7% | +11858.78% | -57.19% | 207.34 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 10 | 20 | 43 | 32.6% | +11755.68% | -59.57% | 197.34 | 🟢 **6 hari lalu** (BUY, masih holding) |
| 8 | 150 | 14 | 35.7% | +11095.73% | -32.25% | 344.00 | 🔴 **248 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 20 | 150 | 7 | 42.9% | +15636.48% | -25.67% | 609.02 | 🔴 **245 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 37 | 35.1% | +19548.22% | -44.22% | 442.09 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 25 | 150 | 8 | 37.5% | +10725.07% | -29.91% | 358.62 | 🔴 **244 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 150 | 14 | 35.7% | +10982.59% | -31.29% | 351.03 | 🔴 **248 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 30 | 36.7% | +14579.68% | -42.23% | 345.23 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 8 | 150 | 14 | 35.7% | +11095.73% | -32.25% | 344.00 | 🔴 **248 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 150 | 7 | 42.9% | +10803.29% | -31.57% | 342.18 | 🔴 **243 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 35 | 31.4% | +14397.21% | -44.00% | 327.24 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 10 | 150 | 14 | 35.7% | +10191.77% | -31.15% | 327.16 | 🔴 **248 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 42 | 33.3% | +15111.87% | -47.32% | 319.35 | 🟢 **5 hari lalu** (BUY, masih holding) |

### SUIUSDT (1 Day)

- **File sumber:** `suiusdt_1d.csv`
- **Total candle:** 1161
- **Buy & Hold:** -46.50%
- **Rekomendasi (return tertinggi):** EMA `5/50` → Return +646.47%, MaxDD -51.10%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **40 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 50 | 12 | 25.0% | +646.47% | -51.10% | 12.65 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 8 | 37.5% | +634.96% | -45.79% | 13.87 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 11 | 27.3% | +634.09% | -49.42% | 12.83 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 14 | 28.6% | +619.83% | -47.17% | 13.14 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 40 | 8 | 37.5% | +581.39% | -40.97% | 14.19 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 11 | 27.3% | +536.57% | -50.05% | 10.72 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 9 | 33.3% | +529.40% | -46.40% | 11.41 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 12 | 25.0% | +484.01% | -51.90% | 9.33 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 50 | 9 | 22.2% | +472.10% | -43.90% | 10.75 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 9 | 33.3% | +472.08% | -44.27% | 10.66 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 8 | 37.5% | +581.39% | -40.97% | 14.19 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 8 | 37.5% | +634.96% | -45.79% | 13.87 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 14 | 28.6% | +619.83% | -47.17% | 13.14 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 11 | 27.3% | +634.09% | -49.42% | 12.83 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 50 | 12 | 25.0% | +646.47% | -51.10% | 12.65 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 7 | 28.6% | +470.51% | -38.92% | 12.09 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 9 | 33.3% | +529.40% | -46.40% | 11.41 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 9 | 33.3% | +446.77% | -40.95% | 10.91 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 50 | 9 | 22.2% | +472.10% | -43.90% | 10.75 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 11 | 27.3% | +536.57% | -50.05% | 10.72 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |

### TRXUSDT (1 Day)

- **File sumber:** `trxusdt_1d.csv`
- **Total candle:** 2948
- **Buy & Hold:** +581.20%
- **Rekomendasi (return tertinggi):** EMA `12/30` → Return +1222.82%, MaxDD -43.96%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **33 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 41 | 39.0% | +1222.82% | -43.96% | 27.81 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 61 | 41.0% | +1050.20% | -38.57% | 27.23 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 53 | 41.5% | +1007.14% | -47.27% | 21.31 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 50 | 38.0% | +1005.38% | -53.45% | 18.81 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 64 | 40.6% | +951.64% | -39.74% | 23.95 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 52 | 42.3% | +910.94% | -46.01% | 19.80 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 41 | 39.0% | +873.59% | -47.25% | 18.49 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 48 | 41.7% | +868.70% | -50.94% | 17.05 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 55 | 34.5% | +825.51% | -52.65% | 15.68 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 59 | 39.0% | +811.66% | -46.24% | 17.55 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 41 | 39.0% | +1222.82% | -43.96% | 27.81 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 61 | 41.0% | +1050.20% | -38.57% | 27.23 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 64 | 40.6% | +951.64% | -39.74% | 23.95 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 75 | 26 | 50.0% | +797.96% | -37.28% | 21.41 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 53 | 41.5% | +1007.14% | -47.27% | 21.31 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 20 | 45.0% | +718.26% | -36.15% | 19.87 | 🔴 **26 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 24 | 45.8% | +764.58% | -38.57% | 19.82 | 🔴 **27 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 52 | 42.3% | +910.94% | -46.01% | 19.80 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 75 | 26 | 46.2% | +694.93% | -35.61% | 19.51 | 🔴 **29 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 50 | 38.0% | +1005.38% | -53.45% | 18.81 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |

### UNIUSDT (1 Day)

- **File sumber:** `uniusdt_1d.csv`
- **Total candle:** 2119
- **Buy & Hold:** -8.11%
- **Rekomendasi (return tertinggi):** EMA `25/26` → Return +1284.83%, MaxDD -35.67%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **1 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 26 | 18 | 44.4% | +1284.83% | -35.67% | 36.02 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 15 | 40 | 20 | 40.0% | +893.33% | -45.23% | 19.75 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 20 | 30 | 22 | 36.4% | +856.12% | -37.61% | 22.76 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 12 | 50 | 21 | 33.3% | +675.23% | -49.67% | 13.59 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 20 | 26 | 27 | 25.9% | +658.70% | -48.50% | 13.58 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 25 | 30 | 18 | 33.3% | +647.10% | -53.19% | 12.17 | 🟢 **Hari ini** (BUY, masih holding) |
| 12 | 40 | 24 | 29.2% | +628.40% | -45.45% | 13.83 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 20 | 40 | 17 | 29.4% | +570.69% | -60.34% | 9.46 | 🟢 **Hari ini** (BUY, masih holding) |
| 9 | 50 | 23 | 34.8% | +541.82% | -46.83% | 11.57 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 15 | 30 | 26 | 38.5% | +536.18% | -45.79% | 11.71 | 🟢 **3 hari lalu** (BUY, masih holding) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 26 | 18 | 44.4% | +1284.83% | -35.67% | 36.02 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 20 | 30 | 22 | 36.4% | +856.12% | -37.61% | 22.76 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 15 | 40 | 20 | 40.0% | +893.33% | -45.23% | 19.75 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 12 | 40 | 24 | 29.2% | +628.40% | -45.45% | 13.83 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 12 | 50 | 21 | 33.3% | +675.23% | -49.67% | 13.59 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 20 | 26 | 27 | 25.9% | +658.70% | -48.50% | 13.58 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 25 | 30 | 18 | 33.3% | +647.10% | -53.19% | 12.17 | 🟢 **Hari ini** (BUY, masih holding) |
| 15 | 30 | 26 | 38.5% | +536.18% | -45.79% | 11.71 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 9 | 50 | 23 | 34.8% | +541.82% | -46.83% | 11.57 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 15 | 26 | 27 | 29.6% | +440.15% | -44.77% | 9.83 | 🟢 **3 hari lalu** (BUY, masih holding) |

### XLMUSDT (1 Day)

- **File sumber:** `xlmusdt_1d.csv`
- **Total candle:** 2959
- **Buy & Hold:** -32.33%
- **Rekomendasi (return tertinggi):** EMA `5/30` → Return +410.08%, MaxDD -62.84%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **3 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 30 | 61 | 31.1% | +410.08% | -62.84% | 6.53 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 5 | 20 | 79 | 29.1% | +282.51% | -66.91% | 4.22 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 5 | 150 | 21 | 33.3% | +208.90% | -48.00% | 4.35 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 5 | 26 | 74 | 28.4% | +158.09% | -67.59% | 2.34 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 8 | 26 | 57 | 28.1% | +151.11% | -69.07% | 2.19 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 9 | 150 | 18 | 22.2% | +140.02% | -50.64% | 2.76 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 8 | 150 | 19 | 21.1% | +129.53% | -55.82% | 2.32 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 10 | 150 | 18 | 27.8% | +119.19% | -49.88% | 2.39 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 5 | 200 | 24 | 20.8% | +118.89% | -49.84% | 2.39 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 9 | 20 | 65 | 27.7% | +113.58% | -66.36% | 1.71 | 🟢 **2 hari lalu** (BUY, masih holding) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 30 | 61 | 31.1% | +410.08% | -62.84% | 6.53 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 5 | 150 | 21 | 33.3% | +208.90% | -48.00% | 4.35 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 5 | 20 | 79 | 29.1% | +282.51% | -66.91% | 4.22 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 9 | 150 | 18 | 22.2% | +140.02% | -50.64% | 2.76 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 10 | 150 | 18 | 27.8% | +119.19% | -49.88% | 2.39 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 5 | 200 | 24 | 20.8% | +118.89% | -49.84% | 2.39 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 5 | 26 | 74 | 28.4% | +158.09% | -67.59% | 2.34 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 8 | 150 | 19 | 21.1% | +129.53% | -55.82% | 2.32 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 8 | 26 | 57 | 28.1% | +151.11% | -69.07% | 2.19 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 9 | 20 | 65 | 27.7% | +113.58% | -66.36% | 1.71 | 🟢 **2 hari lalu** (BUY, masih holding) |

### XMRUSD (1 Day)

- **File sumber:** `xmrusd_daily_kraken.csv`
- **Total candle:** 724
- **Buy & Hold:** +103.11%
- **Rekomendasi (return tertinggi):** EMA `12/20` → Return +167.80%, MaxDD -10.63%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **42 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 20 | 10 | 50.0% | +167.80% | -10.63% | 15.78 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 11 | 45.5% | +164.23% | -9.43% | 17.42 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 8 | 50.0% | +142.38% | -11.89% | 11.97 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 12 | 58.3% | +138.26% | -9.03% | 15.32 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 10 | 50.0% | +138.24% | -9.43% | 14.66 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 12 | 41.7% | +137.38% | -10.26% | 13.39 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 40 | 8 | 50.0% | +137.22% | -11.89% | 11.54 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 7 | 57.1% | +135.59% | -16.67% | 8.14 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 12 | 41.7% | +127.87% | -9.40% | 13.61 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 9 | 44.4% | +121.99% | -10.55% | 11.56 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 8 | 26 | 11 | 45.5% | +164.23% | -9.43% | 17.42 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 10 | 50.0% | +167.80% | -10.63% | 15.78 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 12 | 58.3% | +138.26% | -9.03% | 15.32 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 150 | 3 | 66.7% | +52.95% | -3.59% | 14.76 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 10 | 50.0% | +138.24% | -9.43% | 14.66 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 12 | 41.7% | +127.87% | -9.40% | 13.61 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 12 | 41.7% | +137.38% | -10.26% | 13.39 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 8 | 50.0% | +142.38% | -11.89% | 11.97 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 12 | 33.3% | +118.62% | -10.08% | 11.76 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 9 | 44.4% | +121.99% | -10.55% | 11.56 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |

### XRPUSDT (1 Day)

- **File sumber:** `xrpusdt_1d.csv`
- **Total candle:** 2986
- **Buy & Hold:** +28.67%
- **Rekomendasi (return tertinggi):** EMA `9/200` → Return +99.26%, MaxDD -50.56%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **265 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 200 | 16 | 25.0% | +99.26% | -50.56% | 1.96 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 83 | 21.7% | +95.70% | -69.82% | 1.37 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 12 | 200 | 13 | 23.1% | +92.56% | -48.62% | 1.90 | 🔴 **263 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 200 | 10 | 30.0% | +92.12% | -47.52% | 1.94 | 🔴 **258 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 35 | 25.7% | +82.61% | -68.94% | 1.20 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 200 | 16 | 31.2% | +79.38% | -57.81% | 1.37 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 16 | 31.2% | +76.63% | -54.49% | 1.41 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 12 | 25.0% | +58.11% | -57.81% | 1.01 | 🔴 **263 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 64 | 26.6% | +53.68% | -76.57% | 0.70 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 47 | 29.8% | +49.37% | -61.78% | 0.80 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 200 | 16 | 25.0% | +99.26% | -50.56% | 1.96 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 200 | 10 | 30.0% | +92.12% | -47.52% | 1.94 | 🔴 **258 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 200 | 13 | 23.1% | +92.56% | -48.62% | 1.90 | 🔴 **263 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 16 | 31.2% | +76.63% | -54.49% | 1.41 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 200 | 16 | 31.2% | +79.38% | -57.81% | 1.37 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 83 | 21.7% | +95.70% | -69.82% | 1.37 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 20 | 30 | 35 | 25.7% | +82.61% | -68.94% | 1.20 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 12 | 25.0% | +58.11% | -57.81% | 1.01 | 🔴 **263 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 200 | 11 | 27.3% | +47.08% | -56.08% | 0.84 | 🔴 **261 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 47 | 29.8% | +49.37% | -61.78% | 0.80 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |

### ZECUSDT (1 Day)

- **File sumber:** `zecusdt_1d.csv`
- **Total candle:** 2665
- **Buy & Hold:** +721.00%
- **Rekomendasi (return tertinggi):** EMA `9/20` → Return +5594.37%, MaxDD -51.62%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **Hari ini** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 20 | 50 | 36.0% | +5594.37% | -51.62% | 108.38 | 🟢 **Hari ini** (BUY, masih holding) |
| 5 | 26 | 59 | 32.2% | +5494.26% | -75.56% | 72.71 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 8 | 20 | 52 | 34.6% | +4930.99% | -55.02% | 89.63 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 5 | 20 | 66 | 31.8% | +4126.34% | -72.86% | 56.63 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 10 | 26 | 41 | 41.5% | +3443.90% | -46.94% | 73.37 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 40 | 32 | 43.8% | +3369.27% | -57.52% | 58.57 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 51 | 41.2% | +3168.49% | -48.32% | 65.57 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 45 | 37.8% | +3130.19% | -49.71% | 62.97 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 40 | 45.0% | +3094.18% | -57.93% | 53.41 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 47 | 34.0% | +3031.20% | -48.66% | 62.30 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 20 | 50 | 36.0% | +5594.37% | -51.62% | 108.38 | 🟢 **Hari ini** (BUY, masih holding) |
| 8 | 20 | 52 | 34.6% | +4930.99% | -55.02% | 89.63 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 10 | 26 | 41 | 41.5% | +3443.90% | -46.94% | 73.37 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 26 | 59 | 32.2% | +5494.26% | -75.56% | 72.71 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 10 | 20 | 51 | 41.2% | +3168.49% | -48.32% | 65.57 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 45 | 37.8% | +3130.19% | -49.71% | 62.97 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 47 | 34.0% | +3031.20% | -48.66% | 62.30 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 39 | 46.2% | +2757.55% | -46.94% | 58.74 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 40 | 32 | 43.8% | +3369.27% | -57.52% | 58.57 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 66 | 31.8% | +4126.34% | -72.86% | 56.63 | 🟢 **2 hari lalu** (BUY, masih holding) |


<!-- BACKTEST_RESULTS_END -->

---

_Dihasilkan otomatis oleh `backtest.py`. Metodologi: dual EMA crossover, long-only,
fee dihitung di setiap entry & exit, tanpa slippage. Hasil in-sample murni --
lihat catatan walk-forward terpisah untuk validasi out-of-sample._
