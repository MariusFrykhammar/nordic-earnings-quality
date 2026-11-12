import Link from "next/link";
import type { Metadata } from "next";
import { allLeis, getCompany, getFlags, getIndex, series } from "@/lib/data";
import { COUNTRY, eurM, flagSentence } from "@/lib/format";
import { DivergenceChart } from "@/components/charts";
import FinTable from "@/components/FinTable";

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
    c.sector !== "Unclassified"
      ? index
          .filter((r) => r.rankable && r.sector === c.sector && r.lei !== c.lei && r.revenue_eur_m)
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
        <p className="small"><Link href="/">Findings</Link></p>
        <h1>{c.display_name}</h1>
        <ul className="facts">
          <li>{COUNTRY[c.country] ?? c.country}</li>
          <li>{c.equity?.venue ?? c.listing_status.replace(/^listed shares: /, "")}</li>
          <li>Sector <b>{c.sector}</b></li>
          <li>Revenue <b>{eurM(c.revenue_eur_m)}</b> (FY{c.latest_year})</li>
          <li>Reports in {cur}</li>
        </ul>
        <p className="small muted" style={{ marginTop: 8 }}>
          {c.legal_name ?? c.esef_entity_name}. LEI {c.lei}
          {c.org_number ? `, registration number ${c.org_number}` : ""}
          {c.tickers.length ? `, ticker ${c.tickers.join(", ")}` : ""}.{" "}
          Sector source: {c.sector_basis}.
        </p>
        {statusNote && <p className="small">{statusNote}</p>}
      </div>

      <section>
        <div className="co-grid">
          <div>
            <h2>Profit and cash, FY2020–FY{c.latest_year}</h2>
            <div className="figure">
              <div className="key">
                <span className="p"><i />Net profit</span>
                <span className="c"><i />Operating cash flow</span>
                <span className="g"><i />Profit ahead of cash</span>
              </div>
              <DivergenceChart data={series(c)} currency={cur} />
              <p className="small muted" style={{ margin: "4px 0 0" }}>{cur} millions. Hover a year for the values.</p>
            </div>
          </div>
          <aside aria-labelledby="notes">
            <h2 id="notes">Review notes, FY{c.latest_year}</h2>
            {c.flags.length ? (
              <div className="notes">
                {c.flags.map((f) => (
                  <div className="note" key={f.flag}>
                    <h3><span className="tick" style={{ margin: 0 }} aria-hidden="true" />{f.title}</h3>
                    <p>{flagSentence(f.flag, f.evidence, c.latest_year)}</p>
                    <p className="why">Can signal: {rules[f.flag]?.signals}</p>
                    <p className="why">Innocent explanations: {rules[f.flag]?.innocent}</p>
                  </div>
                ))}
              </div>
            ) : (
              <div className="clean">
                <p>{c.in_universe ? "None of the seven red flags is triggered in the latest year." : "Red flags are not computed for this company type."}</p>
                <p className="small"><Link href="/methodology/">What the flags test</Link></p>
              </div>
            )}
            {c.flags.length > 0 && <p className="small muted">Flags are prompts for analysis, not conclusions. Compared with {c.peer_group ?? "all non-financial companies"}.</p>}
          </aside>
        </div>
      </section>

      <section>
        <h2>Financials</h2>
        <p className="small muted">Click a number to open it in the annual report. Values come from each year&apos;s own report, or from the next year&apos;s comparatives when that year has no report.</p>
        <FinTable company={c} />
      </section>

      {peers.length > 0 && (
        <section>
          <h2>Compare with peers</h2>
          <p>
            Closest in size in {c.sector.toLowerCase()}:{" "}
            {peers.map((p, i) => (
              <span key={p.lei}>
                <Link href={`/company/${p.lei}/`}>{p.name}</Link>
                {i < peers.length - 1 ? ", " : ""}
              </span>
            ))}
            .
          </p>
          <p><Link className="btn" style={{ textDecoration: "none", display: "inline-block" }} href={`/compare/?c=${[c.lei, ...peers.map((p) => p.lei)].join(",")}`}>Compare these {peers.length + 1} companies</Link></p>
        </section>
      )}
    </>
  );
}
