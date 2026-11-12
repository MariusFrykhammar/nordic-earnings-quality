import type { Metadata, Viewport } from "next";
import Link from "next/link";
import "./globals.css";
import Nav from "@/components/Nav";
import { getFlags, getIndex } from "@/lib/data";
import { pct } from "@/lib/format";

export const metadata: Metadata = {
  title: "Nordic Earnings Quality Scanner",
  description:
    "Which Nordic companies' profits are not backed by cash? Accounting red flags from official annual reports of listed companies in Sweden, Norway, Denmark and Finland.",
};
export const viewport: Viewport = { themeColor: "#04080d" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const index = getIndex();
  const meta = getFlags().meta;
  const ranked = index.filter((r) => r.rankable);
  const gap = ranked
    .filter((r) => r.sector !== "Real estate" && (r.net_profit_growth ?? 0) > 0 && (r.ocf_growth ?? 0) < 0 && (r.revenue_eur_m ?? 0) >= 500)
    .sort((a, b) => (b.profit_cash_gap_scaled ?? 0) - (a.profit_cash_gap_scaled ?? 0))
    .slice(0, 6);

  return (
    <html lang="en">
      <body>
        <div className="shell">
          <Nav />
          <div className="main">
            <div className="strip" aria-label="Summary">
              <span className="live">DATA {meta.generated}</span>
              <span><b>{ranked.length}</b>ranked</span>
              <span><b>{ranked.filter((r) => r.n_flags > 0).length}</b>flagged</span>
              {gap.map((r) => (
                <span key={r.lei}>
                  <Link href={`/company/${r.lei}/`}><b>{r.name.toUpperCase()}</b></Link>
                  OCF <span className="down">{pct(r.ocf_growth, true)}</span>
                </span>
              ))}
            </div>
            <main className="content">
              {children}
              <p className="disclaimer">
                Source: company annual reports (ESEF) via filings.xbrl.org, with reference data from GLEIF, ESMA, the
                Norwegian and Finnish business registers and the ECB. Flags are prompts for analysis, not conclusions, and
                nothing here is investment advice. Built by Marius Frykhammar.
              </p>
            </main>
          </div>
        </div>
        <footer className="status" aria-label="Status">
          <span className="ok">● ESEF REPORTS</span>
          <span>filings.xbrl.org</span>
          <span>{index.length.toLocaleString("en-GB")} companies · FY2020–FY2025</span>
          <span>refreshed {meta.generated}</span>
        </footer>
      </body>
    </html>
  );
}
