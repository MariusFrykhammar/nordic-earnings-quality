// Definitions, formulas, report checklists and references shared across pages.

export type Def = { term: string; formula: string; reading: string };

export const DEFINITIONS: Record<string, Def> = {
  cash_conversion: {
    term: "Cash conversion",
    formula: "Operating cash flow ÷ EBIT",
    reading: "Around 1.0× or above means operating profit is backed by cash. Persistently below 0.7× deserves a look at working capital and non-cash income.",
  },
  cash_conversion_3y: {
    term: "Three-year cash conversion",
    formula: "Σ operating cash flow (3 years) ÷ Σ EBIT (3 years)",
    reading: "Smooths timing effects such as a large order paid just after year-end. Only computed when three-year EBIT is at least 2% of revenue.",
  },
  accruals_ratio: {
    term: "Accruals ratio",
    formula: "(Net profit − operating cash flow) ÷ average total assets",
    reading: "The part of profit not yet received in cash, scaled by the balance sheet. Sloan (1996) found that high-accrual earnings tend to persist less. Usually negative, because depreciation is added back in cash flow.",
  },
  profit_cash_gap_scaled: {
    term: "Profit-versus-cash gap",
    formula: "(Δ net profit − Δ operating cash flow) ÷ prior-year revenue",
    reading: "How far profit and cash moved apart in one year, in percent of sales. Scaling by revenue rather than using growth rates keeps small or near-zero bases from dominating the ranking.",
  },
  receivables_vs_revenue: {
    term: "Receivables outpacing sales",
    formula: "Growth in trade receivables − growth in revenue",
    reading: "A rising gap means days sales outstanding are lengthening. Related to the days-sales-in-receivables index in Beneish (1999).",
  },
  inventory_vs_revenue: {
    term: "Inventory build-up",
    formula: "Growth in inventories − growth in revenue",
    reading: "Stock growing faster than sales can point to slowing demand and future write-downs, or simply to stocking up ahead of growth.",
  },
  intangible_capex: {
    term: "Capitalisation rate",
    formula: "Purchases of intangible assets (incl. capitalised development) ÷ revenue",
    reading: "Under IAS 38 development costs are capitalised once criteria are met. A rising rate lifts EBIT today and amortisation later.",
  },
  goodwill_to_equity: {
    term: "Goodwill to equity",
    formula: "Goodwill ÷ total equity",
    reading: "Above 0.8× means most of the equity rests on acquisition premiums that are tested for impairment rather than amortised (IAS 36).",
  },
  net_debt_ebitda: {
    term: "Net debt / EBITDA",
    formula: "(Borrowings + lease liabilities − cash) ÷ (EBIT + depreciation and amortisation)",
    reading: "Leverage relative to cash earnings. Leases are included when tagged, in line with IFRS 16 reporting.",
  },
  roce: {
    term: "Return on capital employed",
    formula: "EBIT ÷ average (equity + borrowings + leases − cash)",
    reading: "Operating return on the capital tied up in the business.",
  },
};

/** What an analyst would open in the annual report when a flag fires. */
export const CHECKLIST: Record<string, string[]> = {
  profit_without_cash: [
    "Cash flow statement: working-capital lines and other non-cash adjustments",
    "Notes on revenue recognition and contract assets (IFRS 15)",
    "One-off gains in other operating income, and tax or pension payments in the year",
  ],
  high_accruals: [
    "Reconciliation from profit to operating cash flow",
    "Fair-value gains, gains on disposals and share of associates' profit",
    "Changes in provisions and accrued income",
  ],
  receivables_outpace_sales: [
    "Trade receivables note: ageing, overdue amounts and loss allowance",
    "Factoring or receivables sale programmes (and changes to them)",
    "Large orders or acquisitions close to year-end",
  ],
  inventory_build_up: [
    "Inventories note: split into raw materials, work in progress and finished goods",
    "Write-downs recognised in the year and their reversal",
    "Management commentary on order intake and backlog",
  ],
  heavy_capitalisation: [
    "Intangible assets note: capitalised development and its useful life",
    "Accounting policy for development costs (IAS 38 criteria)",
    "Amortisation and impairment of capitalised development",
  ],
  acquisition_driven: [
    "Business combinations note: purchase price allocation and goodwill added",
    "Impairment test: cash-generating units, discount rate and headroom",
    "Organic growth versus acquired growth in the directors' report",
  ],
  leverage_creep: [
    "Borrowings note: maturities, covenants and interest rates",
    "Acquisitions and their contribution to EBITDA (full-year effect)",
    "Lease liabilities and their growth",
  ],
};

export const REFERENCES = [
  "Sloan, R. G. (1996). Do stock prices fully reflect information in accruals and cash flows about future earnings? The Accounting Review, 71(3), 289–315.",
  "Beneish, M. D. (1999). The detection of earnings manipulation. Financial Analysts Journal, 55(5), 24–36.",
  "Dechow, P. M., & Dichev, I. D. (2002). The quality of accruals and earnings: The role of accrual estimation errors. The Accounting Review, 77(s-1), 35–59.",
  "Richardson, S. A., Sloan, R. G., Soliman, M. T., & Tuna, I. (2005). Accrual reliability, earnings persistence and stock prices. Journal of Accounting and Economics, 39(3), 437–485.",
  "Dechow, P., Ge, W., & Schrand, C. (2010). Understanding earnings quality: A review of the proxies, their determinants and their consequences. Journal of Accounting and Economics, 50(2–3), 344–401.",
];
