import Link from "next/link";
import type { Metadata } from "next";
import { allLeis, getCompany, getFlags, getIndex, series } from "@/lib/data";
import { COUNTRY, eurM, flagSentence } from "@/lib/format";
import { DivergenceChart } from "@/components/charts";
import FinTable from "@/components/FinTable";
import { CHECKLIST } from "@/lib/glossary";

export const dynamicParams = false;
export function generateStaticParams() {
  return allLeis().map((lei) => ({ lei }));
}

export async function generateMetadata({ params }: { params: Promise<{ lei: string }> }): Promise<Metadata> {
  const c = getCompany((await params).lei);
  return { title: `${c.display_name}: earnings quality`, description: `Profit versus operating cash flow and accounting red flags for ${c.display_name}, from official annual reports.` };
}

export default async function CompanyPage({ params }: { params: Promise<{ lei: string }> }) {
  const { lei } = await params;
  const c = getCompany(lei);
  const rules = getFlags().meta.rules;
  const latest = c.years[String(c.latest_year)];
  const cur = latest.currency;

  // peers: same sector (when classified), listed, closest in size
  const index = getIndex();
  const peers =
    c.supersector !== "Unclassified"
      ? index
          .filter((r) => r.rankable && r.supersector === c.supersector && r.lei !== c.lei && r.revenue_eur_m)
          .sort((a, b) => Math.abs(Math.log((a.revenue_eur_m ?? 1) / (c.revenue_eur_m ?? 1))) - Math.abs(Math.log((b.revenue_eur_m ?? 1) / (c.revenue_eur_m ?? 1))))
          .slice(0, 5)
      : [];

  const statusNote = !c.in_universe
    ? `Classified as ${c.sector.toLowerCase()}, so red flags are not computed: their statements are built differently.`
    : !c.rankable
      ? "Not included in the rankings (" +
        (c.listing_status.startsWith("no listed") ? "no listed shares found in ESMA's register" : c.latest_year < 2024 ? "no report since FY" + c.latest_year : "revenue below €25m") +
        "). Figures and flags are shown for reference."
      : null;

  return (
    <>
      <div className="co-head">
        <p className="eyebrow"><Link href="/">Findings</Link> <span aria-hidden="true">›</span> {COUNTRY[c.country] ?? c.country} <span aria-hidden="true">›</span> <Link href={`/sectors/#${encodeURIComponent(c.sector)}`}>{c.sector}</Link>{c.supersector !== c.sector && c.supersector !== "Unclassified" ? <> <span aria-hidden="true">›</span> {c.supersector}</> : null}</p>
        <h1>{c.display_name}</h1>
        <ul className="facts">
          <li><b>{c.equity?.venue ?? c.listing_status.replace(/^listed shares: /, "")}</b></li>
          {c.tickers.length > 0 && <li>Ticker <b>{c.tickers[0]}</b></li>}
          <li>Revenue <b className="num">{eurM(c.revenue_eur_m)}</b> FY{c.latest_year}</li>
          <li>Reports in <b>{cur}</b></li>
        </ul>
        <p className="small muted" style={{ marginTop: 10 }}>
          {c.legal_name ?? c.esef_entity_name}. LEI {c.lei}
          {c.org_number ? `, registration number ${c.org_number}` : ""}
.{" "}
          Industry classification (ICB): {c.sector}{c.supersector !== c.sector ? `, ${c.supersector}` : ""}; source: {c.sector_basis}.
        </p>
        {statusNote && <p className="small">{statusNote}</p>}
      </div>

      <section>
        <div className="co-grid">
          <div>
            <div className="card">
              <h2>Profit and cash, FY2020–FY{c.latest_year}</h2>
              <div className="key">
                <span className="p"><i />Net profit</span>
                <span className="c"><i />Operating cash flow</span>
                <span className="g"><i />Profit ahead of cash</span>
              </div>
              <DivergenceChart data={series(c)} currency={cur} />
              <p className="small muted" style={{ margin: "6px 0 0" }}>
                {cur} millions. Over time the two lines should move together; operating cash flow normally sits above net profit because depreciation is a non-cash cost. Shaded areas mark years where profit ran ahead of cash.
              </p>
            </div>
          </div>
          <aside aria-labelledby="notes" className="card">
            <h2 id="notes" style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>Review notes, FY{c.latest_year}
              <span className={"badge " + (c.flags.length ? "red" : "green")}>{c.flags.length} / 7</span></h2>
            {c.flags.length ? (
              <div>
                {c.flags.map((f) => (
                  <div className="note" key={f.flag}>
                    <h3><span className="tick" style={{ margin: 0 }} aria-hidden="true" />{f.title}</h3>
                    <p>{flagSentence(f.flag, f.evidence, c.latest_year)}</p>
                    <p className="why">Can signal: {rules[f.flag]?.signals}</p>
                    <p className="why">Innocent explanations: {rules[f.flag]?.innocent}</p>
                    {CHECKLIST[f.flag] && (
                      <details className="why small">
                        <summary style={{ cursor: "pointer" }}>What to check in the annual report</summary>
                        <ul style={{ margin: "6px 0 0", paddingLeft: 18 }}>{CHECKLIST[f.flag].map((x) => <li key={x}>{x}</li>)}</ul>
                      </details>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div>
                <p>{c.in_universe ? "None of the seven red flags is triggered in the latest year." : "Red flags are not computed for this company type."}</p>
                <p className="small"><Link href="/methodology/">What the flags test</Link></p>
              </div>
            )}
            {c.flags.length > 0 && <p className="small muted">Flags are prompts for analysis, not conclusions. Compared with {c.peer_group ?? "all non-financial companies"}.</p>}
          </aside>
        </div>
      </section>

      <section className="card">
        <h2>Financials</h2>
        <p className="small muted">Click a number to open it in the annual report. Values come from each year&apos;s own report, or from the next year&apos;s comparatives when that year has no report.</p>
        <FinTable company={c} />
      </section>

      {peers.length > 0 && (
        <section className="card">
          <h2>Compare with peers</h2>
          <p>
            Closest in size in {c.supersector}:{" "}
            {peers.map((p, i) => (
              <span key={p.lei}>
                <Link href={`/company/${p.lei}/`}>{p.name}</Link>
                {i < peers.length - 1 ? ", " : ""}
              </span>
            ))}
            .
          </p>
          <p><Link className="btn primary" href={`/compare/?c=${[c.lei, ...peers.map((p) => p.lei)].join(",")}`}>Compare these {peers.length + 1} companies</Link></p>
        </section>
      )}
    </>
  );
}
