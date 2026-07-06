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

**Sinyal Terakhir** menunjukkan sudah berapa hari sejak crossover EMA terakhir terjadi pada kombinasi tersebut, dihitung sampai candle paling akhir di data (BUY = masih dalam posisi terbuka, SELL = sudah keluar dan menunggu sinyal beli berikutnya).

## Ringkasan Hasil

| Pair | Timeframe | Total Candle | EMA Terbaik | Return | Max DD | Buy & Hold | vs B&H | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|---|
| **ADAUSDT** | 1 Day | 3002 | `15/40` | +9390.82% | -34.42% | -21.89% | ✅ Menang | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| **AVAXUSDT** | 1 Day | 2113 | `15/75` | +3356.67% | -33.05% | +30.17% | ✅ Menang | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| **BCHUSDT** | 1 Day | 2412 | `25/75` | +200.06% | -55.10% | +12.41% | ✅ Menang | 🔴 **153 hari lalu** (SELL, menunggu sinyal beli) |
| **BNBUSDT** | 1 Day | 3164 | `10/26` | +30822.68% | -31.91% | +37447.42% | ❌ Kalah | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| **BTCUSDT** | 1 Day | 3245 | `10/30` | +6804.41% | -52.55% | +1385.39% | ✅ Menang | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| **DOGEUSDT** | 1 Day | 2558 | `15/26` | +18176.70% | -56.62% | +1912.09% | ✅ Menang | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| **ETHUSDT** | 1 Day | 3245 | `10/20` | +7186.33% | -46.34% | +491.27% | ✅ Menang | 🟢 **0 hari lalu** (BUY, masih holding) |
| **HBARUSDT** | 1 Day | 2472 | `12/30` | +5226.36% | -34.93% | +114.62% | ✅ Menang | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| **LINKUSDT** | 1 Day | 2728 | `5/100` | +1614.49% | -71.67% | +1547.19% | ✅ Menang | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| **LTCUSDT** | 1 Day | 3127 | `15/40` | +209.25% | -56.14% | -84.20% | ✅ Menang | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| **NEARUSDT** | 1 Day | 2091 | `5/20` | +1217.28% | -67.00% | +72.61% | ✅ Menang | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| **PAXGUSDT** | 1 Day | 2138 | `20/150` | +130.22% | -8.78% | +111.31% | ✅ Menang | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| **SOLUSDT** | 1 Day | 2155 | `9/26` | +19464.06% | -44.22% | +2373.55% | ✅ Menang | 🟢 **4 hari lalu** (BUY, masih holding) |
| **SUIUSDT** | 1 Day | 1160 | `5/50` | +646.47% | -51.10% | -46.01% | ✅ Menang | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| **TRXUSDT** | 1 Day | 2947 | `12/30` | +1222.82% | -43.96% | +580.17% | ✅ Menang | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| **UNIUSDT** | 1 Day | 2118 | `25/26` | +1282.65% | -35.67% | -8.25% | ✅ Menang | 🟢 **0 hari lalu** (BUY, masih holding) |
| **XLMUSDT** | 1 Day | 2958 | `5/30` | +418.52% | -62.23% | -31.21% | ✅ Menang | 🟢 **2 hari lalu** (BUY, masih holding) |
| **XMRUSD** | 1 Day | 723 | `12/20` | +167.80% | -10.63% | +99.12% | ✅ Menang | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| **XRPUSDT** | 1 Day | 2985 | `9/200` | +99.26% | -50.56% | +30.04% | ✅ Menang | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| **ZECUSDT** | 1 Day | 2664 | `5/26` | +5612.39% | -75.56% | +738.28% | ✅ Menang | 🟢 **0 hari lalu** (BUY, masih holding) |

## Detail per Aset

### ADAUSDT (1 Day)

- **File sumber:** `adausdt_1d.csv`
- **Total candle:** 3002
- **Buy & Hold:** -21.89%
- **Rekomendasi (return tertinggi):** EMA `15/40` → Return +9390.82%, MaxDD -34.42%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **45 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 25 | 40.0% | +9390.82% | -34.42% | 272.84 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 40 | 23 | 39.1% | +7843.51% | -38.26% | 205.03 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 21 | 42.9% | +7288.51% | -35.55% | 205.01 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 25 | 40.0% | +7048.53% | -32.34% | 217.92 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 32 | 37.5% | +6974.95% | -41.99% | 166.12 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 23 | 39.1% | +6464.02% | -42.21% | 153.15 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 20 | 50.0% | +6346.56% | -41.09% | 154.45 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 75 | 26 | 46.2% | +6326.46% | -46.12% | 137.18 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 29 | 37.9% | +6315.59% | -44.41% | 142.22 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 26 | 38.5% | +6309.51% | -37.53% | 168.10 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 25 | 40.0% | +9390.82% | -34.42% | 272.84 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 25 | 40.0% | +7048.53% | -32.34% | 217.92 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 40 | 23 | 39.1% | +7843.51% | -38.26% | 205.03 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 21 | 42.9% | +7288.51% | -35.55% | 205.01 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 75 | 14 | 50.0% | +5778.85% | -30.69% | 188.28 | 🔴 **268 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 26 | 38.5% | +6309.51% | -37.53% | 168.10 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 32 | 37.5% | +6974.95% | -41.99% | 166.12 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 20 | 50.0% | +6346.56% | -41.09% | 154.45 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 23 | 39.1% | +6464.02% | -42.21% | 153.15 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 50 | 33 | 36.4% | +5800.66% | -39.13% | 148.24 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |

### AVAXUSDT (1 Day)

- **File sumber:** `avaxusdt_1d.csv`
- **Total candle:** 2113
- **Buy & Hold:** +30.17%
- **Rekomendasi (return tertinggi):** EMA `15/75` → Return +3356.67%, MaxDD -33.05%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **51 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 75 | 13 | 38.5% | +3356.67% | -33.05% | 101.58 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 15 | 26.7% | +2538.89% | -43.16% | 58.83 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 52 | 23.1% | +2422.62% | -59.69% | 40.59 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 10 | 100 | 14 | 28.6% | +2363.80% | -41.18% | 57.40 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 14 | 28.6% | +2309.05% | -42.99% | 53.71 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 37 | 29.7% | +2145.24% | -63.60% | 33.73 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 46 | 23.9% | +2022.68% | -56.12% | 36.04 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 20 | 50 | 15 | 33.3% | +2017.64% | -42.82% | 47.12 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 41 | 29.3% | +1997.69% | -62.73% | 31.85 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 33 | 30.3% | +1977.83% | -66.26% | 29.85 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 75 | 13 | 38.5% | +3356.67% | -33.05% | 101.58 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 75 | 10 | 40.0% | +1857.34% | -29.37% | 63.24 | 🔴 **263 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 15 | 26.7% | +2538.89% | -43.16% | 58.83 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 100 | 14 | 28.6% | +2363.80% | -41.18% | 57.40 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 14 | 28.6% | +2309.05% | -42.99% | 53.71 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 50 | 15 | 33.3% | +2017.64% | -42.82% | 47.12 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 100 | 13 | 30.8% | +1540.88% | -36.86% | 41.80 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 52 | 23.1% | +2422.62% | -59.69% | 40.59 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 8 | 100 | 17 | 23.5% | +1687.99% | -43.06% | 39.20 | 🔴 **267 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 10 | 40.0% | +1252.96% | -32.01% | 39.14 | 🔴 **261 hari lalu** (SELL, menunggu sinyal beli) |

### BCHUSDT (1 Day)

- **File sumber:** `bchusdt_1d.csv`
- **Total candle:** 2412
- **Buy & Hold:** +12.41%
- **Rekomendasi (return tertinggi):** EMA `25/75` → Return +200.06%, MaxDD -55.10%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **153 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 75 | 14 | 35.7% | +200.06% | -55.10% | 3.63 | 🔴 **153 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 75 | 11 | 36.4% | +184.31% | -45.26% | 4.07 | 🔴 **152 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 19 | 31.6% | +165.26% | -55.04% | 3.00 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 100 | 12 | 41.7% | +161.33% | -37.10% | 4.35 | 🔴 **153 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 100 | 23 | 30.4% | +141.62% | -50.68% | 2.79 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 40 | 50 | 14 | 35.7% | +139.55% | -53.22% | 2.62 | 🔴 **152 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 68 | 29.4% | +116.90% | -66.39% | 1.76 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 12 | 100 | 16 | 31.2% | +109.75% | -59.95% | 1.83 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 100 | 15 | 33.3% | +101.19% | -61.63% | 1.64 | 🔴 **154 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 22 | 31.8% | +100.11% | -58.51% | 1.71 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 20 | 100 | 12 | 41.7% | +161.33% | -37.10% | 4.35 | 🔴 **153 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 75 | 11 | 36.4% | +184.31% | -45.26% | 4.07 | 🔴 **152 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 14 | 35.7% | +200.06% | -55.10% | 3.63 | 🔴 **153 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 19 | 31.6% | +165.26% | -55.04% | 3.00 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 100 | 23 | 30.4% | +141.62% | -50.68% | 2.79 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 40 | 50 | 14 | 35.7% | +139.55% | -53.22% | 2.62 | 🔴 **152 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 100 | 16 | 31.2% | +109.75% | -59.95% | 1.83 | 🔴 **155 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 68 | 29.4% | +116.90% | -66.39% | 1.76 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 12 | 75 | 22 | 31.8% | +100.11% | -58.51% | 1.71 | 🔴 **156 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 39 | 30.8% | +96.49% | -56.65% | 1.70 | 🔴 **54 hari lalu** (SELL, menunggu sinyal beli) |

### BNBUSDT (1 Day)

- **File sumber:** `bnbusdt_1d.csv`
- **Total candle:** 3164
- **Buy & Hold:** +37447.42%
- **Rekomendasi (return tertinggi):** EMA `10/26` → Return +30822.68%, MaxDD -31.91%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **31 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 26 | 46 | 45.7% | +30822.68% | -31.91% | 965.85 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 34 | 47.1% | +27733.76% | -36.73% | 755.10 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 46 | 45.7% | +26606.06% | -35.84% | 742.35 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 35 | 48.6% | +24534.25% | -36.09% | 679.71 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 41 | 46.3% | +21283.08% | -33.21% | 640.81 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 43 | 48.8% | +21137.95% | -33.13% | 638.01 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 52 | 42.3% | +20012.75% | -38.95% | 513.87 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 40 | 37 | 40.5% | +19337.91% | -43.36% | 446.01 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 47 | 46.8% | +19326.85% | -29.22% | 661.39 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 34 | 38.2% | +19029.96% | -41.94% | 453.74 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 26 | 46 | 45.7% | +30822.68% | -31.91% | 965.85 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 34 | 47.1% | +27733.76% | -36.73% | 755.10 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 46 | 45.7% | +26606.06% | -35.84% | 742.35 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 35 | 48.6% | +24534.25% | -36.09% | 679.71 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 47 | 46.8% | +19326.85% | -29.22% | 661.39 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 41 | 46.3% | +21283.08% | -33.21% | 640.81 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 43 | 48.8% | +21137.95% | -33.13% | 638.01 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 35 | 40.0% | +18432.73% | -30.15% | 611.40 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 52 | 42.3% | +20012.75% | -38.95% | 513.87 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 34 | 35.3% | +14590.54% | -30.30% | 481.60 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |

### BTCUSDT (1 Day)

- **File sumber:** `btcusdt_1d.csv`
- **Total candle:** 3245
- **Buy & Hold:** +1385.39%
- **Rekomendasi (return tertinggi):** EMA `10/30` → Return +6804.41%, MaxDD -52.55%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **44 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 30 | 44 | 38.6% | +6804.41% | -52.55% | 129.48 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 51 | 35.3% | +5336.21% | -51.68% | 103.26 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 47 | 36.2% | +4361.34% | -53.73% | 81.17 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 54 | 35.2% | +4300.59% | -57.97% | 74.19 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 58 | 34.5% | +4205.05% | -50.07% | 83.99 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 51 | 33.3% | +4198.99% | -54.14% | 77.56 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 48 | 35.4% | +4156.22% | -53.26% | 78.04 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 26 | 42.3% | +4052.75% | -38.87% | 104.28 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 42 | 38.1% | +3858.53% | -48.75% | 79.14 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 63 | 34.9% | +3828.81% | -61.34% | 62.42 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 30 | 44 | 38.6% | +6804.41% | -52.55% | 129.48 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 40 | 26 | 42.3% | +4052.75% | -38.87% | 104.28 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 51 | 35.3% | +5336.21% | -51.68% | 103.26 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 50 | 23 | 43.5% | +3513.43% | -35.28% | 99.58 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 50 | 23 | 39.1% | +3002.00% | -34.93% | 85.95 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 58 | 34.5% | +4205.05% | -50.07% | 83.99 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 47 | 36.2% | +4361.34% | -53.73% | 81.17 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 50 | 25 | 40.0% | +3192.44% | -39.95% | 79.90 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 42 | 38.1% | +3858.53% | -48.75% | 79.14 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 48 | 35.4% | +4156.22% | -53.26% | 78.04 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |

### DOGEUSDT (1 Day)

- **File sumber:** `dogeusdt_1d.csv`
- **Total candle:** 2558
- **Buy & Hold:** +1912.09%
- **Rekomendasi (return tertinggi):** EMA `15/26` → Return +18176.70%, MaxDD -56.62%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **40 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 26 | 30 | 36.7% | +18176.70% | -56.62% | 321.00 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 23 | 34.8% | +17991.17% | -52.04% | 345.72 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 46 | 34.8% | +16696.92% | -60.88% | 274.27 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 26 | 42.3% | +16563.15% | -61.03% | 271.40 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 34 | 35.3% | +15384.36% | -56.27% | 273.41 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 36 | 38.9% | +15257.06% | -56.74% | 268.92 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 35 | 37.1% | +14712.45% | -54.26% | 271.13 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 50 | 36 | 33.3% | +14527.90% | -56.75% | 256.01 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 33 | 36.4% | +14293.26% | -58.29% | 245.19 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 26 | 34.6% | +14266.58% | -62.14% | 229.60 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 30 | 23 | 34.8% | +17991.17% | -52.04% | 345.72 | 🔴 **35 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 30 | 36.7% | +18176.70% | -56.62% | 321.00 | 🔴 **40 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 46 | 34.8% | +16696.92% | -60.88% | 274.27 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 34 | 35.3% | +15384.36% | -56.27% | 273.41 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 26 | 42.3% | +16563.15% | -61.03% | 271.40 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 35 | 37.1% | +14712.45% | -54.26% | 271.13 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 36 | 38.9% | +15257.06% | -56.74% | 268.92 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 50 | 36 | 33.3% | +14527.90% | -56.75% | 256.01 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 37 | 43.2% | +13992.38% | -55.59% | 251.72 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 33 | 36.4% | +14293.26% | -58.29% | 245.19 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |

### ETHUSDT (1 Day)

- **File sumber:** `ethusdt_1d.csv`
- **Total candle:** 3245
- **Buy & Hold:** +491.27%
- **Rekomendasi (return tertinggi):** EMA `10/20` → Return +7186.33%, MaxDD -46.34%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **0 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 20 | 56 | 37.5% | +7186.33% | -46.34% | 155.08 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 20 | 26 | 36 | 38.9% | +6260.66% | -46.42% | 134.88 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 37.7% | +5897.62% | -45.00% | 131.06 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 9 | 20 | 61 | 36.1% | +5845.37% | -49.98% | 116.96 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 12 | 20 | 52 | 38.5% | +5753.00% | -44.52% | 129.22 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 54 | 37.0% | +5522.86% | -53.09% | 104.03 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 40 | 23 | 39.1% | +5079.37% | -38.45% | 132.09 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 34 | 41.2% | +5021.73% | -34.45% | 145.77 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 79 | 32.9% | +4798.05% | -49.33% | 97.27 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 15 | 30 | 36 | 44.4% | +4523.11% | -39.14% | 115.56 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 10 | 20 | 56 | 37.5% | +7186.33% | -46.34% | 155.08 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 20 | 30 | 34 | 41.2% | +5021.73% | -34.45% | 145.77 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 36 | 41.7% | +4185.67% | -31.02% | 134.92 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 36 | 38.9% | +6260.66% | -46.42% | 134.88 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 40 | 23 | 39.1% | +5079.37% | -38.45% | 132.09 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 37.7% | +5897.62% | -45.00% | 131.06 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 12 | 20 | 52 | 38.5% | +5753.00% | -44.52% | 129.22 | 🔴 **51 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 61 | 36.1% | +5845.37% | -49.98% | 116.96 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 15 | 30 | 36 | 44.4% | +4523.11% | -39.14% | 115.56 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 50 | 22 | 40.9% | +4329.65% | -40.37% | 107.26 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |

### HBARUSDT (1 Day)

- **File sumber:** `hbarusdt_1d.csv`
- **Total candle:** 2472
- **Buy & Hold:** +114.62%
- **Rekomendasi (return tertinggi):** EMA `12/30` → Return +5226.36%, MaxDD -34.93%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **32 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 31 | 35.5% | +5226.36% | -34.93% | 149.63 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 42 | 28.6% | +4521.47% | -51.31% | 88.12 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 17 | 52.9% | +3847.93% | -35.20% | 109.30 | 🔴 **283 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 39 | 28.2% | +3814.39% | -45.53% | 83.77 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 32 | 31.2% | +3490.14% | -43.71% | 79.85 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 30 | 36.7% | +3463.12% | -43.61% | 79.41 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 29 | 31.0% | +3451.76% | -43.71% | 78.97 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 18 | 50.0% | +3348.87% | -26.30% | 127.35 | 🔴 **283 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 37 | 29.7% | +3279.28% | -47.68% | 68.78 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 44 | 27.3% | +3122.83% | -52.86% | 59.07 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 31 | 35.5% | +5226.36% | -34.93% | 149.63 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 18 | 50.0% | +3348.87% | -26.30% | 127.35 | 🔴 **283 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 17 | 52.9% | +3847.93% | -35.20% | 109.30 | 🔴 **283 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 42 | 28.6% | +4521.47% | -51.31% | 88.12 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 39 | 28.2% | +3814.39% | -45.53% | 83.77 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 32 | 31.2% | +3490.14% | -43.71% | 79.85 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 30 | 36.7% | +3463.12% | -43.61% | 79.41 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 29 | 31.0% | +3451.76% | -43.71% | 78.97 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 27 | 29.6% | +2636.06% | -36.47% | 72.28 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 37 | 29.7% | +3279.28% | -47.68% | 68.78 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |

### LINKUSDT (1 Day)

- **File sumber:** `linkusdt_1d.csv`
- **Total candle:** 2728
- **Buy & Hold:** +1547.19%
- **Rekomendasi (return tertinggi):** EMA `5/100` → Return +1614.49%, MaxDD -71.67%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **48 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 100 | 27 | 37.0% | +1614.49% | -71.67% | 22.53 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 35 | 34.3% | +1375.37% | -76.61% | 17.95 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 45 | 31.1% | +1347.77% | -64.33% | 20.95 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 43 | 37.2% | +1271.16% | -65.77% | 19.33 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 39.3% | +1218.20% | -62.79% | 19.40 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 12 | 26 | 42 | 35.7% | +1187.78% | -74.26% | 16.00 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 44 | 36.4% | +1179.84% | -77.52% | 15.22 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 88 | 33.0% | +1142.53% | -71.13% | 16.06 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 25 | 100 | 14 | 28.6% | +1112.48% | -53.83% | 20.67 | 🔴 **261 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 53 | 26.4% | +1097.85% | -57.62% | 19.05 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 100 | 27 | 37.0% | +1614.49% | -71.67% | 22.53 | 🔴 **48 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 45 | 31.1% | +1347.77% | -64.33% | 20.95 | 🔴 **43 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 100 | 14 | 28.6% | +1112.48% | -53.83% | 20.67 | 🔴 **261 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 61 | 39.3% | +1218.20% | -62.79% | 19.40 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 10 | 30 | 43 | 37.2% | +1271.16% | -65.77% | 19.33 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 53 | 26.4% | +1097.85% | -57.62% | 19.05 | 🔴 **44 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 35 | 34.3% | +1375.37% | -76.61% | 17.95 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 88 | 33.0% | +1142.53% | -71.13% | 16.06 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 12 | 26 | 42 | 35.7% | +1187.78% | -74.26% | 16.00 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 44 | 36.4% | +1179.84% | -77.52% | 15.22 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |

### LTCUSDT (1 Day)

- **File sumber:** `ltcusdt_1d.csv`
- **Total candle:** 3127
- **Buy & Hold:** -84.20%
- **Rekomendasi (return tertinggi):** EMA `15/40` → Return +209.25%, MaxDD -56.14%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **46 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 33 | 36.4% | +209.25% | -56.14% | 3.73 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 39 | 25.6% | +190.20% | -65.68% | 2.90 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 50 | 32 | 31.2% | +179.18% | -49.50% | 3.62 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 27 | 25.9% | +135.94% | -52.14% | 2.61 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 39 | 25.6% | +134.28% | -62.38% | 2.15 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 43 | 32.6% | +130.87% | -61.04% | 2.14 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 16 | 37.5% | +128.12% | -61.27% | 2.09 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 75 | 19 | 31.6% | +122.96% | -61.82% | 1.99 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 100 | 18 | 33.3% | +110.24% | -63.59% | 1.73 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 24 | 29.2% | +108.64% | -58.21% | 1.87 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 33 | 36.4% | +209.25% | -56.14% | 3.73 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 50 | 32 | 31.2% | +179.18% | -49.50% | 3.62 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 39 | 25.6% | +190.20% | -65.68% | 2.90 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 50 | 27 | 25.9% | +135.94% | -52.14% | 2.61 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 39 | 25.6% | +134.28% | -62.38% | 2.15 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 43 | 32.6% | +130.87% | -61.04% | 2.14 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 75 | 16 | 37.5% | +128.12% | -61.27% | 2.09 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 75 | 19 | 31.6% | +122.96% | -61.82% | 1.99 | 🔴 **266 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 24 | 29.2% | +108.64% | -58.21% | 1.87 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 100 | 18 | 33.3% | +110.24% | -63.59% | 1.73 | 🔴 **265 hari lalu** (SELL, menunggu sinyal beli) |

### NEARUSDT (1 Day)

- **File sumber:** `nearusdt_1d.csv`
- **Total candle:** 2091
- **Buy & Hold:** +72.61%
- **Rekomendasi (return tertinggi):** EMA `5/20` → Return +1217.28%, MaxDD -67.00%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **14 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 20 | 52 | 38.5% | +1217.28% | -67.00% | 18.17 | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 26 | 47 | 34.0% | +1196.44% | -72.03% | 16.61 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 27 | 25.9% | +981.09% | -78.71% | 12.46 | 🔴 **10 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 30 | 33.3% | +980.66% | -77.77% | 12.61 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 41 | 31.7% | +870.03% | -73.02% | 11.92 | 🔴 **12 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 28 | 28.6% | +860.41% | -76.56% | 11.24 | 🔴 **10 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 31 | 35.5% | +795.79% | -78.20% | 10.18 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 27 | 29.6% | +778.56% | -79.36% | 9.81 | 🔴 **10 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 41 | 39.0% | +700.34% | -75.35% | 9.29 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 35 | 34.3% | +686.88% | -79.80% | 8.61 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 20 | 52 | 38.5% | +1217.28% | -67.00% | 18.17 | 🔴 **14 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 26 | 47 | 34.0% | +1196.44% | -72.03% | 16.61 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 30 | 30 | 33.3% | +980.66% | -77.77% | 12.61 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 27 | 25.9% | +981.09% | -78.71% | 12.46 | 🔴 **10 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 30 | 41 | 31.7% | +870.03% | -73.02% | 11.92 | 🔴 **12 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 28 | 28.6% | +860.41% | -76.56% | 11.24 | 🔴 **10 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 31 | 35.5% | +795.79% | -78.20% | 10.18 | 🔴 **11 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 27 | 29.6% | +778.56% | -79.36% | 9.81 | 🔴 **10 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 41 | 39.0% | +700.34% | -75.35% | 9.29 | 🔴 **13 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 26 | 27 | 29.6% | +681.83% | -77.10% | 8.84 | 🔴 **9 hari lalu** (SELL, menunggu sinyal beli) |

### PAXGUSDT (1 Day)

- **File sumber:** `paxgusdt_1d.csv`
- **Total candle:** 2138
- **Buy & Hold:** +111.31%
- **Rekomendasi (return tertinggi):** EMA `20/150` → Return +130.22%, MaxDD -8.78%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **49 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 20 | 150 | 6 | 50.0% | +130.22% | -8.78% | 14.84 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 100 | 7 | 42.9% | +123.21% | -12.98% | 9.49 | 🔴 **74 hari lalu** (SELL, menunggu sinyal beli) |
| 40 | 75 | 6 | 50.0% | +121.76% | -12.34% | 9.87 | 🔴 **97 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 150 | 6 | 33.3% | +120.47% | -8.33% | 14.47 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 6 | 50.0% | +120.20% | -8.83% | 13.61 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 150 | 6 | 33.3% | +119.26% | -8.95% | 13.33 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 150 | 11 | 36.4% | +119.16% | -9.47% | 12.59 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 6 | 50.0% | +119.13% | -8.68% | 13.72 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 200 | 6 | 50.0% | +118.23% | -9.49% | 12.46 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 150 | 10 | 30.0% | +117.75% | -10.41% | 11.31 | 🔴 **50 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 30 | 75 | 8 | 50.0% | +117.39% | -7.75% | 15.15 | 🔴 **101 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 150 | 6 | 50.0% | +130.22% | -8.78% | 14.84 | 🔴 **49 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 150 | 6 | 33.3% | +120.47% | -8.33% | 14.47 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 6 | 50.0% | +119.13% | -8.68% | 13.72 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 27 | 37.0% | +103.60% | -7.56% | 13.70 | 🔴 **75 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 75 | 16 | 43.8% | +110.35% | -8.10% | 13.62 | 🔴 **107 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 6 | 50.0% | +120.20% | -8.83% | 13.61 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 24 | 33.3% | +104.88% | -7.77% | 13.50 | 🔴 **109 hari lalu** (SELL, menunggu sinyal beli) |
| 30 | 150 | 6 | 33.3% | +119.26% | -8.95% | 13.33 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 75 | 15 | 46.7% | +106.93% | -8.03% | 13.31 | 🔴 **107 hari lalu** (SELL, menunggu sinyal beli) |

### SOLUSDT (1 Day)

- **File sumber:** `solusdt_1d.csv`
- **Total candle:** 2155
- **Buy & Hold:** +2373.55%
- **Rekomendasi (return tertinggi):** EMA `9/26` → Return +19464.06%, MaxDD -44.22%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **4 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 26 | 37 | 35.1% | +19464.06% | -44.22% | 440.19 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 20 | 150 | 7 | 42.9% | +15636.48% | -25.67% | 609.02 | 🔴 **244 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 42 | 33.3% | +15046.71% | -47.32% | 317.97 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 15 | 20 | 30 | 36.7% | +14516.80% | -42.23% | 343.74 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 12 | 20 | 39 | 35.9% | +14407.64% | -49.84% | 289.05 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 10 | 26 | 35 | 31.4% | +14335.11% | -44.00% | 325.83 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 8 | 30 | 35 | 31.4% | +12859.04% | -55.30% | 232.54 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 5 | 30 | 47 | 27.7% | +11807.55% | -57.19% | 206.44 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 10 | 20 | 43 | 32.6% | +11704.91% | -59.57% | 196.49 | 🟢 **5 hari lalu** (BUY, masih holding) |
| 8 | 150 | 14 | 35.7% | +11095.73% | -32.25% | 344.00 | 🔴 **247 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 20 | 150 | 7 | 42.9% | +15636.48% | -25.67% | 609.02 | 🔴 **244 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 37 | 35.1% | +19464.06% | -44.22% | 440.19 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 25 | 150 | 8 | 37.5% | +10725.07% | -29.91% | 358.62 | 🔴 **243 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 150 | 14 | 35.7% | +10982.59% | -31.29% | 351.03 | 🔴 **247 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 150 | 14 | 35.7% | +11095.73% | -32.25% | 344.00 | 🔴 **247 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 30 | 36.7% | +14516.80% | -42.23% | 343.74 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 30 | 150 | 7 | 42.9% | +10803.29% | -31.57% | 342.18 | 🔴 **242 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 150 | 14 | 35.7% | +10191.77% | -31.15% | 327.16 | 🔴 **247 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 35 | 31.4% | +14335.11% | -44.00% | 325.83 | 🟢 **4 hari lalu** (BUY, masih holding) |
| 8 | 26 | 42 | 33.3% | +15046.71% | -47.32% | 317.97 | 🟢 **4 hari lalu** (BUY, masih holding) |

### SUIUSDT (1 Day)

- **File sumber:** `suiusdt_1d.csv`
- **Total candle:** 1160
- **Buy & Hold:** -46.01%
- **Rekomendasi (return tertinggi):** EMA `5/50` → Return +646.47%, MaxDD -51.10%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **39 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 50 | 12 | 25.0% | +646.47% | -51.10% | 12.65 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 8 | 37.5% | +634.96% | -45.79% | 13.87 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 11 | 27.3% | +634.09% | -49.42% | 12.83 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 14 | 28.6% | +619.83% | -47.17% | 13.14 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 40 | 8 | 37.5% | +581.39% | -40.97% | 14.19 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 11 | 27.3% | +536.57% | -50.05% | 10.72 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 9 | 33.3% | +529.40% | -46.40% | 11.41 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 12 | 25.0% | +484.01% | -51.90% | 9.33 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 50 | 9 | 22.2% | +472.10% | -43.90% | 10.75 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 9 | 33.3% | +472.08% | -44.27% | 10.66 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 15 | 40 | 8 | 37.5% | +581.39% | -40.97% | 14.19 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 26 | 8 | 37.5% | +634.96% | -45.79% | 13.87 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 40 | 14 | 28.6% | +619.83% | -47.17% | 13.14 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 11 | 27.3% | +634.09% | -49.42% | 12.83 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 50 | 12 | 25.0% | +646.47% | -51.10% | 12.65 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 30 | 7 | 28.6% | +470.51% | -38.92% | 12.09 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 9 | 33.3% | +529.40% | -46.40% | 11.41 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 50 | 9 | 33.3% | +446.77% | -40.95% | 10.91 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 50 | 9 | 22.2% | +472.10% | -43.90% | 10.75 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 11 | 27.3% | +536.57% | -50.05% | 10.72 | 🔴 **38 hari lalu** (SELL, menunggu sinyal beli) |

### TRXUSDT (1 Day)

- **File sumber:** `trxusdt_1d.csv`
- **Total candle:** 2947
- **Buy & Hold:** +580.17%
- **Rekomendasi (return tertinggi):** EMA `12/30` → Return +1222.82%, MaxDD -43.96%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **32 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 41 | 39.0% | +1222.82% | -43.96% | 27.81 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 61 | 41.0% | +1050.20% | -38.57% | 27.23 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 53 | 41.5% | +1007.14% | -47.27% | 21.31 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 50 | 38.0% | +1005.38% | -53.45% | 18.81 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 64 | 40.6% | +951.64% | -39.74% | 23.95 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 52 | 42.3% | +910.94% | -46.01% | 19.80 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 26 | 41 | 39.0% | +873.59% | -47.25% | 18.49 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 48 | 41.7% | +868.70% | -50.94% | 17.05 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 55 | 34.5% | +825.51% | -52.65% | 15.68 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 59 | 39.0% | +811.66% | -46.24% | 17.55 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 30 | 41 | 39.0% | +1222.82% | -43.96% | 27.81 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 61 | 41.0% | +1050.20% | -38.57% | 27.23 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 64 | 40.6% | +951.64% | -39.74% | 23.95 | 🔴 **34 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 75 | 26 | 50.0% | +797.96% | -37.28% | 21.41 | 🔴 **29 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 53 | 41.5% | +1007.14% | -47.27% | 21.31 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 100 | 20 | 45.0% | +718.26% | -36.15% | 19.87 | 🔴 **25 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 75 | 24 | 45.8% | +764.58% | -38.57% | 19.82 | 🔴 **26 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 52 | 42.3% | +910.94% | -46.01% | 19.80 | 🔴 **33 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 75 | 26 | 46.2% | +694.93% | -35.61% | 19.51 | 🔴 **28 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 50 | 38.0% | +1005.38% | -53.45% | 18.81 | 🔴 **32 hari lalu** (SELL, menunggu sinyal beli) |

### UNIUSDT (1 Day)

- **File sumber:** `uniusdt_1d.csv`
- **Total candle:** 2118
- **Buy & Hold:** -8.25%
- **Rekomendasi (return tertinggi):** EMA `25/26` → Return +1282.65%, MaxDD -35.67%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **0 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 26 | 18 | 44.4% | +1282.65% | -35.67% | 35.95 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 15 | 40 | 20 | 40.0% | +891.77% | -45.23% | 19.71 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 20 | 30 | 22 | 36.4% | +854.61% | -37.71% | 22.67 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 12 | 50 | 21 | 33.3% | +674.01% | -49.67% | 13.57 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 20 | 26 | 27 | 25.9% | +657.51% | -48.58% | 13.53 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 25 | 30 | 17 | 35.3% | +649.35% | -53.19% | 12.21 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 40 | 24 | 29.2% | +627.25% | -45.45% | 13.80 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 20 | 40 | 16 | 31.2% | +572.71% | -60.34% | 9.49 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 50 | 23 | 34.8% | +540.81% | -46.83% | 11.55 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 15 | 30 | 26 | 38.5% | +535.18% | -45.87% | 11.67 | 🟢 **2 hari lalu** (BUY, masih holding) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 25 | 26 | 18 | 44.4% | +1282.65% | -35.67% | 35.95 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 20 | 30 | 22 | 36.4% | +854.61% | -37.71% | 22.67 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 15 | 40 | 20 | 40.0% | +891.77% | -45.23% | 19.71 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 12 | 40 | 24 | 29.2% | +627.25% | -45.45% | 13.80 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 12 | 50 | 21 | 33.3% | +674.01% | -49.67% | 13.57 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 20 | 26 | 27 | 25.9% | +657.51% | -48.58% | 13.53 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 25 | 30 | 17 | 35.3% | +649.35% | -53.19% | 12.21 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 26 | 38.5% | +535.18% | -45.87% | 11.67 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 9 | 50 | 23 | 34.8% | +540.81% | -46.83% | 11.55 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 15 | 26 | 27 | 29.6% | +439.30% | -44.85% | 9.79 | 🟢 **2 hari lalu** (BUY, masih holding) |

### XLMUSDT (1 Day)

- **File sumber:** `xlmusdt_1d.csv`
- **Total candle:** 2958
- **Buy & Hold:** -31.21%
- **Rekomendasi (return tertinggi):** EMA `5/30` → Return +418.52%, MaxDD -62.23%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **2 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 30 | 61 | 31.1% | +418.52% | -62.23% | 6.73 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 5 | 20 | 79 | 29.1% | +288.83% | -66.91% | 4.32 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 5 | 150 | 21 | 33.3% | +214.01% | -48.00% | 4.46 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 5 | 26 | 74 | 28.4% | +162.36% | -67.05% | 2.42 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 8 | 26 | 57 | 28.1% | +155.27% | -69.07% | 2.25 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 9 | 150 | 18 | 22.2% | +143.99% | -49.83% | 2.89 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 8 | 150 | 19 | 21.1% | +133.33% | -55.09% | 2.42 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 10 | 150 | 18 | 27.8% | +122.81% | -49.88% | 2.46 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 5 | 200 | 24 | 20.8% | +122.51% | -49.01% | 2.50 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 9 | 20 | 65 | 27.7% | +117.11% | -66.36% | 1.76 | 🟢 **1 hari lalu** (BUY, masih holding) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 30 | 61 | 31.1% | +418.52% | -62.23% | 6.73 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 5 | 150 | 21 | 33.3% | +214.01% | -48.00% | 4.46 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 5 | 20 | 79 | 29.1% | +288.83% | -66.91% | 4.32 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 9 | 150 | 18 | 22.2% | +143.99% | -49.83% | 2.89 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 5 | 200 | 24 | 20.8% | +122.51% | -49.01% | 2.50 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 10 | 150 | 18 | 27.8% | +122.81% | -49.88% | 2.46 | 🟢 **3 hari lalu** (BUY, masih holding) |
| 5 | 26 | 74 | 28.4% | +162.36% | -67.05% | 2.42 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 8 | 150 | 19 | 21.1% | +133.33% | -55.09% | 2.42 | 🟢 **2 hari lalu** (BUY, masih holding) |
| 8 | 26 | 57 | 28.1% | +155.27% | -69.07% | 2.25 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 9 | 20 | 65 | 27.7% | +117.11% | -66.36% | 1.76 | 🟢 **1 hari lalu** (BUY, masih holding) |

### XMRUSD (1 Day)

- **File sumber:** `xmrusd_daily_kraken.csv`
- **Total candle:** 723
- **Buy & Hold:** +99.12%
- **Rekomendasi (return tertinggi):** EMA `12/20` → Return +167.80%, MaxDD -10.63%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **41 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 12 | 20 | 10 | 50.0% | +167.80% | -10.63% | 15.78 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 11 | 45.5% | +164.23% | -9.43% | 17.42 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 8 | 50.0% | +142.38% | -11.89% | 11.97 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 12 | 58.3% | +138.26% | -9.03% | 15.32 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 10 | 50.0% | +138.24% | -9.43% | 14.66 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 12 | 41.7% | +137.38% | -10.26% | 13.39 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 40 | 8 | 50.0% | +137.22% | -11.89% | 11.54 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 30 | 7 | 57.1% | +135.59% | -16.67% | 8.14 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 12 | 41.7% | +127.87% | -9.40% | 13.61 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 9 | 44.4% | +121.99% | -10.55% | 11.56 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 8 | 26 | 11 | 45.5% | +164.23% | -9.43% | 17.42 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 10 | 50.0% | +167.80% | -10.63% | 15.78 | 🔴 **41 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 12 | 58.3% | +138.26% | -9.03% | 15.32 | 🔴 **42 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 150 | 3 | 66.7% | +52.95% | -3.59% | 14.76 | 🔴 **36 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 26 | 10 | 50.0% | +138.24% | -9.43% | 14.66 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 30 | 12 | 41.7% | +127.87% | -9.40% | 13.61 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 26 | 12 | 41.7% | +137.38% | -10.26% | 13.39 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 40 | 8 | 50.0% | +142.38% | -11.89% | 11.97 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 30 | 12 | 33.3% | +118.62% | -10.08% | 11.76 | 🔴 **39 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 40 | 9 | 44.4% | +121.99% | -10.55% | 11.56 | 🔴 **37 hari lalu** (SELL, menunggu sinyal beli) |

### XRPUSDT (1 Day)

- **File sumber:** `xrpusdt_1d.csv`
- **Total candle:** 2985
- **Buy & Hold:** +30.04%
- **Rekomendasi (return tertinggi):** EMA `9/200` → Return +99.26%, MaxDD -50.56%
- **Sinyal terakhir pada kombinasi ini:** 🔴 **264 hari lalu** (SELL, menunggu sinyal beli)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 200 | 16 | 25.0% | +99.26% | -50.56% | 1.96 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 83 | 21.7% | +97.79% | -69.82% | 1.40 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 12 | 200 | 13 | 23.1% | +92.56% | -48.62% | 1.90 | 🔴 **262 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 200 | 10 | 30.0% | +92.12% | -47.52% | 1.94 | 🔴 **257 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 35 | 25.7% | +82.61% | -68.94% | 1.20 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 200 | 16 | 31.2% | +79.38% | -57.81% | 1.37 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 16 | 31.2% | +76.63% | -54.49% | 1.41 | 🔴 **263 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 12 | 25.0% | +58.11% | -57.81% | 1.01 | 🔴 **262 hari lalu** (SELL, menunggu sinyal beli) |
| 9 | 20 | 64 | 26.6% | +53.68% | -76.57% | 0.70 | 🔴 **47 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 47 | 29.8% | +49.37% | -61.78% | 0.80 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 200 | 16 | 25.0% | +99.26% | -50.56% | 1.96 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 25 | 200 | 10 | 30.0% | +92.12% | -47.52% | 1.94 | 🔴 **257 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 200 | 13 | 23.1% | +92.56% | -48.62% | 1.90 | 🔴 **262 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 200 | 16 | 31.2% | +76.63% | -54.49% | 1.41 | 🔴 **263 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 83 | 21.7% | +97.79% | -69.82% | 1.40 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 8 | 200 | 16 | 31.2% | +79.38% | -57.81% | 1.37 | 🔴 **264 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 30 | 35 | 25.7% | +82.61% | -68.94% | 1.20 | 🔴 **45 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 200 | 12 | 25.0% | +58.11% | -57.81% | 1.01 | 🔴 **262 hari lalu** (SELL, menunggu sinyal beli) |
| 20 | 200 | 11 | 27.3% | +47.08% | -56.08% | 0.84 | 🔴 **260 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 30 | 47 | 29.8% | +49.37% | -61.78% | 0.80 | 🔴 **46 hari lalu** (SELL, menunggu sinyal beli) |

### ZECUSDT (1 Day)

- **File sumber:** `zecusdt_1d.csv`
- **Total candle:** 2664
- **Buy & Hold:** +738.28%
- **Rekomendasi (return tertinggi):** EMA `5/26` → Return +5612.39%, MaxDD -75.56%
- **Sinyal terakhir pada kombinasi ini:** 🟢 **0 hari lalu** (BUY, masih holding)

**Top 10 berdasarkan Total Return**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 5 | 26 | 59 | 32.2% | +5612.39% | -75.56% | 74.28 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 9 | 20 | 49 | 36.7% | +5611.51% | -51.62% | 108.71 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 52 | 34.6% | +5037.23% | -55.02% | 91.56 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 5 | 20 | 66 | 31.8% | +4215.58% | -72.86% | 57.86 | 🟢 **1 hari lalu** (BUY, masih holding) |
| 10 | 26 | 41 | 41.5% | +3443.90% | -46.94% | 73.37 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 40 | 32 | 43.8% | +3369.27% | -57.52% | 58.57 | 🔴 **29 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 51 | 41.2% | +3168.49% | -48.32% | 65.57 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 45 | 37.8% | +3130.19% | -49.71% | 62.97 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 26 | 40 | 45.0% | +3094.18% | -57.93% | 53.41 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 47 | 34.0% | +3031.20% | -48.66% | 62.30 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |

**Top 10 berdasarkan Calmar (risk-adjusted)**

| Fast | Slow | Trades | Win Rate | Return | Max DD | Calmar | Sinyal Terakhir |
|---|---|---|---|---|---|---|---|
| 9 | 20 | 49 | 36.7% | +5611.51% | -51.62% | 108.71 | 🔴 **31 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 20 | 52 | 34.6% | +5037.23% | -55.02% | 91.56 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 5 | 26 | 59 | 32.2% | +5612.39% | -75.56% | 74.28 | 🟢 **0 hari lalu** (BUY, masih holding) |
| 10 | 26 | 41 | 41.5% | +3443.90% | -46.94% | 73.37 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 10 | 20 | 51 | 41.2% | +3168.49% | -48.32% | 65.57 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 12 | 20 | 45 | 37.8% | +3130.19% | -49.71% | 62.97 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 26 | 47 | 34.0% | +3031.20% | -48.66% | 62.30 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 15 | 20 | 39 | 46.2% | +2757.55% | -46.94% | 58.74 | 🔴 **30 hari lalu** (SELL, menunggu sinyal beli) |
| 8 | 40 | 32 | 43.8% | +3369.27% | -57.52% | 58.57 | 🔴 **29 hari lalu** (SELL, menunggu sinyal beli) |
| 5 | 20 | 66 | 31.8% | +4215.58% | -72.86% | 57.86 | 🟢 **1 hari lalu** (BUY, masih holding) |


<!-- BACKTEST_RESULTS_END -->

---

_Dihasilkan otomatis oleh `backtest.py`. Metodologi: dual EMA crossover, long-only,
fee dihitung di setiap entry & exit, tanpa slippage. Hasil in-sample murni --
lihat catatan walk-forward terpisah untuk validasi out-of-sample._
