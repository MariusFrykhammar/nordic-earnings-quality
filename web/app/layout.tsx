import type { Metadata, Viewport } from "next";
import "./globals.css";
import Nav from "@/components/Nav";
import { getFlags } from "@/lib/data";

export const metadata: Metadata = {
  title: "Nordic Earnings Quality Scanner",
  description:
    "Which Nordic companies' profits are not backed by cash? Accounting red flags from official annual reports of listed companies in Sweden, Norway, Denmark and Finland.",
};
export const viewport: Viewport = { themeColor: "#04080d" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  const meta = getFlags().meta;
  return (
    <html lang="en">
      <body>
        <Nav />
        <main className="content">{children}</main>
        <footer className="foot">
          <div className="foot-inner">
            <p>
              Source: company annual reports (ESEF) via filings.xbrl.org, with reference data from GLEIF, ESMA, the
              Norwegian and Finnish business registers and the ECB. Data refreshed {meta.generated}.
            </p>
            <p>
              Flags are prompts for analysis, not conclusions, and nothing here is investment advice. Built by Marius
              Frykhammar. <a href="https://github.com/MariusFrykhammar/nordic-earnings-quality">Code and data on GitHub</a>.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
