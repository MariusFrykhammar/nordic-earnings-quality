# Day 1 gate report (data)

Generated from pipeline run 5 (GitHub Actions). Source: company annual reports (ESEF) via filings.xbrl.org. FY2020–FY2025.

## 1. Coverage

| Country | Filings FY20–25 | After dedup | Companies (IFRS) | Non-financial | **Core 4 for 3+ yrs** | Rankable (≥ €25m rev, FY24+, not private form) |
|---|---|---|---|---|---|---|
| SE | 1811 | 1746 | 439 | 406 | **332** | 295 |
| NO | 1188 | 1114 | 302 | 268 | **213** | 142 |
| DK | 2043 | 1969 | 301 | 262 | **173** | 150 |
| FI | 1148 | 723 | 165 | 149 | **132** | 112 |
| **Total** | | | 1207 | 1085 | **850** | 699 |

Core 4 = revenue, EBIT, net profit, operating cash flow. Gate target: about 400+. Downloads failed: 0. Revenue restatements > 2% (own report vs next year's comparative): 169.

### Company-years with data, non-financial companies

**SE**

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| revenue | 294 | 345 | 348 | 347 | 342 | 316 |
| ebit | 280 | 330 | 332 | 329 | 323 | 295 |
| net_profit | 303 | 355 | 353 | 353 | 346 | 319 |
| ocf | 299 | 352 | 352 | 352 | 347 | 320 |
| total_assets | 312 | 357 | 356 | 353 | 350 | 321 |
| equity | 338 | 359 | 357 | 361 | 339 | 308 |
| cash | 349 | 366 | 372 | 372 | 350 | 321 |
| borrowings | 165 | 197 | 211 | 218 | 228 | 203 |
| receivables | 292 | 333 | 334 | 328 | 327 | 299 |
| inventories | 177 | 207 | 213 | 210 | 213 | 192 |
| goodwill_measure | 223 | 260 | 267 | 262 | 263 | 241 |
| capex | 260 | 310 | 305 | 304 | 306 | 281 |
| capex_intangible | 178 | 220 | 216 | 222 | 223 | 202 |
| da | 210 | 247 | 245 | 237 | 228 | 199 |

**NO**

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| revenue | 191 | 222 | 212 | 214 | 208 | 179 |
| ebit | 186 | 217 | 212 | 212 | 205 | 176 |
| net_profit | 194 | 226 | 218 | 220 | 211 | 180 |
| ocf | 193 | 224 | 218 | 219 | 210 | 179 |
| total_assets | 199 | 227 | 219 | 223 | 213 | 180 |
| equity | 223 | 236 | 239 | 231 | 212 | 179 |
| cash | 220 | 233 | 236 | 231 | 211 | 177 |
| borrowings | 138 | 161 | 156 | 156 | 150 | 128 |
| receivables | 182 | 207 | 201 | 207 | 202 | 174 |
| inventories | 127 | 150 | 143 | 145 | 141 | 119 |
| goodwill_measure | 129 | 148 | 147 | 138 | 135 | 120 |
| capex | 144 | 172 | 162 | 163 | 159 | 134 |
| capex_intangible | 45 | 63 | 59 | 52 | 54 | 50 |
| da | 163 | 193 | 182 | 186 | 185 | 157 |

**DK**

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| revenue | 89 | 160 | 187 | 186 | 213 | 203 |
| ebit | 89 | 161 | 187 | 185 | 212 | 198 |
| net_profit | 93 | 168 | 197 | 195 | 224 | 211 |
| ocf | 91 | 167 | 196 | 195 | 224 | 213 |
| total_assets | 104 | 174 | 204 | 203 | 228 | 214 |
| equity | 158 | 203 | 212 | 240 | 228 | 214 |
| cash | 155 | 187 | 200 | 231 | 223 | 209 |
| borrowings | 66 | 115 | 137 | 139 | 150 | 137 |
| receivables | 98 | 163 | 188 | 188 | 213 | 200 |
| inventories | 75 | 127 | 151 | 156 | 171 | 160 |
| goodwill_measure | 72 | 115 | 135 | 142 | 162 | 149 |
| capex | 77 | 134 | 160 | 165 | 181 | 169 |
| capex_intangible | 60 | 107 | 128 | 135 | 147 | 133 |
| da | 66 | 126 | 151 | 151 | 171 | 160 |

**FI**

| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|
| revenue | 125 | 140 | 130 | 124 | 124 | 112 |
| ebit | 123 | 138 | 130 | 125 | 124 | 111 |
| net_profit | 125 | 140 | 130 | 125 | 124 | 111 |
| ocf | 125 | 140 | 130 | 125 | 124 | 111 |
| total_assets | 125 | 140 | 131 | 125 | 125 | 112 |
| equity | 139 | 138 | 133 | 129 | 125 | 111 |
| cash | 137 | 139 | 134 | 129 | 125 | 111 |
| borrowings | 77 | 84 | 81 | 78 | 79 | 68 |
| receivables | 119 | 132 | 124 | 120 | 120 | 109 |
| inventories | 91 | 105 | 99 | 100 | 100 | 90 |
| goodwill_measure | 109 | 118 | 109 | 104 | 105 | 96 |
| capex | 103 | 119 | 113 | 113 | 114 | 104 |
| capex_intangible | 30 | 34 | 33 | 30 | 31 | 26 |
| da | 112 | 127 | 120 | 117 | 117 | 105 |

FY2025 is lower because some FY2025 reports are not yet in the repository (e.g. Wärtsilä).

### How metrics were mapped (company-years)

- **revenue**: `Revenue` 4014; `RevenueFromContractsWithCustomers` 605; `RevenueAndOperatingIncome` 411; `fallback:RentalIncomeFromInvestmentProperty` 192; `specific-line:RevenueFromSaleOfGoods` 84; `specific-line:RevenueFromRenderingOfServices` 34
- **ebit**: `ProfitLossFromOperatingActivities` 5243; `extension-auto:` 11
- **net_profit**: `ProfitLoss` 5721; `fallback:ProfitLossAttributableToOwnersOfParent` 25; `ProfitLossAttributableToOwnersOfParent+ProfitLossAttributableToNoncontrollingInterests` 2
- **ocf**: `CashFlowsFromUsedInOperatingActivities` 5540; `fallback:CashFlowsFromUsedInOperations` 175; `CashFlowsFromUsedInOperatingActivitiesContinuingOperations` 14; `extension-auto:` 1
- **receivables**: `CurrentTradeReceivables` 3294; `TradeAndOtherCurrentReceivables` 1452; `TradeReceivables` 265; `TradeAndOtherReceivables` 117
- **borrowings_noncurrent**: `LongtermBorrowings` 2958; `NoncurrentPortionOfNoncurrentLoansReceived` 366
- **goodwill**: `Goodwill` 2770
- **intangibles_incl_goodwill**: `IntangibleAssetsAndGoodwill` 2403; `Goodwill+IntangibleAssetsOtherThanGoodwill` 1249
- **da**: `DepreciationAndAmortisationExpense` 1724; `DepreciationAmortisationAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss` 1128; `AdjustmentsForDepreciationAndAmortisationExpense` 893; `AdjustmentsForDepreciationAndAmortisationExpenseAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss` 549; `DepreciationExpense+AmortisationExpense` 38; `AdjustmentsForDepreciationExpense+AdjustmentsForAmortisationExpense` 35

## 2. Spot-checks (12 companies, 3 per country)

| Company | Year | Ours: revenue / EBIT (m) | Published | Result |
|---|---|---|---|---|
| ATLAS COPCO AKTIEBOLAG | FY2025 | 168,343 / 34,114 | 168,343 / 34,114 | ✅ |
| Sandvik Aktiebolag | FY2025 | 120,680 / 20,809 | 120,680 / 20,809 (PBT 19,458 + net finance 1,351) | ✅ |
| Electrolux Professional AB (publ) | FY2025 | 131,282 / 3,657 | 131,282 / 3,657 | ✅ |
| ORKLA ASA | FY2025 | 71,044 / 7,086 | 71,547 / 7,086 | ⚠️ EBIT ✅. Revenue: we take the IFRS `Revenue` tag; Orkla's headline 'operating revenues' also includes other operating revenue |
| KONGSBERG GRUPPEN ASA | FY2025 | 31,562 / 4,694 | 31,562 / ~4,697 (continuing ops, Maritime demerged) | ✅ |
| TELENOR ASA | FY2025 | 76,548 / 17,978 | 76,548 / 17,978 | ✅ |
| CARLSBERG A/S | FY2025 | 89,095 / not reported | 89,095 / 13,356 *before special items* | ✅ revenue; EBIT correctly 'not reported' (no EBIT line after special items is tagged) |
| DSV A/S | FY2025 | 247,331 / not reported | 247,331 / 19,611 *before special items* | ✅ revenue; EBIT as Carlsberg |
| NOVO NORDISK A/S | FY2025 | 309,064 / 127,658 | 309,064 / 127,658 | ✅ |
| KONE OYJ | FY2025 | 11,245.2 / 1,336.2 | 11,245.2 / 1,336.2 | ✅ |
| UPM-KYMMENE OYJ | FY2025 | 9,656 / 749 | 9,656 / 749 | ✅ |
| Wärtsilä Oyj Abp | FY2024 | 6,449 / 716 | 6,449 / 716 | ✅ (FY2025 report not yet in the repository) |

Net profit and operating cash flow also matched where published (Electrolux 878, UPM 491 / 1,405, Novo 102,434, Carlsberg 6,978, Kongsberg 7,922 incl. discontinued, Wärtsilä OCF 1,208).

## 3. Companies needing overrides

77 non-financial companies with a recent report miss at least one core metric. By gap: ebit 47, revenue 18, revenue+ebit+net_profit+ocf 4, ocf 2, net_profit 2, revenue+ebit 1, revenue+net_profit 1, ebit+net_profit 1, ebit+net_profit+ocf 1.

| Company | Country | Sector | Missing | Possible concepts in the report |
|---|---|---|---|---|
| AALBORG BOLDSPILKLUB A/S | DK | Transport & shipping | revenue, ebit, net_profit, ocf | `OperatingEquipmentAndFixtures` |
| BI Erhvervsejendomme A/S | DK | Real estate | revenue, ebit |  |
| BRØNDBYERNES I.F. FODBOLD A/S | DK | Unclassified | ebit, net_profit | `AdjustmentsForDepreciationAndAmortisationExpenseAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss`, `CashFlowsFromUsedInFinancingActivities`, `CashFlowsFromUsedInInvestingActivities` |
| CARLSBERG A/S | DK | Consumer | ebit | `CashFlowsFromUsedInInvestingActivitiesFinancial`, `CashFlowsFromUsedInInvestingActivitiesOperational`, `CashFlowsFromUsedInOperatingAndInvestingActivities` |
| CARLSBERG BREWERIES A/S | DK | Unclassified | ebit | `CashFlowsFromUsedInInvestingActivitiesFinancial`, `CashFlowsFromUsedInInvestingActivitiesOperational`, `CashFlowsFromUsedInOperatingAndInvestingActivities` |
| CENTRICA ENERGY TRADING A/S | DK | Unclassified | revenue | `CashFlowsFromUsedInCashPoolingClassifiedAsFinancingActivities`, `ProfitLossFromOperatingActivitiesBeforeInterestTaxesDepreciationAndAmortisationExpense`, `RevenueAndTradingIncomeExpense` |
| CONSOLIDATED HOLDINGS A/S | DK | Unclassified | revenue |  |
| Christiania Shipping A/S | DK | Unclassified | revenue | `InterestPaidOnLeaseLiabilitiesClassifiedAsOperatingActivities`, `InterestPaidOnOtherFinancialLiabilitiesClassifiedAsOperatingActivities`, `InterestPaidOtherThanLeaseLiabilitiesClassifiedAsOperatingActivities` |
| DANSKE COMMODITIES A/S | DK | Energy | revenue | `CashFlowsFromUsedInCashPoolingClassifiedAsFinancingActivities`, `CashFlowsFromUsedInOperatingActivitiesBeforeTax`, `RevenueFromContractsWithCustomersAndTradingIncomeExpense` |
| DSV A/S | DK | Transport & shipping | ebit | `AdjustedFreeCashFlow`, `CashFlowsFromUsedInOperatingAndInvestingActivities`, `GrossProfitExcludingDepreciationAmortisationAndEmployeeBenefitsExpenseOtherThanHourlyWorkers` |
| FAST EJENDOM DANMARK A/S | DK | Real estate | revenue, net_profit |  |
| FLSMIDTH A/S | DK | Industrials | revenue, ebit, net_profit, ocf |  |
| GYLDENDAL A/S | DK | Telecom & media | ebit | `DistributionCostsAndSalesAndMarketingExpense`, `ProfitLossFromOperatingActivitiesBeforeSpecialItems` |
| HEMPEL A/S | DK | Industrials | ebit | `CashFlowsFromUsedInOperatingAndInvestingActivities`, `ProfitLossFromOperatingActivitiesFromContinuingOperations`, `ProfitLossFromOperatingActivitiesFromDiscontinuedOperations` |
| HEMPEL FONDEN | DK | Unclassified | ebit | `CashFlowsFromUsedInOperatingAndInvestingActivities`, `ProfitLossFromOperatingActivitiesFromContinuingOperations`, `ProfitLossFromOperatingActivitiesFromDiscontinuedOperations` |
| INVESTERINGSSELSKABET LUXOR A/S | DK | Unclassified | ebit | `OtherFinanceIncomeReceivedClassifiedAsOperatingActivities`, `OtherIncomeReceivedClassifiedAsOperatingActivities`, `PaymentsForOperatingExpenseAndOtherClassifiedAsOperatingActivities` |
| KALUNDBORG REFINERY A/S | DK | Unclassified | ebit | `ProfitLossFromOperatingActivitiesBeforeInterestTaxesDepreciationAndAmortisationExpense` |
| MFT Energy A/S | DK | Unclassified | revenue | `CashFlowsFromUsedInIncreaseDecreaseInCurrentBorrowingsFromRelatedParties` |
| MFT Energy Holding ApS | DK | Unclassified | revenue |  |
| MT Højgaard Holding A/S | DK | Unclassified | ebit | `ProfitLossBeforeTaxContinuingOperations`, `ProfitLossFromOperatingActivitiesBeforeShareOfProfitLossOfAssociatesAndJointVenturesAccountedForUsingEquityMethod`, `ProfitLossFromOperatingActivitiesFromContinuingOperations` |
| NORDIC BIOSCIENCE HOLDING A/S | DK | Unclassified | ebit | `OperatingProfitBeforeSpecialItems` |
| NTG Nordic Transport Group A/S | DK | Unclassified | ebit | `CashFlowsFromUsedInOperatingAndInvestingActivities`, `FinanceCostsPaidOtherThanInterestPaidOnLeaseLiabilitiesClassifiedAsOperatingActivities`, `GrossProfitExcludingDepreciationAmortisationAndEmployeeBenefitsExpenseOtherThanTerminalRelatedWorkers` |
| Nitor Holding ApS | DK | Unclassified | revenue | `ProfitLossFromOperatingActivitiesBeforeInterestTaxesDepreciationAndAmortisationExpense` |
| PRIME OFFICE A/S | DK | Real estate | revenue, ebit, net_profit, ocf |  |
| RESS LIFE INVESTMENTS A/S | DK | Unclassified | revenue |  |
| Rekom Group Holding ApS | DK | Unclassified | ebit | `CashFlowsFromUsedInOperatingAndInvestingActivities`, `InterestPaidOnLeaseLiabilitiesClassifiedAsOperatingActivities`, `InterestPaidOtherThanLeaseLiabilitiesClassifiedAsOperatingActivities` |
| Scandinavian Investment Group A/S | DK | Real estate | ebit | `CashFlowFromOperatingAndInvestmentActivities` |
| WRIST SHIP SUPPLY HOLDING A/S | DK | Unclassified | revenue |  |
| Digitalist Group Oyj | FI | Unclassified | ebit, net_profit, ocf |  |
| GOODTECH ASA | NO | Unclassified | ocf | `CostOfSalesAndSubcontractorCost`, `NetOperatingRevenueAfterExternalProjectCosts`, `OperatingProfitAndLossBeforeDepreciationAndImpairment` |
| GRIEG SEAFOOD ASA | NO | Unclassified | ebit | `EBITEarningsBeforeInterestsAndTaxesCashFlow`, `FairValueAdjustmentOfBiologicalAssetsCashFlow` |
| Hafnia Limited | NO | Unclassified | revenue | `CharterRevenueFromExternalShips`, `CharterRevenueFromHafniaShips`, `ProfitLossFromOperatingActivitiesBeforeInterestTaxesDepreciationAndAmortisationExpense` |
| KMC PROPERTIES ASA | NO | Real estate | revenue, ebit, net_profit, ocf |  |
| MOWI ASA | NO | Unclassified | ebit | `OtherNonOperatingIncomeExpense` |
| ODFJELL SE | NO | Transport & shipping | ebit | `GrossProfitIncludingOperatingExpenses`, `ProfitLossFromOperatingActivitiesBeforeDepreciationAmortizationAndCapitalGainsLosses`, `ProfitLossFromOperatingActivitiesIncludingShareOfProfitFromAssociatesAndJointVentures` |
| PCI BIOTECH HOLDING ASA | NO | Unclassified | revenue |  |
| SATS ASA | NO | Industrials | ebit | `OperatingProfitExcludingImpairment`, `TotalOperatingExpensesExcludingImpairment` |
| SoftwareOne Holding AG | NO | Unclassified | ebit |  |
| TREASURE AS | NO | Unclassified | revenue | `OperatingExpensePaidClassifiedAsOperatingActivities`, `OtherIncomeClassifiedAsOperatingActivities`, `ShareOfOtherComprehensiveIncomeOfAssociatesAccountedForUsingEquityMethodThatWillBeReclassifiedToProfitOrLossNetOfTax` |
| Younited Financial S.A. | NO | Unclassified | ebit |  |
| AB Sagax | SE | Real estate | ebit | `AOfWhichProfitFromPropertyManagementFromJointVentures`, `EOfWhichProfitFromPropertyManagement`, `OperatingCostsExcludingRepairsAndMaintenence` |
| Altra Fastigheter AB | SE | Real estate | ebit | `GainsLossesOnFairValueAdjustmentCooperationAgreements`, `InterestPaidOnBondsClassifiedAsOperatingActivities`, `InterestPaidOtherThanInterestPaidOnBondsClassifiedAsOperatingActivities` |
| Atrium Ljungberg AB | SE | Real estate | ebit | `BruttoreslutatVaravbruttoresultatfastighetsforvaltning`, `BruttoresultatVaravbruttoresultatprojektochentreprenadverksamhet`, `Resultatforevardeforandringar` |
| Brinova Fastigheter AB (publ) | SE | Real estate | ebit | `Foervaltningsresultat` |
| Catena AB | SE | Real estate | ebit | `ProfitFromPropertyManagement` |
| Cibus Nordic Real Estate AB (publ) | SE | Real estate | ebit | `Foervaltningsresultat` |
| Corem Property Group AB | SE | Real estate | ebit |  |
| Fastighets AB Balder | SE | Real estate | ebit | `AndelIResultatFrånIntressebolagJointVenturesVaravFörvaltningsresultat`, `AndelIResultatFrånIntressebolagJointVenturesVaravSkatt`, `AndelIResultatFrånIntressebolagJointVenturesVaravVärdeförändringar` |
| Fastighetsbolaget Emilshus AB | SE | Real estate | ebit | `Foervaltningsresultat` |
| Fortinova Fastigheter AB (publ) | SE | Real estate | ebit | `ProfitLossFromPropertyManagement` |
| GARO Aktiebolag | SE | Unclassified | net_profit | `LiabilitiesDirectlyAttributableToSales` |
| Gruvaktiebolaget Viscaria | SE | Unclassified | revenue |  |
| Havsfrun Investment AB | SE | Unclassified | revenue |  |
| John Mattson Fastighetsföretagen AB (publ) | SE | Real estate | ebit | `OperatingCosts` |
| K-Fast Holding AB | SE | Real estate | ebit | `DirectOperatingExpenseFromInvestmentPropertyGeneratingRentalIncomeExcludingRepairsAndMaintenanceExpense`, `OperatingExpenseFromConstructionContracts`, `ProfitLossBeforeTaxAndFairValueAdjustments` |
| KlaraBo Sverige AB | SE | Real estate | ebit | `Foervaltningsresultat`, `Roerelseresultat` |
| Linc AB | SE | Unclassified | revenue | `ResultatFranFoervaltningsverksamheten` |
| Logistea AB | SE | Real estate | ebit | `ProfitBeforeChangesOfValue` |
| Lundin Gold Inc. | SE | Unclassified | ebit |  |
| Lundin Mining Corporation | SE | Unclassified | ebit | `ProfitLossFromContinuingOperationsAttributableToOwnersOfParent` |
| Mangold AB | SE | Unclassified | ebit | `ResultatFoereKreditfoerluster` |
| Medicover AB | SE | Unclassified | revenue |  |
| NAXS AB (publ) | SE | Unclassified | revenue | `FinanceIncomeAndInterestRevenueCalculatedUsingEffectiveInterestMethod`, `NonCurrentFinancialAssetsAtFairValueThroughProfitOrLossFunds`, `ProceedsFromSalesOfOtherNonCurrentFinancialAssetsClassifiedAsInvestingActivities` |
| NP3 Fastigheter AB | SE | Real estate | ebit | `Forvaltningsresultat`, `ForvaltningsresultatFranIntresseforetagOchJointVenture`, `ResultatEfterFinansiellaKostnader` |
| Neobo Fastigheter AB (publ) | SE | Real estate | ebit | `Förvaltningsresultat` |
| Net Insight AB | SE | Unclassified | ocf |  |
| Nivika Fastigheter AB (publ) | SE | Real estate | ebit | `Foervaltningsresultat` |
| Pandox Aktiebolag | SE | Real estate | ebit | `GrossProfitFromHotelOperations`, `GrossProfitFromInvestmentProperty`, `InterestPaidOnLeaseLiabilitiesClassifiedAsOperatingActivities` |
| Platzer Fastigheter Holding AB (publ) | SE | Real estate | ebit | `AndelarIIntressefoeretagOchJointVenturesResultatVaravFoervaltningsresultat`, `AndelarIIntressefoeretagOchJointVenturesResultatVaravSkatt`, `AndelarIIntressefoeretagOchJointVenturesResultatVaravVaerdefoeraendringar` |
| Prisma Properties AB | SE | Real estate | ebit | `Foervaltningsresultat`, `ResultatPerAktieFoereOchEfterUtspaedningKr` |
| SBF Bostad AB (publ) | SE | Real estate | ebit | `Foervaltningsresultat`, `Forvaltningsresultat` |
| Stendörren Fastigheter AB | SE | Real estate | ebit | `NetOperatingIncome` |
| Stenhus Fastigheter i Norden AB (publ) | SE | Real estate | ebit | `ResultatFronIntresseforetagVaravForvaltningsresultat`, `ResultatInklusiveVaerdefoeraendringarIIntressefoeretag`, `ResultatInklusiveVardeforandringarIIntresseforetagVaravFoervaltningsresultat` |
| Truecaller AB | SE | Unclassified | net_profit |  |
| VEF AB (publ) | SE | Unclassified | revenue |  |
| WALLENSTAM AB | SE | Real estate | ebit | `Resultatforevardeforandringarochnedskrivningar` |
| Wihlborgs Fastigheter AB | SE | Real estate | ebit | `Foervaltningsresultat` |

### Auto-matched company-specific concepts (to confirm)

- AUSTEVOLL SEAFOOD ASA: ebit ← `austevollseafood:Ebit`
- BRØNDBYERNES I.F. FODBOLD A/S: ocf ← `ifrs_full:CashFlowsFromUsedInOperatingActivities`
- BRØNDBYERNES I.F. FODBOLD A/S: revenue ← `ifrs_full:Revenue`
- Billerud Aktiebolag (publ): revenue ← `bill:NetSales`
- HUFVUDSTADEN AB: ebit ← `hufv:Rörelseresultat`
- Knowit Aktiebolag (publ): revenue ← `know:NetSales`
- NORGESGRUPPEN ASA: ebit ← `ng:OperatingProfit`
- PANORO ENERGY ASA: revenue ← `panoro:TotalRevenues`
- Trainers' House Oyj: ebit ← `trai:OperatingResult`

## 4. Validation

- balance: assets != equity + liabilities: 50 company-years
- balance: assets != equity and liabilities: 5 company-years
- implausible: equity ratio > 100%: 2 company-years
- implausible: revenue > 20x total assets (scale error?): 1 company-years
- implausible: |EBIT margin| > 100%: 408 company-years
- sign: negative cash: 16 company-years
- sign: negative revenue: 9 company-years
- sign: non-positive total assets: 4 company-years

|EBIT margin| > 100% is mostly early-stage life-science and tech companies with very small revenue; informational only.

## 5. Top 15 flagged companies (for common-sense review)

Rankable universe: 699 companies. Flags per company: {0: 468, 1: 175, 2: 48, 3: 8}.

| # | Company | Country | FY | Flags |
|---|---|---|---|---|
| 1 | DSVM Invest A/S | DK | 2025 | Profit without cash, High accruals, Inventory build-up |
| 2 | AKER HORIZONS ASA | NO | 2024 | High accruals, Receivables outpace sales, Inventory build-up |
| 3 | LEO Pharma A/S | DK | 2025 | High accruals, Receivables outpace sales, Heavy capitalisation |
| 4 | EQL Pharma AB | SE | 2025 | High accruals, Receivables outpace sales, Heavy capitalisation |
| 5 | Pohjolan Voima Oyj | FI | 2025 | Profit without cash, Receivables outpace sales, Leverage creep |
| 6 | BW ENERGY LIMITED | NO | 2025 | Receivables outpace sales, Inventory build-up, Heavy capitalisation |
| 7 | B3 Consulting Group AB (publ) | SE | 2025 | Profit without cash, Acquisition-driven, Leverage creep |
| 8 | Shape Robotics A/S | DK | 2024 | Profit without cash, High accruals, Heavy capitalisation |
| 9 | Stillfront Group AB (publ) | SE | 2025 | Heavy capitalisation, Acquisition-driven |
| 10 | SELVAAG BOLIG ASA | NO | 2025 | Receivables outpace sales, Inventory build-up |
| 11 | AVANCE GAS HOLDING LTD | NO | 2024 | Profit without cash, High accruals |
| 12 | Besqab Bostadsutveckling AB | SE | 2025 | High accruals, Receivables outpace sales |
| 13 | NORDIC BIOSCIENCE HOLDING A/S | DK | 2025 | High accruals, Inventory build-up |
| 14 | GOMSPACE A/S | DK | 2025 | High accruals, Heavy capitalisation |
| 15 | MilDef Group AB | SE | 2025 | High accruals, Inventory build-up |

Flags are prompts for analysis, not conclusions. See `data/flags.json` → `meta.rules` for definitions and innocent explanations.
