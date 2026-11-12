# Day 1 gate report (data)

Generated 2026-11-12. Financial data: company annual reports (ESEF) via filings.xbrl.org, FY2020–FY2025.

## Sources

| Source | Used for | Status |
|---|---|---|
| ESEF annual reports (filings.xbrl.org) | all financial figures, fact-level source links | 5552 reports, 0 failed downloads |
| gleif | legal names, legal form, registration numbers | ok: 1207 of 1207 LEIs |
| firds | listed shares and trading venue (ESMA) | ok: 813 issuers with listed equity |
| registries | official industry codes (NACE) | ok: industry codes for 412 companies (NO, FI; SE/DK need credentials) |
| ISO 10383 | trading venue names and types | used to resolve venue codes |
| ECB | euro reference rates | loaded |
| Wikidata | industry where no registry code | fallback only |

## 1. Coverage

| Country | Reports after dedup | Companies | Non-financial | **Core 4 for 3+ yrs** | Rankable |
|---|---|---|---|---|---|
| SE | 1746 | 439 | 401 | **328** | 270 |
| NO | 1114 | 302 | 265 | **210** | 127 |
| DK | 1969 | 301 | 255 | **169** | 63 |
| FI | 723 | 165 | 137 | **121** | 99 |
| **Total** | | | | **828** | 559 |

Core 4 = revenue, EBIT, net profit, operating cash flow. Rankable = non-financial, revenue ≥ €25m, FY2024+ report, shares listed on a Nordic exchange (ESMA FIRDS). Fact-level source links: 89,738.

### Listing status and sector source (non-financial companies)

- **SE**: listing listed shares 333; no listed shares (ESMA FIRDS) 57; shares traded only outside Nordic exchanges (ESMA FIRDS) 11. Sector source: none 292; wikidata 57; data 47; name 3; PRH / YTJ 1; Brønnøysundregistrene 1
- **NO**: listing listed shares 166; no listed shares (ESMA FIRDS) 92; shares traded only outside Nordic exchanges (ESMA FIRDS) 7. Sector source: Brønnøysundregistrene 181; none 60; wikidata 15; data 8; PRH / YTJ 1
- **DK**: listing no listed shares (ESMA FIRDS) 160; listed shares 90; shares traded only outside Nordic exchanges (ESMA FIRDS) 5. Sector source: none 170; wikidata 70; data 12; name 3
- **FI**: listing listed shares 111; no listed shares (ESMA FIRDS) 21; shares traded only outside Nordic exchanges (ESMA FIRDS) 5. Sector source: PRH / YTJ 105; none 16; wikidata 10; data 6

### Company-years with data, non-financial companies

**SE**

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| revenue | 291 | 341 | 344 | 343 | 339 | 314 |
| ebit | 276 | 325 | 327 | 324 | 319 | 292 |
| net_profit | 299 | 350 | 348 | 348 | 342 | 316 |
| ocf | 295 | 347 | 347 | 347 | 343 | 317 |
| total_assets | 308 | 352 | 351 | 348 | 346 | 318 |
| equity | 334 | 354 | 352 | 356 | 335 | 305 |
| cash | 344 | 361 | 367 | 367 | 346 | 318 |
| borrowings | 164 | 195 | 209 | 216 | 227 | 202 |
| receivables | 289 | 329 | 330 | 324 | 324 | 297 |
| inventories | 175 | 205 | 211 | 208 | 211 | 191 |
| goodwill_measure | 222 | 258 | 265 | 260 | 261 | 240 |
| capex | 257 | 306 | 301 | 300 | 302 | 278 |
| capex_intangible | 177 | 217 | 213 | 219 | 220 | 200 |
| da | 208 | 244 | 242 | 234 | 226 | 198 |

**NO**

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| revenue | 188 | 218 | 208 | 211 | 206 | 180 |
| ebit | 183 | 213 | 208 | 209 | 203 | 177 |
| net_profit | 191 | 222 | 214 | 217 | 209 | 181 |
| ocf | 189 | 220 | 214 | 216 | 208 | 180 |
| total_assets | 195 | 223 | 215 | 220 | 211 | 182 |
| equity | 219 | 232 | 235 | 228 | 210 | 181 |
| cash | 216 | 229 | 232 | 228 | 209 | 179 |
| borrowings | 137 | 161 | 154 | 156 | 151 | 130 |
| receivables | 180 | 205 | 199 | 206 | 201 | 177 |
| inventories | 128 | 151 | 144 | 146 | 142 | 121 |
| goodwill_measure | 129 | 149 | 148 | 141 | 138 | 124 |
| capex | 140 | 167 | 159 | 161 | 157 | 135 |
| capex_intangible | 44 | 62 | 59 | 53 | 54 | 50 |
| da | 164 | 194 | 182 | 187 | 186 | 158 |

**DK**

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| revenue | 86 | 155 | 182 | 182 | 207 | 197 |
| ebit | 86 | 156 | 182 | 181 | 206 | 192 |
| net_profit | 89 | 163 | 192 | 191 | 218 | 205 |
| ocf | 88 | 162 | 191 | 191 | 218 | 207 |
| total_assets | 101 | 169 | 199 | 199 | 222 | 208 |
| equity | 154 | 198 | 207 | 234 | 222 | 208 |
| cash | 150 | 182 | 195 | 225 | 217 | 203 |
| borrowings | 64 | 112 | 134 | 136 | 147 | 135 |
| receivables | 95 | 158 | 183 | 184 | 207 | 194 |
| inventories | 72 | 123 | 147 | 152 | 166 | 155 |
| goodwill_measure | 69 | 111 | 131 | 138 | 157 | 144 |
| capex | 74 | 129 | 155 | 161 | 177 | 165 |
| capex_intangible | 58 | 103 | 124 | 131 | 143 | 129 |
| da | 65 | 123 | 148 | 149 | 168 | 157 |

**FI**

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| revenue | 116 | 128 | 118 | 114 | 115 | 104 |
| ebit | 114 | 126 | 118 | 115 | 115 | 103 |
| net_profit | 116 | 128 | 118 | 115 | 115 | 103 |
| ocf | 116 | 128 | 118 | 115 | 115 | 103 |
| total_assets | 116 | 128 | 119 | 115 | 116 | 104 |
| equity | 127 | 126 | 121 | 119 | 116 | 103 |
| cash | 126 | 127 | 122 | 119 | 116 | 104 |
| borrowings | 72 | 78 | 74 | 72 | 74 | 64 |
| receivables | 111 | 122 | 114 | 112 | 113 | 103 |
| inventories | 85 | 98 | 92 | 95 | 95 | 86 |
| goodwill_measure | 101 | 107 | 98 | 96 | 98 | 90 |
| capex | 95 | 109 | 103 | 104 | 105 | 96 |
| capex_intangible | 26 | 30 | 29 | 27 | 27 | 23 |
| da | 104 | 116 | 109 | 108 | 109 | 98 |

### How metrics were mapped (company-years)

- **revenue**: `Revenue` 4014; `RevenueFromContractsWithCustomers` 605; `RevenueAndOperatingIncome` 411; `fallback:RentalIncomeFromInvestmentProperty` 192; `specific-line:RevenueFromSaleOfGoods` 84; `specific-line:RevenueFromRenderingOfServices` 34
- **ebit**: `ProfitLossFromOperatingActivities` 5243; `extension-auto:` 11
- **net_profit**: `ProfitLoss` 5721; `fallback:ProfitLossAttributableToOwnersOfParent` 25; `ProfitLossAttributableToOwnersOfParent+ProfitLossAttributableToNoncontrollingInterests` 2
- **ocf**: `CashFlowsFromUsedInOperatingActivities` 5540; `fallback:CashFlowsFromUsedInOperations` 175; `CashFlowsFromUsedInOperatingActivitiesContinuingOperations` 14; `extension-auto:` 1
- **receivables**: `CurrentTradeReceivables` 3294; `TradeAndOtherCurrentReceivables` 1452; `TradeReceivables` 265; `TradeAndOtherReceivables` 117
- **goodwill**: `Goodwill` 2770
- **intangibles_incl_goodwill**: `IntangibleAssetsAndGoodwill` 2403; `Goodwill+IntangibleAssetsOtherThanGoodwill` 1249
- **da**: `DepreciationAndAmortisationExpense` 1724; `DepreciationAmortisationAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss` 1128; `AdjustmentsForDepreciationAndAmortisationExpense` 893; `AdjustmentsForDepreciationAndAmortisationExpenseAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss` 549; `DepreciationExpense+AmortisationExpense` 38; `AdjustmentsForDepreciationExpense+AdjustmentsForAmortisationExpense` 35

## 2. Spot-checks (12 companies, 3 per country)

| Company | Year | Ours: revenue / EBIT (m) | Published | Result |
|---|---|---|---|---|
| Atlas Copco | FY2025 | 168,343 / 34,114 | 168,343 / 34,114 | ✅ |
| Sandvik | FY2025 | 120,680 / 20,809 | 120,680 / 20,809 (PBT 19,458 + net finance 1,351) | ✅ |
| Electrolux | FY2025 | 131,282 / 3,657 | 131,282 / 3,657 | ✅ |
| Orkla | FY2025 | 71,044 / 7,086 | 71,547 / 7,086 | ⚠️ EBIT ✅; IFRS `Revenue` tag excludes other operating revenue |
| Kongsberg Gruppen | FY2025 | 31,562 / 4,694 | 31,562 / ~4,697 (continuing ops) | ✅ |
| Telenor | FY2025 | 76,548 / 17,978 | 76,548 / 17,978 | ✅ |
| Carlsberg | FY2025 | 89,095 / not reported | 89,095 / 13,356 before special items | ✅ EBIT correctly not reported |
| DSV | FY2025 | 247,331 / not reported | 247,331 / 19,611 before special items | ✅ EBIT correctly not reported |
| Novo Nordisk | FY2025 | 309,064 / 127,658 | 309,064 / 127,658 | ✅ |
| Kone | FY2025 | 11,245.2 / 1,336.2 | 11,245.2 / 1,336.2 | ✅ |
| UPM-Kymmene | FY2025 | 9,656 / 749 | 9,656 / 749 | ✅ |
| Wärtsilä | FY2024 | 6,449 / 716 | 6,449 / 716 | ✅ (FY2025 report not yet in repository) |

## 3. Companies needing overrides

77 non-financial companies with a recent report miss a core metric: ebit 47, revenue 17, revenue+ebit+net_profit+ocf 5, ocf 2, net_profit 2, revenue+ebit 1, revenue+net_profit 1, ebit+net_profit 1, ebit+net_profit+ocf 1.

| Company | Country | Sector | Missing |
|---|---|---|---|
| AALBORG BOLDSPILKLUB A/S | DK | Transport & shipping | revenue, ebit, net_profit, ocf |
| BI Erhvervsejendomme A/S | DK | Real estate | revenue, ebit |
| BRØNDBYERNES I.F. FODBOLD A/S | DK | Unclassified | ebit, net_profit |
| CARLSBERG A/S | DK | Consumer | ebit |
| CARLSBERG BREWERIES A/S | DK | Unclassified | ebit |
| CENTRICA ENERGY TRADING A/S | DK | Unclassified | revenue |
| CONSOLIDATED HOLDINGS A/S | DK | Unclassified | revenue |
| Christiania Shipping A/S | DK | Unclassified | revenue |
| DANSKE COMMODITIES A/S | DK | Energy | revenue |
| DSV A/S | DK | Transport & shipping | ebit |
| FAST EJENDOM DANMARK A/S | DK | Real estate | revenue, net_profit |
| FLSMIDTH A/S | DK | Industrials | revenue, ebit, net_profit, ocf |
| GYLDENDAL A/S | DK | Telecom & media | ebit |
| HEMPEL A/S | DK | Industrials | ebit |
| HEMPEL FONDEN | DK | Unclassified | ebit |
| INVESTERINGSSELSKABET LUXOR A/S | DK | Unclassified | ebit |
| KALUNDBORG REFINERY A/S | DK | Unclassified | ebit |
| MFT Energy A/S | DK | Unclassified | revenue |
| MFT Energy Holding ApS | DK | Unclassified | revenue |
| MT Højgaard Holding A/S | DK | Unclassified | ebit |
| NORDIC BIOSCIENCE HOLDING A/S | DK | Unclassified | ebit |
| NTG Nordic Transport Group A/S | DK | Unclassified | ebit |
| Nitor Holding ApS | DK | Unclassified | revenue |
| PRIME OFFICE A/S | DK | Real estate | revenue, ebit, net_profit, ocf |
| RESS LIFE INVESTMENTS A/S | DK | Unclassified | revenue |
| Rekom Group Holding ApS | DK | Unclassified | ebit |
| Scandinavian Investment Group A/S | DK | Real estate | ebit |
| WRIST SHIP SUPPLY HOLDING A/S | DK | Unclassified | revenue |
| Digitalist Group Oyj | FI | Technology | ebit, net_profit, ocf |
| AX INV1 HOLDING AS | NO | Technology | revenue, ebit, net_profit, ocf |
| GOODTECH ASA | NO | Industrials | ocf |
| GRIEG SEAFOOD ASA | NO | Consumer | ebit |
| Hafnia Limited | NO | Unclassified | revenue |
| KMC PROPERTIES ASA | NO | Industrials | revenue, ebit, net_profit, ocf |
| MOWI ASA | NO | Consumer | ebit |
| ODFJELL SE | NO | Transport & shipping | ebit |
| PCI BIOTECH HOLDING ASA | NO | Health care | revenue |
| SATS ASA | NO | Industrials | ebit |
| SoftwareOne Holding AG | NO | Unclassified | ebit |
| TREASURE AS | NO | Real estate | revenue |
| Younited Financial S.A. | NO | Unclassified | ebit |
| AB Sagax | SE | Real estate | ebit |
| Altra Fastigheter AB | SE | Real estate | ebit |
| Atrium Ljungberg AB | SE | Real estate | ebit |
| Brinova Fastigheter AB (publ) | SE | Real estate | ebit |
| Catena AB | SE | Real estate | ebit |
| Cibus Nordic Real Estate AB (publ) | SE | Real estate | ebit |
| Corem Property Group AB | SE | Real estate | ebit |
| Fastighets AB Balder | SE | Real estate | ebit |
| Fastighetsbolaget Emilshus AB | SE | Real estate | ebit |
| Fortinova Fastigheter AB (publ) | SE | Real estate | ebit |
| GARO Aktiebolag | SE | Unclassified | net_profit |
| Gruvaktiebolaget Viscaria | SE | Unclassified | revenue |
| John Mattson Fastighetsföretagen AB (publ) | SE | Real estate | ebit |
| K-Fast Holding AB | SE | Real estate | ebit |
| KlaraBo Sverige AB | SE | Real estate | ebit |
| Linc AB | SE | Unclassified | revenue |
| Logistea AB | SE | Real estate | ebit |
| Lundin Gold Inc. | SE | Unclassified | ebit |
| Lundin Mining Corporation | SE | Unclassified | ebit |
| Mangold AB | SE | Unclassified | ebit |
| Medicover AB | SE | Unclassified | revenue |
| NAXS AB (publ) | SE | Unclassified | revenue |
| NP3 Fastigheter AB | SE | Real estate | ebit |
| Neobo Fastigheter AB (publ) | SE | Real estate | ebit |
| Net Insight AB | SE | Unclassified | ocf |
| Nivika Fastigheter AB (publ) | SE | Real estate | ebit |
| Pandox Aktiebolag | SE | Real estate | ebit |
| Platzer Fastigheter Holding AB (publ) | SE | Real estate | ebit |
| Prisma Properties AB | SE | Real estate | ebit |
| SBF Bostad AB (publ) | SE | Real estate | ebit |
| Stendörren Fastigheter AB | SE | Real estate | ebit |
| Stenhus Fastigheter i Norden AB (publ) | SE | Real estate | ebit |
| Truecaller AB | SE | Unclassified | net_profit |
| VEF AB (publ) | SE | Unclassified | revenue |
| WALLENSTAM AB | SE | Real estate | ebit |
| Wihlborgs Fastigheter AB | SE | Real estate | ebit |

## 4. Validation

- balance: assets != equity + liabilities: 50 company-years
- balance: assets != equity and liabilities: 5 company-years
- implausible: equity ratio > 100%: 2 company-years
- implausible: revenue > 20x total assets (scale error?): 1 company-years
- implausible: |EBIT margin| > 100%: 408 company-years
- sign: negative cash: 16 company-years
- sign: negative revenue: 9 company-years
- sign: non-positive total assets: 4 company-years

## 5. Top 15 flagged companies

Rankable universe: 559 companies. Flags per company: {0: 400, 1: 127, 2: 28, 3: 4}.

| # | Company | Country | Market | FY | Flags |
|---|---|---|---|---|---|
| 1 | EQL Pharma | SE | Nasdaq Stockholm | 2025 | High accruals, Receivables outpace sales, Heavy capitalisation |
| 2 | BW Energy | NO | Oslo Børs | 2025 | Receivables outpace sales, Inventory build-up, Heavy capitalisation |
| 3 | B3 Consulting Group | SE | Nasdaq Stockholm | 2025 | Profit without cash, Acquisition-driven, Leverage creep |
| 4 | Hexagon Purus | NO | Oslo Børs | 2025 | Receivables outpace sales, Heavy capitalisation, Acquisition-driven |
| 5 | MilDef Group | SE | Nasdaq Stockholm | 2025 | High accruals, Inventory build-up |
| 6 | Bittium | FI | Nasdaq Helsinki | 2025 | Profit without cash, Receivables outpace sales |
| 7 | Aspocomp Group | FI | Nasdaq Helsinki | 2024 | Receivables outpace sales, Inventory build-up |
| 8 | Luotea | FI | Nasdaq Helsinki | 2025 | High accruals, Acquisition-driven |
| 9 | Raute | FI | Nasdaq Helsinki | 2025 | High accruals, Receivables outpace sales |
| 10 | Vistin Pharma | NO | Oslo Børs | 2025 | Profit without cash, Receivables outpace sales |
| 11 | Orion | FI | Nasdaq Helsinki | 2025 | Profit without cash, High accruals |
| 12 | engcon | SE | Nasdaq Stockholm | 2025 | High accruals, Inventory build-up |
| 13 | AIK Fotboll | SE | NGM Main Regulated | 2024 | High accruals, Heavy capitalisation |
| 14 | Dynavox Group | SE | Nasdaq Stockholm | 2025 | Profit without cash, Inventory build-up |
| 15 | Norconsult | NO | Oslo Børs | 2025 | Profit without cash, Acquisition-driven |

Flags are prompts for analysis, not conclusions. Definitions and innocent explanations: `data/flags.json` → `meta.rules`.
