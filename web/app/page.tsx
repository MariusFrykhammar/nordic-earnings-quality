import Link from "next/link";
import { getCompany, getFlags, getIndex, series } from "@/lib/data";
import { COUNTRY, pct } from "@/lib/format";
import { DivergenceChart } from "@/components/charts";
import Findings, { type Row } from "@/components/Findings";

export default function Home() {
  const index = getIndex();
  const flags = getFlags();
  const rank = index.filter((r) => r.rankable);
  const rows: Row[] = rank.map((r) => ({ ...r, spark: series(getCompany(r.lei)) }));

  // Hero: the widest profit-vs-cash gap among companies with revenue of at least €250m
  const gapList = rank
    .filter((r) => r.sector !== "Real Estate" && (r.net_profit_growth ?? 0) > 0 && (r.ocf_growth ?? 0) < 0 && r.profit_cash_gap_scaled !== null)
    .sort((a, b) => (b.profit_cash_gap_scaled ?? 0) - (a.profit_cash_gap_scaled ?? 0));
  // a clear case: sizeable company, profit growth not a base effect, and profit now above cash
  const sizeable = gapList.filter((r) => (r.revenue_eur_m ?? 0) >= 250 && (r.net_profit_growth ?? 9) <= 1);
  const heroRow =
    sizeable.find((r) => {
      const y = getCompany(r.lei).years[String(r.latest_year)].values;
      return (y.net_profit ?? 0) > (y.ocf ?? 0);
    }) ?? sizeable[0] ?? gapList[0];
  const hero = heroRow ? getCompany(heroRow.lei) : null;

  const nFlagged = rank.filter((r) => r.n_flags > 0).length;
  const nGap = gapList.length;

  const today = new Date(flags.meta.generated).toLocaleDateString("en-GB", { weekday: "long", day: "numeric", month: "long" });
  const nReports = index.length;
  return (
    <>
      <h1>Where profits and cash part ways</h1>
      <p className="lede">
        Profit is an accounting estimate; operating cash flow is what actually came in. This scanner reads the official
        annual reports of listed Nordic companies and points out where the two part ways.
      </p>
      <div className="stats">
        <div className="stat"><div className="k">Listed companies ranked</div><div className="v">{rank.length}</div><div className="s">{Object.values(COUNTRY).join(", ")}</div></div>
        <div className="stat"><div className="k">Profit up, cash down</div><div className="v down">{nGap}</div><div className="s">latest fiscal year</div></div>
        <div className="stat"><div className="k">With a red flag</div><div className="v">{nFlagged}</div><div className="s">of seven tests</div></div>
        <div className="stat"><div className="k">Data as of</div><div className="v" style={{ fontSize: 20, paddingTop: 4, fontFamily: "var(--font)", fontWeight: 600 }}>{today}</div><div className="s">{nReports.toLocaleString("en-GB")} companies, FY2020–FY2025</div></div>
      </div>
      <div className="guide">
        <div>
          <h3>What the gap means</h3>
          <p className="small muted">Profit is booked when it is earned; cash arrives when customers pay. A widening gap means more of the profit sits in receivables, inventory or other estimates.</p>
        </div>
        <div>
          <h3>What a red flag is</h3>
          <p className="small muted">Seven tests from the earnings-quality literature, each compared with sector peers. A flag is a question to ask the company, with common innocent explanations listed beside it.</p>
        </div>
        <div>
          <h3>Where the numbers come from</h3>
          <p className="small muted">Official annual reports in the EU&apos;s machine-readable format. Every figure links to the exact line in the filing. <Link href="/about/">Why this was built</Link></p>
        </div>
      </div>
      {hero && heroRow && (
        <section>
          <figure className="card hero-figure">
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap", alignItems: "baseline" }}>
              <h2 style={{ margin: 0 }}>
                <Link className="who" href={`/company/${hero.lei}/`}>{hero.display_name}</Link>
                <span className="muted" style={{ fontWeight: 400 }}> profit vs cash</span>
              </h2>
              <span className="small">
                FY{hero.latest_year}: net profit <span className="num up">{pct(heroRow.net_profit_growth, true)}</span>, operating cash flow{" "}
                <span className="num down">{pct(heroRow.ocf_growth, true)}</span>
              </span>
            </div>
            <div className="key" style={{ marginTop: 10 }}>
              <span className="p"><i />Net profit</span>
              <span className="c"><i />Operating cash flow</span>
              <span className="g"><i />Profit ahead of cash</span>
            </div>
            <div className="only-wide"><DivergenceChart data={series(hero)} currency={hero.years[String(hero.latest_year)].currency} height={300} width={1100} /></div>
            <div className="only-narrow"><DivergenceChart data={series(hero)} currency={hero.years[String(hero.latest_year)].currency} height={300} width={560} /></div>
            <figcaption>
              The largest profit-versus-cash gap among companies with revenue above €250m. {COUNTRY[hero.country]},{" "}
              {hero.years[String(hero.latest_year)].currency} millions. <Link href="/methodology/">How it works</Link>
            </figcaption>
          </figure>
        </section>
      )}
      <section aria-labelledby="findings">
        <h2 id="findings">Ranked findings</h2>
        <Findings rows={rows} rules={Object.fromEntries(Object.entries(flags.meta.rules).map(([k, v]) => [k, v.title]))} />
      </section>
    </>
  );
}
