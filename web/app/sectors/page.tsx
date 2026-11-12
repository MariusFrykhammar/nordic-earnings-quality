import type { Metadata } from "next";
import { getIndex } from "@/lib/data";
import Sectors, { type SectorRow } from "@/components/Sectors";

export const metadata: Metadata = { title: "Sectors: earnings quality scanner" };

export default function SectorsPage() {
  const rows: SectorRow[] = getIndex()
    .filter((r) => r.rankable)
    .map((r) => ({
      lei: r.lei, name: r.name, country: r.country, sector: r.sector, supersector: r.supersector, revenue_eur_m: r.revenue_eur_m,
      ebit_margin: r.ebit_margin, revenue_growth: r.revenue_growth, cash_conversion_3y: r.cash_conversion_3y,
      n_flags: r.n_flags, market: r.market,
    }));
  return (
    <section style={{ marginTop: 0 }}>
      <h1>Sectors</h1>
      <p className="lede">
        The ranked companies grouped by ICB industry and supersector, the classification used by the Nordic exchanges, with typical growth, margins and cash conversion for each group. Use it to see
        what normal looks like before judging a single company.
      </p>
      <Sectors rows={rows} />
    </section>
  );
}
