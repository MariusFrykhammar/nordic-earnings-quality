"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import type { Company, IndexRow } from "@/lib/data";
import { COUNTRY, eurM, pct, ratio } from "@/lib/format";
import { BubbleChart } from "./charts";
import { downloadCsv, ShareButton } from "./tools";

const MAX = 6;

export default function Compare() {
  const [index, setIndex] = useState<IndexRow[]>([]);
  const [sel, setSel] = useState<string[]>([]);
  const [data, setData] = useState<Record<string, Company>>({});
  const [q, setQ] = useState("");

  useEffect(() => {
    fetch("/data/companies.json").then((r) => r.json()).then(setIndex);
    const c = new URLSearchParams(window.location.search).get("c");
    if (c) setSel(c.split(",").filter(Boolean).slice(0, MAX));
  }, []);
  useEffect(() => {
    window.history.replaceState(null, "", sel.length ? `?c=${sel.join(",")}` : window.location.pathname);
    sel.filter((l) => !data[l]).forEach((l) =>
      fetch(`/data/company/${l}.json`).then((r) => (r.ok ? r.json() : null)).then((d) => d && setData((x) => ({ ...x, [l]: d }))),
    );
  }, [sel]); // eslint-disable-line react-hooks/exhaustive-deps

  const matches = useMemo(() => {
    if (q.length < 2) return [];
    const s = q.toLowerCase();
    return index.filter((r) => r.in_universe && !sel.includes(r.lei) && (r.name + " " + r.legal_name).toLowerCase().includes(s)).slice(0, 12);
  }, [q, index, sel]);

  const cos = sel.map((l) => data[l]).filter(Boolean);
  const latest = (c: Company) => c.years[String(c.latest_year)];
  const bubbles = cos
    .filter((c) => latest(c).metrics.revenue_growth !== undefined && latest(c).metrics.ebit_margin !== undefined)
    .map((c) => ({ lei: c.lei, name: c.display_name, x: latest(c).metrics.revenue_growth, y: latest(c).metrics.ebit_margin, size: c.revenue_eur_m ?? 0 }));

  const ROWS: [string, (c: Company) => string | number, (c: Company) => number | null][] = [
    ["Revenue (FY, EUR)", (c) => eurM(c.revenue_eur_m), (c) => c.revenue_eur_m],
    ["Revenue growth", (c) => pct(latest(c).metrics.revenue_growth, true, 1), (c) => latest(c).metrics.revenue_growth ?? null],
    ["EBIT margin", (c) => pct(latest(c).metrics.ebit_margin, false, 1), (c) => latest(c).metrics.ebit_margin ?? null],
    ["Net margin", (c) => pct(latest(c).metrics.net_margin, false, 1), (c) => latest(c).metrics.net_margin ?? null],
    ["Cash conversion, latest year", (c) => ratio(latest(c).metrics.cash_conversion), (c) => latest(c).metrics.cash_conversion ?? null],
    ["Cash conversion, 3 years", (c) => ratio(latest(c).metrics.cash_conversion_3y), (c) => latest(c).metrics.cash_conversion_3y ?? null],
    ["Accruals / average assets", (c) => pct(latest(c).metrics.accruals_ratio, false, 1), (c) => latest(c).metrics.accruals_ratio ?? null],
    ["Return on capital employed", (c) => pct(latest(c).metrics.roce, false, 1), (c) => latest(c).metrics.roce ?? null],
    ["Net debt / EBITDA", (c) => ratio(latest(c).metrics.net_debt_ebitda, 1, "×"), (c) => latest(c).metrics.net_debt_ebitda ?? null],
    ["Red flags", (c) => c.flags.length, (c) => c.flags.length],
  ];

  return (
    <>
      <div className="picker">
        {sel.map((l) => (
          <span className="pill" key={l}>
            {data[l]?.display_name ?? index.find((r) => r.lei === l)?.name ?? l}
            <button aria-label="Remove" onClick={() => setSel(sel.filter((x) => x !== l))}>×</button>
          </span>
        ))}
        {sel.length < MAX && (
          <div className="suggest filters" style={{ margin: 0 }}>
            <input type="search" placeholder="Add a company" value={q} onChange={(e) => setQ(e.target.value)} aria-label="Add a company" />
            {matches.length > 0 && (
              <ul>
                {matches.map((m) => (
                  <li key={m.lei}>
                    <button onClick={() => { setSel([...sel, m.lei]); setQ(""); }}>
                      {m.name} <span className="muted">({COUNTRY[m.country]}, {m.sector})</span>
                    </button>
                  </li>
                ))}
              </ul>
            )}
          </div>
        )}
        {cos.length > 0 && (
          <span className="tools">
            <button className="btn" onClick={() => downloadCsv("comparison.csv", [["Metric", ...cos.map((c) => c.display_name)], ...ROWS.map(([l, , raw]) => [l, ...cos.map((c) => raw(c) ?? "")])])}>Download CSV</button>
            <ShareButton />
          </span>
        )}
      </div>

      {cos.length === 0 ? (
        <p className="muted">Search for a company above, or open a company page and use its peer comparison.</p>
      ) : (
        <>
          <div className="figure" style={{ marginBottom: 24 }}>
            <BubbleChart data={bubbles} />
            <p className="small muted" style={{ margin: "4px 0 0" }}>Latest fiscal year for each company. Circle area shows revenue in euros.</p>
          </div>
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>&nbsp;</th>
                  {cos.map((c) => <th key={c.lei} className="r"><Link href={`/company/${c.lei}/`}>{c.display_name}</Link><br /><span className="muted">FY{c.latest_year}</span></th>)}
                </tr>
              </thead>
              <tbody>
                {ROWS.map(([label, f]) => (
                  <tr key={label}>
                    <td>{label}</td>
                    {cos.map((c) => <td key={c.lei} className="r num">{f(c)}</td>)}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </>
  );
}
