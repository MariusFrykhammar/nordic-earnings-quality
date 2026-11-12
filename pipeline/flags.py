"""Red flags (section 5 of the plan). Flags are prompts for analysis, not conclusions.

Each flag is evaluated on a company's latest fiscal year (t) using t-1 and t-2 where needed.
Thresholds live in RULES so the methodology page and the code stay in sync.
"""
from __future__ import annotations

from statistics import quantiles

RULES = {
    "profit_without_cash": {
        "title": "Profit without cash",
        "rule": "Net profit up at least 10% while operating cash flow fell at least 10% in the latest year; "
        "or 3-year operating cash flow / EBIT below 0.6 and in the bottom 10% of peers "
        "(only when 3-year EBIT is at least 2% of revenue).",
        "signals": "Earnings are not turning into cash.",
        "innocent": "Fast growth ties up working capital; large one-off tax or pension payments; timing of customer prepayments.",
        "np_growth_min": 0.10, "ocf_growth_max": -0.10, "conv3_abs": 0.6, "conv3_pct": 10,
    },
    "high_accruals": {
        "title": "High accruals",
        "rule": "(Net profit - operating cash flow) / average total assets in the top 10% of peers and above 5%.",
        "signals": "Earnings quality (Sloan, 1996): a large share of profit comes from accruals rather than cash.",
        "innocent": "Non-cash gains (asset sales, revaluations), growth investment in working capital.",
        "pct": 90, "abs_min": 0.05,
    },
    "receivables_outpace_sales": {
        "title": "Receivables outpace sales",
        "rule": "Trade receivables grew at least 20 percentage points faster than revenue, with receivables at least 5% of revenue.",
        "signals": "Aggressive revenue recognition, or customers paying more slowly.",
        "innocent": "A large order invoiced near year-end, acquisitions at year-end, a change in factoring.",
        "gap_min": 0.20, "materiality": 0.05,
    },
    "inventory_build_up": {
        "title": "Inventory build-up",
        "rule": "Inventories grew at least 20 percentage points faster than revenue, with inventories at least 5% of revenue.",
        "signals": "Weaker demand, possible future write-downs.",
        "innocent": "Stocking up ahead of launches or expected price rises, supply-chain buffers, acquisitions.",
        "gap_min": 0.20, "materiality": 0.05,
    },
    "heavy_capitalisation": {
        "title": "Heavy capitalisation",
        "rule": "Spending on intangible assets (incl. capitalised development) at least 5% of revenue, in the top 10% of peers, "
        "and at least 1 percentage point higher than two years earlier.",
        "signals": "Costs moved from the income statement to the balance sheet.",
        "innocent": "Software and R&D-heavy business models capitalise development under IAS 38 by design.",
        "abs_min": 0.05, "pct": 90, "rise_min": 0.01,
    },
    "acquisition_driven": {
        "title": "Acquisition-driven",
        "rule": "Goodwill / equity at least 0.8 and up at least 0.1 over two years.",
        "signals": "Growth bought rather than built; impairment risk.",
        "innocent": "Serial acquirers with a disciplined model; goodwill is tested for impairment yearly.",
        "level_min": 0.8, "rise_min": 0.1,
    },
    "leverage_creep": {
        "title": "Leverage creep",
        "rule": "Net debt / EBITDA at least 2.5x and up at least 1.0x over two years, while cash conversion fell.",
        "signals": "Balance-sheet strain.",
        "innocent": "Debt-funded acquisitions that have not yet contributed a full year of EBITDA.",
        "level_min": 2.5, "rise_min": 1.0,
    },
}

# Property companies report fair-value changes in profit, which distorts profit-vs-cash measures,
# and run structurally higher leverage.
# Property companies and residential developers hold projects as inventory and receivables by design.
EXCLUDE_BY_SECTOR = {"Real estate": {"profit_without_cash", "high_accruals", "leverage_creep",
                                     "inventory_build_up", "receivables_outpace_sales"}}


def percentile(values: list[float], pct: int) -> float | None:
    vals = sorted(v for v in values if v is not None)
    if len(vals) < 10:
        return None
    return quantiles(vals, n=100, method="inclusive")[pct - 1]


def evaluate(series: dict[int, dict], t: int, sector: str, peers: dict[str, dict[str, float | None]]) -> list[dict]:
    """series[year] = {'v': values+derived, 'm': metrics}. peers: thresholds for the company's peer group."""
    cur = series.get(t)
    if not cur:
        return []
    m, v = cur["m"], cur["v"]
    p1 = series.get(t - 1, {"m": {}, "v": {}})
    p2 = series.get(t - 2, {"m": {}, "v": {}})
    out = []
    excl = EXCLUDE_BY_SECTOR.get(sector, set())

    def add(key, evidence):
        if key not in excl:
            out.append({"flag": key, "title": RULES[key]["title"], "evidence": evidence})

    # 1 profit without cash
    r = RULES["profit_without_cash"]
    npg, ocfg = m.get("net_profit_growth"), m.get("ocf_growth")
    hit = False
    ev = {}
    if npg is not None and ocfg is not None and npg >= r["np_growth_min"] and ocfg <= r["ocf_growth_max"]:
        hit = True
        ev.update(net_profit_growth=npg, ocf_growth=ocfg)
    conv3 = m.get("cash_conversion_3y")
    if conv3 is not None:
        thr = peers.get("cash_conversion_3y_p10")
        if thr is not None and conv3 < min(r["conv3_abs"], thr):
            hit = True
            ev.update(cash_conversion_3y=conv3, peer_p10=thr)
    if hit:
        add("profit_without_cash", ev)

    # 2 high accruals
    r = RULES["high_accruals"]
    acc, thr = m.get("accruals_ratio"), peers.get("accruals_ratio_p90")
    if acc is not None and thr is not None and acc >= max(thr, r["abs_min"]):
        add("high_accruals", {"accruals_ratio": acc, "peer_p90": thr})

    # 3/4 receivables, inventories
    for key, g, ratio in (
        ("receivables_outpace_sales", "receivables_growth", "receivables_to_revenue"),
        ("inventory_build_up", "inventory_growth", "inventory_to_revenue"),
    ):
        r = RULES[key]
        gx, rg, mat = m.get(g), m.get("revenue_growth"), m.get(ratio)
        if gx is not None and rg is not None and mat is not None and gx - rg >= r["gap_min"] and mat >= r["materiality"]:
            add(key, {g: gx, "revenue_growth": rg, ratio: mat})

    # 5 heavy capitalisation
    r = RULES["heavy_capitalisation"]
    ic, thr = m.get("intangible_capex_to_revenue"), peers.get("intangible_capex_to_revenue_p90")
    base = p2["m"].get("intangible_capex_to_revenue")
    if base is None:
        base = p1["m"].get("intangible_capex_to_revenue")
    if ic is not None and thr is not None and base is not None and ic >= max(thr, r["abs_min"]) and ic - base >= r["rise_min"]:
        add("heavy_capitalisation", {"intangible_capex_to_revenue": ic, "earlier": base, "peer_p90": thr})

    # 6 acquisition-driven
    r = RULES["acquisition_driven"]
    gw, gw2 = m.get("goodwill_to_equity"), p2["m"].get("goodwill_to_equity")
    if gw is not None and gw2 is not None and gw >= r["level_min"] and gw - gw2 >= r["rise_min"]:
        add("acquisition_driven", {"goodwill_to_equity": gw, "two_years_earlier": gw2, "basis": v.get("goodwill_basis")})

    # 7 leverage creep
    r = RULES["leverage_creep"]
    nd, nd2 = m.get("net_debt_ebitda"), p2["m"].get("net_debt_ebitda")
    cc, cc2 = m.get("cash_conversion"), p2["m"].get("cash_conversion")
    if None not in (nd, nd2, cc, cc2) and nd >= r["level_min"] and nd - nd2 >= r["rise_min"] and cc < cc2:
        add("leverage_creep", {"net_debt_ebitda": nd, "two_years_earlier": nd2, "cash_conversion": cc, "cash_conversion_two_years_earlier": cc2})

    return out


def cash_conversion_3y(series: dict[int, dict], t: int) -> float | None:
    ocf3 = [series.get(y, {}).get("v", {}).get("ocf") for y in (t - 2, t - 1, t)]
    ebit3 = [series.get(y, {}).get("v", {}).get("ebit") for y in (t - 2, t - 1, t)]
    rev3 = [series.get(y, {}).get("v", {}).get("revenue") for y in (t - 2, t - 1, t)]
    if all(x is not None for x in ocf3 + ebit3) and sum(ebit3) > 0:
        # a near-zero EBIT makes the ratio meaningless: require EBIT of at least 2% of revenue over 3 years
        if all(x is not None for x in rev3) and sum(rev3) > 0 and sum(ebit3) < 0.02 * sum(rev3):
            return None
        return sum(ocf3) / sum(ebit3)
    return None
