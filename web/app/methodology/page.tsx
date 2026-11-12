import type { Metadata } from "next";
import { getFlags } from "@/lib/data";

export const metadata: Metadata = { title: "Methodology: earnings quality scanner" };

export default function Methodology() {
  const { meta } = getFlags();
  return (
    <section className="prose" style={{ marginTop: 0 }}>
      <h1>How the scanner works</h1>
      <p className="lede">
        Every figure comes from a listed company&apos;s official annual report. The scanner computes a few ratios and
        flags patterns that analysts usually want explained. It does not judge whether a company has done anything wrong.
      </p>

      <div className="card"><h2>Where the numbers come from</h2>
      <p>
        Listed companies in the EU and Norway publish their annual reports in a machine-readable format (ESEF), where each
        figure carries a standard accounting tag. The scanner reads the consolidated group figures from these reports via
        filings.xbrl.org, a public repository run by XBRL International, for fiscal years 2020 onward. When a value is
        missing or ambiguous it is shown as not reported rather than estimated. Each number on a company page links to the
        exact fact in the report.
      </p>
      <dl>
        {Object.entries(meta.reference_sources).map(([k, v]) => (
          <div key={k}><dt>{k}</dt><dd>{v.charAt(0).toUpperCase() + v.slice(1)}.</dd></div>
        ))}
      </dl>

      </div><div className="card"><h2>Which companies are included</h2>
      <p>
        Rankings cover non-financial companies whose shares are admitted to trading on a Nordic exchange according to
        ESMA&apos;s register, with revenue of at least €{meta.min_revenue_eur_m_for_rankings} million and an annual report for
        2024 or later. Banks, insurers and investment companies are left out because their statements work differently.
        Bond-only issuers are shown on their own pages but not ranked.
      </p>

      </div><div className="card"><h2>The seven red flags</h2>
      <p>Each flag is tested on the latest fiscal year. Where a rule mentions peers, it compares with companies in the same sector when there are at least ten of them, otherwise with all non-financial companies.</p>
      <dl>
        {Object.entries(meta.rules).map(([k, r]) => (
          <div key={k}>
            <dt>{r.title}</dt>
            <dd>{r.rule}</dd>
            <dd className="muted">Can signal: {r.signals} Innocent explanations: {r.innocent}</dd>
          </div>
        ))}
      </dl>
      <p>
        Property companies and residential developers are exempt from the profit-versus-cash, accruals, leverage,
        inventory and receivables flags, since revaluations and project inventories are part of their business model.
      </p>

      </div><div className="card"><h2>Limitations</h2>
      <p>
        Companies tag their reports differently, and some report key lines only in their own company-specific tags.
        Figures labelled &ldquo;before special items&rdquo; or &ldquo;adjusted&rdquo; are never used. Sector labels come from the
        Norwegian and Finnish business registers where available and from Wikidata otherwise; many Swedish and Danish
        companies are still unclassified. Data was last refreshed on {meta.generated}.
      </p>
      <p>Nothing on this site is investment advice. The code and data are open on GitHub.</p>
      </div>
    </section>
  );
}
