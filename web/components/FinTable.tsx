"use client";
import { useState } from "react";
import type { Company } from "@/lib/data";
import { money, pct, ratio } from "@/lib/format";
import { downloadCsv } from "./tools";

type RowDef = { key: string; label: string; kind: "flow" | "stock" | "pct" | "x" | "ratio"; src?: "values" | "metrics" };

const GROUPS: { title: string; rows: RowDef[] }[] = [
  { title: "Income and cash flow", rows: [
    { key: "revenue", label: "Revenue", kind: "flow" },
    { key: "ebit", label: "Operating profit (EBIT)", kind: "flow" },
    { key: "net_profit", label: "Net profit", kind: "flow" },
    { key: "ocf", label: "Operating cash flow", kind: "flow" },
    { key: "capex", label: "Capital expenditure", kind: "flow" },
    { key: "capex_intangible", label: "of which intangible assets", kind: "flow" },
    { key: "da", label: "Depreciation and amortisation", kind: "flow" },
  ] },
  { title: "Balance sheet", rows: [
    { key: "total_assets", label: "Total assets", kind: "stock" },
    { key: "equity", label: "Equity", kind: "stock" },
    { key: "cash", label: "Cash", kind: "stock" },
    { key: "borrowings", label: "Borrowings", kind: "stock" },
    { key: "receivables", label: "Trade receivables", kind: "stock" },
    { key: "inventories", label: "Inventories", kind: "stock" },
    { key: "goodwill_measure", label: "Goodwill", kind: "stock" },
  ] },
  { title: "Ratios", rows: [
    { key: "revenue_growth", label: "Revenue growth", kind: "pct", src: "metrics" },
    { key: "ebit_margin", label: "EBIT margin", kind: "pct", src: "metrics" },
    { key: "cash_conversion", label: "Cash conversion (OCF / EBIT)", kind: "ratio", src: "metrics" },
    { key: "accruals_ratio", label: "Accruals / average assets", kind: "pct", src: "metrics" },
    { key: "roce", label: "Return on capital employed", kind: "pct", src: "metrics" },
    { key: "equity_ratio", label: "Equity ratio", kind: "pct", src: "metrics" },
    { key: "net_debt_ebitda", label: "Net debt / EBITDA", kind: "x", src: "metrics" },
  ] },
];

export default function FinTable({ company: c }: { company: Company }) {
  const [eur, setEur] = useState(false);
  const years = Object.keys(c.years).filter((y) => Number(y) >= 2020).sort();
  const cur = c.years[String(c.latest_year)].currency;

  const val = (y: string, r: RowDef): number | null => {
    const yr = c.years[y];
    const v = (r.src === "metrics" ? yr.metrics : yr.values)[r.key];
    if (v === undefined || v === null) return null;
    if (eur && (r.kind === "flow" || r.kind === "stock")) {
      const fx = r.kind === "flow" ? yr.fx_eur_avg : yr.fx_eur_end;
      return fx ? v / fx : null;
    }
    return v;
  };
  const fmt = (v: number | null, r: RowDef) =>
    r.kind === "pct" ? pct(v, false, 1) : r.kind === "x" ? ratio(v, 1, "×") : r.kind === "ratio" ? ratio(v, 2) : money(v);
  const link = (y: string, r: RowDef) => {
    const refs = c.years[y].refs ?? {};
    const alias: Record<string, string[]> = { goodwill_measure: ["goodwill", "intangibles_incl_goodwill"], borrowings: ["borrowings_total"] };
    const ref = [r.key, ...(alias[r.key] ?? [])].map((k) => refs[k]).find(Boolean);
    return ref ? `${c.reports[ref[0]]}#f-${ref[1]}` : null;
  };

  const exportCsv = () =>
    downloadCsv(`${c.display_name.replace(/\W+/g, "-").toLowerCase()}-financials.csv`, [
      ["Metric", "Unit", ...years.map((y) => "FY" + y)],
      ...GROUPS.flatMap((g) => g.rows.map((r) => [r.label, r.kind === "flow" || r.kind === "stock" ? `${eur ? "EUR" : cur} m` : r.kind === "pct" ? "share" : "x", ...years.map((y) => val(y, r) ?? "")])),
    ]);

  return (
    <>
      <div className="filters">
        <span className="seg" role="group" aria-label="Currency">
          <button aria-pressed={!eur} onClick={() => setEur(false)}>{cur}</button>
          {cur !== "EUR" && <button aria-pressed={eur} onClick={() => setEur(true)}>EUR</button>}
        </span>
        <span className="muted small">millions{eur ? ", converted at ECB rates (year average for flows, year-end for balances)" : ""}</span>
        <span className="tools"><button className="btn" onClick={exportCsv}>Download CSV</button></span>
      </div>
      <div className="table-scroll">
        <table className="fin">
          <thead>
            <tr>
              <th>&nbsp;</th>
              {years.map((y) => <th key={y} className="r">FY{y}{c.years[y].own_report ? "" : "*"}</th>)}
            </tr>
          </thead>
          <tbody>
            {GROUPS.map((g) => (
              <FragmentGroup key={g.title} title={g.title} span={years.length + 1}>
                {g.rows.map((r) => (
                  <tr key={r.key}>
                    <td>{r.label}</td>
                    {years.map((y) => {
                      const v = val(y, r);
                      const href = r.src === "metrics" ? null : link(y, r);
                      return (
                        <td key={y} className="r num">
                          {href && v !== null ? <a href={href} target="_blank" rel="noopener noreferrer" title="Open in the annual report">{fmt(v, r)}</a> : fmt(v, r)}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </FragmentGroup>
            ))}
          </tbody>
        </table>
      </div>
      {years.some((y) => !c.years[y].own_report) && <p className="small muted">* No own report for that year in the source; figures are the comparatives in the following year&apos;s report.</p>}
      {c.years[String(c.latest_year)].bases.goodwill_basis?.includes("incl.") && <p className="small muted">Goodwill is tagged together with other intangible assets in this company&apos;s reports.</p>}
    </>
  );
}

function FragmentGroup({ title, span, children }: { title: string; span: number; children: React.ReactNode }) {
  return (
    <>
      <tr className="group"><td colSpan={span}>{title}</td></tr>
      {children}
    </>
  );
}
