/**
 * app.js -- render hasil backtest dari .backtest_cache/manifest.json.
 *
 * backtest.py (mode --detail) menulis manifest.json sebagai satu file JSON
 * teragregasi (bullish + bearish + metadata parameter). Skrip ini fetch
 * file itu SEKALI, lalu merender seluruh tabel di client-side. index.html
 * sendiri tidak pernah disentuh oleh backtest.py -- jadi diff git untuk
 * index.html/style.css/app.js hanya berubah kalau desain/logic tampilan
 * memang diubah, terpisah dari perubahan data (manifest.json).
 */

const MANIFEST_URL = ".backtest_cache/manifest.json";

// Label timeframe singkat, sama seperti versi Python (_build_summary_table_html)
function shortTimeframe(label) {
  if (!label || label === "-") return "-";
  return label
    .replace(" Day", "D")
    .replace(" Hour", "H")
    .replace(" Minute", "M")
    .replace(" Week", "W")
    .replace(" Month", "Mo");
}

// Sama seperti _days_label() di backtest.py: "Hari ini" untuk 0, "N hari lalu" untuk N > 0
function daysLabel(days) {
  if (days === null || days === undefined) return "-";
  const rounded = Math.round(days);
  if (rounded <= 0) return "Hari ini";
  if (rounded === 1) return "1 hari lalu";
  return `${rounded} hari lalu`;
}

function escapeHtml(val) {
  const div = document.createElement("div");
  div.textContent = String(val);
  return div.innerHTML;
}

function fmtPct(val, decimals = 1) {
  if (val === null || val === undefined) return "-";
  return `${val >= 0 ? "+" : ""}${val.toFixed(decimals)}%`;
}

function pctClass(val) {
  if (val === null || val === undefined) return "muted-num";
  return val >= 0 ? "pos-num" : "neg-num";
}

function signalBadgeHtml(row) {
  if (row.days_since_last_signal === null || row.days_since_last_signal === undefined || !row.last_signal_type) {
    return '<span class="dash">-</span>';
  }
  const cssClass = row.last_signal_type === "BUY" ? "signal-buy" : "signal-sell";
  return (
    `<span class="badge ${cssClass}">${escapeHtml(row.last_signal_type)}</span>` +
    `<span class="signal-detail">${escapeHtml(daysLabel(row.days_since_last_signal))}</span>`
  );
}

function buildTable(group) {
  const wrap = document.createElement("div");
  wrap.className = "table-wrap";

  const table = document.createElement("table");
  table.innerHTML = `
    <thead>
      <tr>
        <th>Pair</th>
        <th class="tf-col">Timeframe</th>
        <th>Sinyal Terakhir</th>
        <th class="num-col">Return</th>
        <th class="num-col">Win Rate</th>
        <th class="num-col">Trades</th>
      </tr>
    </thead>
    <tbody></tbody>
  `;

  const tbody = table.querySelector("tbody");
  for (const row of group) {
    const tr = document.createElement("tr");
    if (row.last_signal_type === "SELL") tr.className = "sell-row";

    tr.innerHTML = `
      <td class="pair">${escapeHtml(row.pair)}</td>
      <td class="tf-col muted-num">${escapeHtml(shortTimeframe(row.timeframe))}</td>
      <td>${signalBadgeHtml(row)}</td>
      <td class="num-col ${pctClass(row.total_return_pct)}">${fmtPct(row.total_return_pct)}</td>
      <td class="num-col muted-num">${row.win_rate != null ? row.win_rate.toFixed(0) + "%" : "-"}</td>
      <td class="num-col muted-num">${row.n_trades != null ? row.n_trades : "-"}</td>
    `;
    tbody.appendChild(tr);
  }

  wrap.appendChild(table);
  return wrap;
}

function buildSectionLabel(kind, count, freshnessLabel) {
  const div = document.createElement("div");
  div.className = `section-label ${kind}`;
  const title = kind === "buy" ? "Bullish" : "Bearish";
  const sigWord = kind === "buy" ? "BUY" : "SELL";
  div.innerHTML = `
    <span class="dot"></span><span class="label">${title}</span>
    <span class="count">— sinyal ${sigWord} ${escapeHtml(freshnessLabel)} (${count} pair)</span>
  `;
  return div;
}

async function render() {
  const root = document.getElementById("results-root");
  const paramsEl = document.getElementById("masthead-params");
  const generatedEl = document.getElementById("generated-at");

  let manifest;
  try {
    const res = await fetch(MANIFEST_URL, { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    manifest = await res.json();
  } catch (err) {
    root.innerHTML = `<p class="error-note">Gagal memuat manifest.json: ${escapeHtml(err.message)}. Pastikan backtest.py sudah dijalankan dengan flag --detail minimal sekali.</p>`;
    return;
  }

  const { params, bullish = [], bearish = [] } = manifest;

  // Isi masthead params dari data manifest (bukan hardcoded), supaya kalau
  // parameter MACD/fee berubah di backtest.py, tampilan otomatis ikut.
  if (paramsEl && params) {
    paramsEl.innerHTML = `
      <div><strong>Fee:</strong> ${params.fee_pct}%/sisi &nbsp;&middot;&nbsp;
      <strong>Timeframe:</strong> daily &nbsp;&middot;&nbsp;
      <strong>Mode:</strong> Spot, long-only &nbsp;&middot;&nbsp;
      <strong>MACD:</strong> ${params.fast}/${params.slow}/${params.signal}</div>
      <div class="src">Script: <a href="https://github.com/Rovikin/web/tree/main/signal/spot">github.com/Rovikin/web/signal/spot</a></div>
    `;
  }

  if (generatedEl && manifest.generated_at) {
    generatedEl.textContent = `Manifest diperbarui: ${manifest.generated_at}`;
  }

  root.innerHTML = "";

  if (bullish.length === 0 && bearish.length === 0) {
    const p = document.createElement("p");
    p.className = "empty-note";
    p.textContent = `Tidak ada pair dengan sinyal ${params?.freshness_label ?? "hari ini"}.`;
    root.appendChild(p);
    return;
  }

  if (bullish.length > 0) {
    root.appendChild(buildSectionLabel("buy", bullish.length, params?.freshness_label ?? "hari ini"));
    root.appendChild(buildTable(bullish));
  }

  if (bearish.length > 0) {
    root.appendChild(buildSectionLabel("sell", bearish.length, params?.freshness_label ?? "hari ini"));
    root.appendChild(buildTable(bearish));
  }
}

render();
