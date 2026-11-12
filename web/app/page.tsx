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
    .filter((r) => r.sector !== "Real estate" && (r.net_profit_growth ?? 0) > 0 && (r.ocf_growth ?? 0) < 0 && r.profit_cash_gap_scaled !== null)
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

  return (
    <>
      <div className="hero">
        <div>
          <h1>Where Nordic profits and cash flows part ways</h1>
          <p className="lede">
            Profit is an accounting estimate; operating cash flow is what actually came in. This scanner reads the
            official annual reports of {rank.length} listed Nordic companies and points out where the two diverge.
          </p>
          <p>
            In the latest reported year, {nGap} of them grew net profit while operating cash flow fell, and {nFlagged} trip
            at least one of seven accounting red flags. Each figure links to the exact line in the company&apos;s annual
            report.
          </p>
          <p className="small muted">
            Coverage: {Object.values(COUNTRY).join(", ")}, FY2020–FY{flags.meta.generated.slice(0, 4) === "2026" ? "2025" : "latest"}.
            Data refreshed {flags.meta.generated}. <Link href="/methodology/">How it works</Link>
          </p>
        </div>
        {hero && heroRow && (
          <figure className="hero-figure" style={{ margin: 0 }}>
            <div className="key">
              <span className="p"><i />Net profit</span>
              <span className="c"><i />Operating cash flow</span>
              <span className="g"><i />Profit ahead of cash</span>
            </div>
            <DivergenceChart data={series(hero)} currency={hero.years[String(hero.latest_year)].currency} height={280} />
            <figcaption>
              <Link className="who" href={`/company/${hero.lei}/`}>{hero.display_name}</Link>, {COUNTRY[hero.country]}:
              in FY{hero.latest_year} net profit {pct(heroRow.net_profit_growth, true)}, operating cash flow{" "}
              {pct(heroRow.ocf_growth, true)}. {hero.years[String(hero.latest_year)].currency} millions.
            </figcaption>
          </figure>
        )}
      </div>
      <section aria-labelledby="findings">
        <h2 id="findings">Findings</h2>
        <Findings rows={rows} rules={Object.fromEntries(Object.entries(flags.meta.rules).map(([k, v]) => [k, v.title]))} />
      </section>
    </>
  );
}
