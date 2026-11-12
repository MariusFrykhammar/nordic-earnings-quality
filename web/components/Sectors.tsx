"use client";
import Link from "next/link";
import { useMemo, useState } from "react";
import { COUNTRY, eurM, pct, ratio } from "@/lib/format";

export type SectorRow = {
  lei: string; name: string; country: string; sector: string; supersector: string; revenue_eur_m: number | null; ebit_margin: number | null;
  revenue_growth: number | null; cash_conversion_3y: number | null; n_flags: number; market: string | null;
};

const median = (xs: (number | null)[]) => {
  const v = xs.filter((x): x is number => x !== null && Number.isFinite(x)).sort((a, b) => a - b);
  if (!v.length) return null;
  const m = Math.floor(v.length / 2);
  return v.length % 2 ? v[m] : (v[m - 1] + v[m]) / 2;
};

export default function Sectors({ rows }: { rows: SectorRow[] }) {
  const [country, setCountry] = useState("");
  const [open, setOpen] = useState<string | null>(null);
  const groups = useMemo(() => {
    const by: Record<string, SectorRow[]> = {};
    rows.filter((r) => !country || r.country === country).forEach((r) => (by[r.supersector] ||= []).push(r));
    return Object.entries(by)
      .map(([sector, cs]) => ({
        sector, industry: cs[0].sector, cs: cs.sort((a, b) => (b.revenue_eur_m ?? 0) - (a.revenue_eur_m ?? 0)),
        n: cs.length, rev: cs.reduce((s, c) => s + (c.revenue_eur_m ?? 0), 0),
        margin: median(cs.map((c) => c.ebit_margin)), growth: median(cs.map((c) => c.revenue_growth)),
        conv: median(cs.map((c) => c.cash_conversion_3y)), flagged: cs.filter((c) => c.n_flags > 0).length / cs.length,
      }))
      .sort((a, b) => (a.sector === "Unclassified" ? 1 : b.sector === "Unclassified" ? -1 : a.industry.localeCompare(b.industry) || b.rev - a.rev));
  }, [rows, country]);

  return (
    <>
      <div className="filters">
        <label>
          Country
          <select value={country} onChange={(e) => setCountry(e.target.value)}>
            <option value="">All</option>
            {Object.entries(COUNTRY).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
          </select>
        </label>
      </div>
      <div className="table-card"><div className="table-scroll">
        <table>
          <thead>
            <tr>
              <th>Industry and supersector</th>
              <th className="r">Companies</th>
              <th className="r" title="Sum of latest-year revenue, EUR">Revenue, EUR</th>
              <th className="r" title="Median revenue growth, latest year">Median growth</th>
              <th className="r" title="Median EBIT margin, latest year">Median EBIT margin</th>
              <th className="r" title="Median of operating cash flow ÷ EBIT over three years">Median cash conversion, 3 yrs</th>
              <th className="r" title="Share of companies with at least one red flag">With a red flag</th>
            </tr>
          </thead>
          <tbody>
            {groups.map((g, i) => (
              <SectorRows showIndustry={i === 0 || groups[i - 1].industry !== g.industry} key={g.sector} g={g} open={open === g.sector} toggle={() => setOpen(open === g.sector ? null : g.sector)} country={country} />
            ))}
          </tbody>
        </table>
      </div></div>
      <p className="small muted" style={{ marginTop: 10 }}>
        Classification follows ICB. It comes from Euronext for Oslo-listed companies, otherwise from official industry
        codes (NACE) in the Norwegian and Finnish business registers mapped to ICB, then from Wikidata. Banks, insurers
        and investment companies are not ranked. Click a supersector to list its companies.
      </p>
    </>
  );
}

function SectorRows({ g, open, toggle, country, showIndustry }: { showIndustry: boolean; g: { sector: string; industry: string; cs: SectorRow[]; n: number; rev: number; margin: number | null; growth: number | null; conv: number | null; flagged: number }; open: boolean; toggle: () => void; country: string }) {
  return (
    <>
      {showIndustry && g.industry !== "Unclassified" && (
        <tr id={g.industry}><td colSpan={7} style={{ paddingTop: 18, fontWeight: 700, color: "var(--muted)", fontSize: 13 }}>{g.industry}</td></tr>
      )}
      <tr onClick={toggle} style={{ cursor: "pointer" }}>
        <td className="co"><button className="linkbtn" style={{ color: "var(--text)", textDecoration: "none", fontWeight: 600 }} aria-expanded={open}>{open ? "▾" : "▸"} {g.sector}</button></td>
        <td className="r num">{g.n}</td>
        <td className="r num">{eurM(g.rev)}</td>
        <td className="r num">{pct(g.growth, true, 1)}</td>
        <td className="r num">{pct(g.margin, false, 1)}</td>
        <td className="r num">{ratio(g.conv)}</td>
        <td className="r num">{pct(g.flagged)}</td>
      </tr>
      {open && (
        <>
          {g.cs.map((c) => (
            <tr key={c.lei} style={{ background: "#ffffff04" }}>
              <td className="co" style={{ paddingLeft: 32 }}><Link href={`/company/${c.lei}/`}>{c.name}</Link><span className="sub">{COUNTRY[c.country]}, {c.market ?? "listed"}</span></td>
              <td className="r num">{c.n_flags ? <span className="down">{c.n_flags} flag{c.n_flags > 1 ? "s" : ""}</span> : ""}</td>
              <td className="r num">{eurM(c.revenue_eur_m)}</td>
              <td className="r num">{pct(c.revenue_growth, true, 1)}</td>
              <td className="r num">{pct(c.ebit_margin, false, 1)}</td>
              <td className="r num">{ratio(c.cash_conversion_3y)}</td>
              <td className="r small"></td>
            </tr>
          ))}
          <tr><td colSpan={7} className="small"><Link href={`/?supersector=${encodeURIComponent(g.sector)}${country ? `&country=${country}` : ""}&list=flags`}>See this supersector in the ranked findings</Link></td></tr>
        </>
      )}
    </>
  );
}
