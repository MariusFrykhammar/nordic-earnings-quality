import type { Metadata } from "next";
import Link from "next/link";
import { getFlags, getIndex } from "@/lib/data";

export const metadata: Metadata = { title: "About: earnings quality scanner" };

export default function About() {
  const meta = getFlags().meta;
  const index = getIndex();
  const ranked = index.filter((r) => r.rankable).length;
  return (
    <section className="prose" style={{ marginTop: 0 }}>
      <h1>About this project</h1>
      <p className="lede">
        A free research tool for one question that comes up in every equity, credit and due-diligence review: is this
        company&apos;s profit turning into cash?
      </p>

      <div className="card">
        <h2>Why it was built</h2>
        <p>
          Reported profit rests on estimates: when revenue is recognised, what gets capitalised, how receivables and
          inventory are valued. Operating cash flow is harder to shape. When the two drift apart for long, it is often
          the first visible sign of aggressive accounting, weakening demand or a balance sheet under strain, and
          sometimes simply of fast growth.
        </p>
        <p>
          Checking this by hand means opening one annual report at a time. Since 2020, listed companies in the EU and
          Norway have filed their annual reports in a machine-readable format (ESEF), so the check can now be run across
          every listed Nordic company at once, with each figure traceable to the official filing. Commercial screens
          offer similar ratios, but behind a paywall and rarely with a link back to the source line.
        </p>
      </div>

      <div className="card">
        <h2>How to use it in research</h2>
        <ol>
          <li><b>Screen.</b> Start from the ranked lists, or filter by country, sector or a specific red flag.</li>
          <li><b>Read the review notes.</b> Each flag states what was measured, what it can signal and the common innocent explanations.</li>
          <li><b>Go to the source.</b> Every figure on a company page opens the exact fact in the company&apos;s annual report, and each flag lists the notes worth reading.</li>
          <li><b>Compare.</b> Set the company against peers of similar size before drawing conclusions.</li>
        </ol>
        <p className="muted small">
          The flags are a starting point for questions, not a verdict. Fast-growing, acquisitive and project-based
          businesses trip them for ordinary reasons, and the review notes say so.
        </p>
      </div>

      <div className="card">
        <h2>Data, coverage and reproducibility</h2>
        <dl>
          <div><dt>Coverage</dt><dd>{index.length.toLocaleString("en-GB")} companies filing IFRS annual reports in Sweden, Norway, Denmark and Finland, fiscal years 2020 to 2025; {ranked} listed non-financial companies are ranked.</dd></div>
          <div><dt>Refresh</dt><dd>The pipeline runs monthly and after every code change, and the site rebuilds automatically. Last refresh: {meta.generated}.</dd></div>
          <div><dt>Open data and code</dt><dd>Everything is open on <a href="https://github.com/MariusFrykhammar/nordic-earnings-quality">GitHub</a> under the MIT licence: the Python pipeline, the concept mapping and every generated file. Each company&apos;s data can be downloaded as CSV from its page.</dd></div>
          <div><dt>Cost</dt><dd>Built entirely on free, official sources and free hosting.</dd></div>
          <div><dt>Feedback</dt><dd>Corrections and ideas are welcome via <a href="https://github.com/MariusFrykhammar/nordic-earnings-quality/issues">GitHub issues</a>.</dd></div>
        </dl>
      </div>

      <div className="card">
        <h2>Citing this tool</h2>
        <p className="small" style={{ fontFamily: "var(--mono)" }}>
          Frykhammar, M. ({meta.generated.slice(0, 4)}). Nordic Earnings Quality Scanner [web application and dataset].
          https://nordic-earnings-quality.vercel.app. Data from company ESEF annual reports via filings.xbrl.org,
          retrieved {meta.generated}.
        </p>
      </div>
      <p className="small muted">See <Link href="/methodology/">Methodology</Link> for formulas, thresholds and references.</p>
    </section>
  );
}
