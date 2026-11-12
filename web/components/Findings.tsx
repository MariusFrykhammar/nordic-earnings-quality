"use client";
import Link from "next/link";
import { useEffect, useMemo, useState } from "react";
import type { IndexRow } from "@/lib/data";
import { COUNTRY, eurM, pct } from "@/lib/format";
import { Spark, type Pt } from "./charts";
import { downloadCsv, ShareButton } from "./tools";

export type Row = IndexRow & { spark: Pt[] };

const TABS = [
  { id: "gap", label: "Profit up, cash down", explain: "Companies whose net profit grew while operating cash flow fell in the latest year, ranked by the size of the gap relative to the previous year's revenue (so small bases don't dominate). Property companies are left out because revaluations run through their profit." },
  { id: "flags", label: "Most red flags", explain: "Companies tripping the most of the seven accounting red flags in their latest year. Ties are ordered by the profit-versus-cash gap." },
  { id: "recv", label: "Receivables outpacing sales", explain: "Trade receivables growing faster than revenue, ranked by the difference in growth rates. Customers paying later, or revenue booked before cash, both show up here." },
] as const;
type Tab = (typeof TABS)[number]["id"];

export default function Findings({ rows, rules }: { rows: Row[]; rules: Record<string, string> }) {
  const [tab, setTab] = useState<Tab>("gap");
  const [country, setCountry] = useState("");
  const [sector, setSector] = useState("");
  const [flag, setFlag] = useState("");
  const [q, setQ] = useState("");
  const [limit, setLimit] = useState(25);

  // read shareable state from the URL once, then keep the URL in sync
  useEffect(() => {
    const p = new URLSearchParams(window.location.search);
    const t = p.get("list");
    if (t && TABS.some((x) => x.id === t)) setTab(t as Tab);
    setCountry(p.get("country") ?? "");
    setSector(p.get("sector") ?? "");
    setFlag(p.get("flag") ?? "");
    setQ(p.get("q") ?? "");
  }, []);
  useEffect(() => {
    const p = new URLSearchParams();
    if (tab !== "gap") p.set("list", tab);
    if (country) p.set("country", country);
    if (sector) p.set("sector", sector);
    if (flag) p.set("flag", flag);
    if (q) p.set("q", q);
    const s = p.toString();
    window.history.replaceState(null, "", s ? `?${s}` : window.location.pathname);
  }, [tab, country, sector, flag, q]);

  const sectors = useMemo(() => [...new Set(rows.map((r) => r.sector))].sort(), [rows]);

  const list = useMemo(() => {
    let out = rows.filter(
      (r) =>
        (!country || r.country === country) &&
        (!sector || r.sector === sector) &&
        (!flag || r.flags.includes(flag)) &&
        (!q || (r.name + " " + r.legal_name).toLowerCase().includes(q.toLowerCase())),
    );
    if (tab === "gap") {
      out = out
        .filter((r) => r.sector !== "Real estate" && (r.net_profit_growth ?? 0) > 0 && (r.ocf_growth ?? 0) < 0 && r.profit_cash_gap_scaled !== null)
        .sort((a, b) => (b.profit_cash_gap_scaled ?? 0) - (a.profit_cash_gap_scaled ?? 0));
    } else if (tab === "flags") {
      out = out.filter((r) => r.n_flags > 0).sort((a, b) => b.n_flags - a.n_flags || (b.profit_cash_gap_scaled ?? -9) - (a.profit_cash_gap_scaled ?? -9));
    } else {
      out = out
        .filter((r) => r.sector !== "Real estate" && r.receivables_growth !== null && r.revenue_growth !== null && r.receivables_growth > r.revenue_growth)
        .sort((a, b) => (b.receivables_growth! - b.revenue_growth!) - (a.receivables_growth! - a.revenue_growth!));
    }
    return out;
  }, [rows, tab, country, sector, flag, q]);

  const exportCsv = () =>
    downloadCsv(`nordic-earnings-quality-${tab}.csv`, [
      ["Company", "Legal name", "LEI", "Country", "Sector", "Market", "Fiscal year", "Revenue (EUR m)", "Net profit growth", "OCF growth", "Revenue growth", "Receivables growth", "Red flags"],
      ...list.map((r) => [r.name, r.legal_name, r.lei, r.country, r.sector, r.market ?? "", r.latest_year, r.revenue_eur_m ?? "", r.net_profit_growth ?? "", r.ocf_growth ?? "", r.revenue_growth ?? "", r.receivables_growth ?? "", r.flags.map((f) => rules[f]).join("; ")]),
    ]);

  const current = TABS.find((t) => t.id === tab)!;
  return (
    <>
      <div className="tabs" role="tablist" aria-label="Ranked lists">
        {TABS.map((t) => (
          <button key={t.id} role="tab" aria-selected={tab === t.id} onClick={() => { setTab(t.id); setLimit(25); }}>
            {t.label}
          </button>
        ))}
      </div>
      <p className="explain">{current.explain}</p>
      <div className="filters">
        <label className="sr">
          <span className="muted small">Country </span>
          <select value={country} onChange={(e) => setCountry(e.target.value)}>
            <option value="">All</option>
            {Object.entries(COUNTRY).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </label>
        <label>
          <span className="muted small">Sector </span>
          <select value={sector} onChange={(e) => setSector(e.target.value)}>
            <option value="">All</option>
            {sectors.map((s) => <option key={s}>{s}</option>)}
          </select>
        </label>
        <label>
          <span className="muted small">Red flag </span>
          <select value={flag} onChange={(e) => setFlag(e.target.value)}>
            <option value="">Any</option>
            {Object.entries(rules).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </label>
        <input type="search" placeholder="Find a company" value={q} onChange={(e) => setQ(e.target.value)} aria-label="Find a company" />
        <span className="tools">
          <button className="btn" onClick={exportCsv}>Download CSV</button>
          <ShareButton />
        </span>
      </div>
      <p className="small muted">{list.length} companies</p>
      <div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th className="rank">#</th>
              <th>Company</th>
              <th>Profit vs cash, 2020–</th>
              {tab === "recv" ? (
                <>
                  <th className="r">Receivables</th>
                  <th className="r">Revenue</th>
                </>
              ) : (
                <>
                  <th className="r">Net profit</th>
                  <th className="r">Operating cash flow</th>
                </>
              )}
              <th className="r">Revenue</th>
              <th>Red flags</th>
            </tr>
          </thead>
          <tbody>
            {list.slice(0, limit).map((r, i) => (
              <tr key={r.lei}>
                <td className="rank num">{i + 1}</td>
                <td className="co">
                  <Link href={`/company/${r.lei}/`}>{r.name}</Link>
                  <span className="sub">{COUNTRY[r.country]}, {r.market ?? "listed"}, FY{r.latest_year}</span>
                </td>
                <td><Spark data={r.spark} /></td>
                {tab === "recv" ? (
                  <>
                    <td className="r num">{pct(r.receivables_growth, true)}</td>
                    <td className="r num">{pct(r.revenue_growth, true)}</td>
                  </>
                ) : (
                  <>
                    <td className="r num">{pct(r.net_profit_growth, true)}</td>
                    <td className={"r num" + ((r.ocf_growth ?? 0) < 0 ? " neg" : "")}>{pct(r.ocf_growth, true)}</td>
                  </>
                )}
                <td className="r num">{eurM(r.revenue_eur_m)}</td>
                <td>{r.flags.length ? r.flags.map((f) => <span key={f} className="tick">{rules[f]}</span>) : <span className="muted small">None</span>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {list.length === 0 && <p className="muted">No companies match these filters. Clear a filter to see more.</p>}
      {list.length > limit && (
        <p><button className="btn" onClick={() => setLimit(limit + 50)}>Show {Math.min(50, list.length - limit)} more</button></p>
      )}
      <p className="small muted">Growth rates compare the latest fiscal year with the one before. Lines show net profit (blue) and operating cash flow (ochre) for each year since 2020.</p>
    </>
  );
}
