// Build-time data access. Reads the pipeline output in ../data (server only).
import { readFileSync, readdirSync } from "node:fs";
import path from "node:path";

const DATA = path.join(process.cwd(), "..", "data");

export type Flag = { flag: string; title: string; evidence: Record<string, number | string> };

export type Year = {
  fy_end: string;
  currency: string;
  own_report: boolean;
  report: number;
  refs: Record<string, [number, string]>;
  fx_eur_avg?: number;
  fx_eur_end?: number;
  values: Record<string, number>;
  bases: Record<string, string>;
  metrics: Record<string, number>;
  concepts: Record<string, string>;
};

export type Company = {
  lei: string;
  display_name: string;
  legal_name: string | null;
  esef_entity_name: string;
  country: string;
  sector: string;
  sector_basis: string;
  org_number: string | null;
  registry: { nace: string; nace_text: string | null; register: string } | null;
  equity: { isins: string[]; venue: string | null; regulated_market: boolean } | null;
  tickers: string[];
  latest_year: number;
  in_universe: boolean;
  rankable: boolean;
  listing_status: string;
  revenue_eur_m: number | null;
  flags: Flag[];
  peer_group: string | null;
  reports: string[];
  years: Record<string, Year>;
};

export type IndexRow = {
  lei: string;
  name: string;
  legal_name: string;
  country: string;
  sector: string;
  market: string | null;
  currency: string;
  latest_year: number;
  in_universe: boolean;
  listing_status: string;
  rankable: boolean;
  revenue_eur_m: number | null;
  n_flags: number;
  flags: string[];
  profit_cash_gap: number | null;
  profit_cash_gap_scaled: number | null;
  net_profit_growth: number | null;
  ocf_growth: number | null;
  receivables_growth: number | null;
  revenue_growth: number | null;
  ebit_margin: number | null;
  cash_conversion_3y: number | null;
};

export type Rule = { title: string; rule: string; signals: string; innocent: string };
export type FlagsFile = {
  meta: {
    generated: string;
    source: string;
    min_revenue_eur_m_for_rankings: number;
    rules: Record<string, Rule>;
    sector_exclusions: Record<string, string[]>;
    reference_sources: Record<string, string>;
  };
};

const read = <T,>(p: string): T => JSON.parse(readFileSync(path.join(DATA, p), "utf8"));

export const getIndex = () => read<IndexRow[]>("companies.json");
export const getFlags = () => read<FlagsFile>("flags.json");
export const getCompany = (lei: string) => read<Company>(path.join("company", `${lei}.json`));
export const allLeis = () =>
  readdirSync(path.join(DATA, "company")).filter((f) => f.endsWith(".json")).map((f) => f.replace(".json", ""));

/** Profit and operating cash flow per year, for sparklines. */
export function series(c: Company): { year: number; np: number | null; ocf: number | null }[] {
  return Object.entries(c.years)
    .map(([y, v]) => ({ year: Number(y), np: v.values.net_profit ?? null, ocf: v.values.ocf ?? null }))
    .filter((r) => r.year >= 2020)
    .sort((a, b) => a.year - b.year);
}
