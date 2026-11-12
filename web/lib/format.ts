// Formatting helpers shared by server and client components.

export const COUNTRY: Record<string, string> = { SE: "Sweden", NO: "Norway", DK: "Denmark", FI: "Finland" };

const nf = (d: number) => new Intl.NumberFormat("en-GB", { minimumFractionDigits: d, maximumFractionDigits: d });

/** Millions with sensible precision: 168,343 / 1,336.2 / 0.45 */
export function money(v: number | null | undefined): string {
  if (v === null || v === undefined || Number.isNaN(v)) return "–";
  const a = Math.abs(v);
  return nf(a >= 1000 ? 0 : a >= 10 ? 1 : 2).format(v);
}

export function pct(v: number | null | undefined, signed = false, digits = 0): string {
  if (v === null || v === undefined || Number.isNaN(v)) return "–";
  if (signed && v > 9.99) return "> +999%";
  const s = nf(digits).format(v * 100) + "%";
  return signed && v > 0 ? "+" + s : s.replace("-", "−");
}

export function ratio(v: number | null | undefined, digits = 2, suffix = ""): string {
  if (v === null || v === undefined || Number.isNaN(v)) return "–";
  return nf(digits).format(v).replace("-", "−") + suffix;
}

export const eurM = (v: number | null | undefined) => (v === null || v === undefined ? "–" : "€" + money(v) + "m");

/** Plain-language sentence describing what triggered a flag. */
export function flagSentence(flag: string, ev: Record<string, number | string>, year: number): string {
  const n = (k: string) => (typeof ev[k] === "number" ? (ev[k] as number) : null);
  switch (flag) {
    case "profit_without_cash":
      if (n("net_profit_growth") !== null)
        return `In FY${year} net profit changed ${pct(n("net_profit_growth"), true)} while operating cash flow changed ${pct(n("ocf_growth"), true)}.`;
      return `Over three years operating cash flow was ${ratio(n("cash_conversion_3y"))}× EBIT; the bottom tenth of peers sits below ${ratio(n("peer_p10"))}×.`;
    case "high_accruals":
      return `Net profit exceeded operating cash flow by ${pct(n("accruals_ratio"), false, 1)} of average total assets; the peer top tenth starts at ${pct(n("peer_p90"), false, 1)}.`;
    case "receivables_outpace_sales":
      return `Trade receivables changed ${pct(n("receivables_growth"), true)} against revenue ${pct(n("revenue_growth"), true)}; receivables are ${pct(n("receivables_to_revenue"))} of revenue.`;
    case "inventory_build_up":
      return `Inventories changed ${pct(n("inventory_growth"), true)} against revenue ${pct(n("revenue_growth"), true)}; inventories are ${pct(n("inventory_to_revenue"))} of revenue.`;
    case "heavy_capitalisation":
      return `Spending on intangible assets was ${pct(n("intangible_capex_to_revenue"), false, 1)} of revenue, up from ${pct(n("earlier"), false, 1)} two years earlier.`;
    case "acquisition_driven":
      return `Goodwill is ${ratio(n("goodwill_to_equity"))}× equity, up from ${ratio(n("two_years_earlier"))}× two years earlier${ev.basis && String(ev.basis).includes("incl.") ? " (tagged together with other intangibles)" : ""}.`;
    case "leverage_creep":
      return `Net debt rose to ${ratio(n("net_debt_ebitda"), 1)}× EBITDA from ${ratio(n("two_years_earlier"), 1)}× two years earlier, while cash conversion fell from ${ratio(n("cash_conversion_two_years_earlier"))} to ${ratio(n("cash_conversion"))}.`;
    default:
      return "";
  }
}
