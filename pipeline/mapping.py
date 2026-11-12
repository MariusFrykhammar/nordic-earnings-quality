"""Map reported concepts to the scanner's metrics.

Order: per-company override (mapping/overrides.yaml) -> IFRS concepts in priority order ->
sums of IFRS components -> company extension concepts matched by name (marked 'extension-auto'
so they can be reviewed and confirmed as overrides). Nothing found -> metric is absent
("not reported"); we never guess.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

I = "ifrs-full:"

# metric -> (kind, [single concepts in priority order], [component sums tried after singles])
# kind: D = duration (flow), I = instant (balance)
CONCEPTS: dict[str, tuple[str, list[str], list[list[str]]]] = {
    "revenue": ("D", ["Revenue", "RevenueFromContractsWithCustomers", "RevenueAndOperatingIncome"], []),
    "ebit": ("D", ["ProfitLossFromOperatingActivities"], []),
    "net_profit": ("D", ["ProfitLoss"], []),
    "net_profit_owners": ("D", ["ProfitLossAttributableToOwnersOfParent"], []),
    "total_assets": ("I", ["Assets", "EquityAndLiabilities"], []),
    "equity": ("I", ["Equity"], []),
    "cash": ("I", ["CashAndCashEquivalents"], []),
    "borrowings_noncurrent": ("I", ["NoncurrentBorrowings", "LongtermBorrowings", "NoncurrentPortionOfNoncurrentLoansReceived"], []),
    "borrowings_current": (
        "I",
        ["CurrentBorrowingsAndCurrentPortionOfNoncurrentBorrowings", "CurrentBorrowings", "CurrentLoansReceivedAndCurrentPortionOfNoncurrentLoansReceived"],
        [["ShorttermBorrowings", "CurrentPortionOfLongtermBorrowings"]],
    ),
    "borrowings_total": ("I", ["Borrowings"], []),
    "lease_liabilities": ("I", ["LeaseLiabilities"], [["NoncurrentLeaseLiabilities", "CurrentLeaseLiabilities"]]),
    "receivables": ("I", ["CurrentTradeReceivables", "TradeReceivables", "TradeAndOtherCurrentReceivables", "TradeAndOtherReceivables"], []),
    "inventories": ("I", ["Inventories"], []),
    "goodwill": ("I", ["Goodwill"], []),
    "intangibles_ex_goodwill": ("I", ["IntangibleAssetsOtherThanGoodwill"], []),
    "intangibles_incl_goodwill": ("I", ["IntangibleAssetsAndGoodwill"], [["Goodwill", "IntangibleAssetsOtherThanGoodwill"]]),
    "investment_property": ("I", ["InvestmentProperty"], []),
    "ocf": ("D", ["CashFlowsFromUsedInOperatingActivities"], []),
    "capex_ppe": (
        "D",
        [
            "PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities",
            "PurchaseOfPropertyPlantAndEquipment",
        ],
        [],
    ),
    "capex_intangible": ("D", ["PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities", "PurchaseOfIntangibleAssets"], []),
    "capex_combined": (
        "D",
        ["PurchaseOfPropertyPlantAndEquipmentIntangibleAssetsOtherThanGoodwillInvestmentPropertyAndOtherNoncurrentAssets"],
        [],
    ),
    "da": (
        "D",
        [
            "DepreciationAndAmortisationExpense",
            "AdjustmentsForDepreciationAndAmortisationExpense",
            "DepreciationAmortisationAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss",
            "AdjustmentsForDepreciationAndAmortisationExpenseAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss",
        ],
        [["DepreciationExpense", "AmortisationExpense"], ["AdjustmentsForDepreciationExpense", "AdjustmentsForAmortisationExpense"]],
    ),
    # validation only
    "liabilities": ("I", ["Liabilities"], []),
    "equity_and_liabilities": ("I", ["EquityAndLiabilities"], []),
    # financial-sector markers (used for classification only)
    "interest_income": ("D", ["RevenueFromInterest", "InterestRevenueCalculatedUsingEffectiveInterestMethod", "InterestIncome"], []),
    "insurance_revenue": ("D", ["InsuranceRevenue", "RevenueFromInsuranceContractsIssued"], []),
}

# D&A concepts that include impairment: noted in provenance, EBITDA labelled accordingly.
DA_INCLUDES_IMPAIRMENT = {
    "DepreciationAmortisationAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss",
    "AdjustmentsForDepreciationAndAmortisationExpenseAndImpairmentLossReversalOfImpairmentLossRecognisedInProfitOrLoss",
}

# Extension-concept name patterns (local name, lower case, non-letters removed), 5 languages.
EXT_PATTERNS = {
    "revenue": [
        r"^(net)?(sales|revenue|revenues|turnover)(total)?$", r"^totalrevenues?$", r"^netsales", r"^netturnover$",
        r"^nettoomsattning$", r"^nettoomsattningen$", r"^intakter$", r"^driftsinntekter$", r"^salgsinntekter$",
        r"^nettoomsaetning$", r"^omsaetning$", r"^liikevaihto$", r"^operatingrevenues?$",
    ],
    "ebit": [
        r"^operating(profit|income|result)(loss)?$", r"^operatingprofitloss$", r"^ebit$", r"^rorelseresultat$",
        r"^driftsresultat$", r"^resultatafprimaerdrift$", r"^liikevoitto$", r"^liiketulos$", r"^profitlossfromoperations$",
    ],
    "ocf": [
        r"^cashflows?from(used)?(in)?operatingactivities$", r"^netcashfromoperatingactivities$",
        r"^kassaflodefranlopandeverksamhet$", r"^kontantstromfradrift$", r"^liiketoiminnanrahavirta$",
    ],
}
EXT_EXCLUDE = re.compile(
    r"adjusted|underlying|before|excluding|exclspecial|specialitems|comparable|segment|percent|margin|other|"
    r"continuing|discontinued|perShare|justerad|vertailukelpoinen|oikaistu",
    re.I,
)

_OVERRIDES: dict | None = None


def overrides() -> dict:
    global _OVERRIDES
    if _OVERRIDES is None:
        p = Path("mapping/overrides.yaml")
        _OVERRIDES = (yaml.safe_load(p.read_text()) or {}) if p.exists() else {}
    return _OVERRIDES


def _norm(local: str) -> str:
    s = local.lower()
    for a, b in (("å", "a"), ("ä", "a"), ("ö", "o"), ("ø", "o"), ("æ", "ae")):
        s = s.replace(a, b)
    return re.sub(r"[^a-z]", "", s)


def map_year(lei: str, dur: dict[str, float], inst: dict[str, float]) -> tuple[dict, dict]:
    """Map one fiscal year's facts. Returns (values, provenance)."""
    vals: dict[str, float] = {}
    prov: dict[str, str] = {}
    ov = (overrides().get(lei) or {}).get("concepts", {})
    for metric, (kind, singles, sums) in CONCEPTS.items():
        facts = dur if kind == "D" else inst
        if metric in ov:
            if ov[metric] is None:  # explicitly "not reported"
                continue
            if ov[metric] in facts:
                vals[metric], prov[metric] = facts[ov[metric]], "override:" + ov[metric]
                continue
        for c in singles:
            if I + c in facts:
                vals[metric], prov[metric] = facts[I + c], c
                break
        else:
            for parts in sums:
                if all(I + c in facts for c in parts):
                    vals[metric] = sum(facts[I + c] for c in parts)
                    prov[metric] = "+".join(parts)
                    break
            else:
                if metric in EXT_PATTERNS:
                    hit = ext_match(metric, facts)
                    if hit:
                        vals[metric], prov[metric] = facts[hit], "extension-auto:" + hit
    return vals, prov


def ext_match(metric: str, facts: dict[str, float]) -> str | None:
    cands = []
    for c in facts:
        if c.startswith(I):
            continue
        local = c.split(":", 1)[-1]
        if EXT_EXCLUDE.search(local):
            continue
        n = _norm(local)
        if any(re.search(p, n) for p in EXT_PATTERNS[metric]):
            cands.append(c)
    return sorted(cands)[0] if len(cands) == 1 else None  # ambiguous -> not reported
