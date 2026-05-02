type MetricSummary = {
  domain: string;
  system_name: string;
  metric_name: string;
  unit: string;
  n_records: number;
  avg_value: number;
  min_value: number;
  max_value: number;
};

const sampleData: MetricSummary[] = [
  { domain: "infrastructure", system_name: "Water Distribution Grid", metric_name: "flow_rate", unit: "l_per_s", n_records: 2, avg_value: 100.35, min_value: 98.2, max_value: 102.5 },
  { domain: "infrastructure", system_name: "Energy Grid", metric_name: "load", unit: "MW", n_records: 2, avg_value: 443.6, min_value: 430.0, max_value: 457.2 }
];

function renderTable(rows: MetricSummary[]): string {
  const body = rows
    .map(row => `<tr><td>${row.domain}</td><td>${row.system_name}</td><td>${row.metric_name}</td><td>${row.avg_value}</td><td>${row.unit}</td></tr>`)
    .join("");

  return `<table>
    <thead><tr><th>Domain</th><th>System</th><th>Metric</th><th>Average</th><th>Unit</th></tr></thead>
    <tbody>${body}</tbody>
  </table>`;
}

document.addEventListener("DOMContentLoaded", () => {
  const app = document.getElementById("app");
  if (app) {
    app.innerHTML = `<h1>Data Systems Metric Summary</h1>${renderTable(sampleData)}`;
  }
});
