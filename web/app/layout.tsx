import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "Nordic Earnings Quality Scanner",
  description:
    "Which Nordic companies' profits are not backed by cash? Accounting red flags from official annual reports of listed companies in Sweden, Norway, Denmark and Finland.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="mast">
          <div className="wrap">
            <Link href="/" className="brand">
              Earnings quality<small>Nordic listed companies</small>
            </Link>
            <nav className="nav" aria-label="Main">
              <Link href="/">Findings</Link>
              <Link href="/compare/">Compare</Link>
              <Link href="/methodology/">Methodology</Link>
            </nav>
          </div>
        </header>
        <main className="wrap">{children}</main>
        <footer>
          <div className="wrap">
            <p>
              Source: company annual reports (ESEF) via filings.xbrl.org, with reference data from GLEIF, ESMA, the
              Norwegian and Finnish business registers and the ECB. Flags are prompts for analysis, not conclusions,
              and nothing here is investment advice.
            </p>
            <p>
              Built by Marius Frykhammar.{" "}
              <a href="https://github.com/MariusFrykhammar/nordic-earnings-quality">Code and data on GitHub</a>.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
