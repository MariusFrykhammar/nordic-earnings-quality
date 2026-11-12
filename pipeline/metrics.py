"""Per-year metrics from mapped values. All ratios are unitless; growth rates are decimals (0.1 = 10%)."""
from __future__ import annotations


def _div(a, b):
    if a is None or b is None or b == 0:
        return None
    return a / b


def _growth(cur, prev):
    if cur is None or prev is None or prev <= 0:
        return None
    return cur / prev - 1


def _avg(a, b):
    if a is None:
        return None
    return a if b is None else (a + b) / 2


def derived(v: dict) -> dict:
    """Derived levels for one year (no prior year needed)."""
    d = {}
    bt = v.get("borrowings_total")
    nc, cu = v.get("borrowings_noncurrent"), v.get("borrowings_current")
    if bt is not None:
        d["borrowings"], d["borrowings_basis"] = bt, "total"
    elif nc is not None or cu is not None:
        d["borrowings"] = (nc or 0) + (cu or 0)
        d["borrowings_basis"] = "non-current + current" if (nc is not None and cu is not None) else (
            "non-current only" if nc is not None else "current only")
    leases = v.get("lease_liabilities")
    if d.get("borrowings") is not None and v.get("cash") is not None:
        d["net_debt"] = d["borrowings"] + (leases or 0) - v["cash"]
        d["net_debt_basis"] = "incl. leases" if leases is not None else "excl. leases (not reported)"
    if v.get("capex_ppe") is not None or v.get("capex_intangible") is not None:
        d["capex"] = abs(v.get("capex_ppe") or 0) + abs(v.get("capex_intangible") or 0)
    elif v.get("capex_combined") is not None:
        d["capex"] = abs(v["capex_combined"])
    if v.get("ebit") is not None and v.get("da") is not None:
        d["ebitda"] = v["ebit"] + abs(v["da"])
    if v.get("goodwill") is not None:
        d["goodwill_measure"], d["goodwill_basis"] = v["goodwill"], "goodwill"
    elif v.get("intangibles_incl_goodwill") is not None:
        d["goodwill_measure"], d["goodwill_basis"] = v["intangibles_incl_goodwill"], "goodwill incl. other intangibles (combined tag)"
    if d.get("borrowings") is not None and v.get("equity") is not None and v.get("cash") is not None:
        d["capital_employed"] = v["equity"] + d["borrowings"] + (leases or 0) - v["cash"]
    return d


def year_metrics(cur: dict, prev: dict | None) -> dict:
    """cur/prev: merged dicts of mapped values + derived levels."""
    p = prev or {}
    m = {}
    rev = cur.get("revenue")
    m["revenue_growth"] = _growth(rev, p.get("revenue"))
    m["ebit_margin"] = _div(cur.get("ebit"), rev) if rev and rev > 0 else None
    m["net_margin"] = _div(cur.get("net_profit"), rev) if rev and rev > 0 else None
    eq_avg = _avg(cur.get("equity"), p.get("equity"))
    m["roe"] = _div(cur.get("net_profit"), eq_avg) if eq_avg and eq_avg > 0 else None
    ce_avg = _avg(cur.get("capital_employed"), p.get("capital_employed"))
    m["roce"] = _div(cur.get("ebit"), ce_avg) if ce_avg and ce_avg > 0 else None
    ebit = cur.get("ebit")
    m["cash_conversion"] = _div(cur.get("ocf"), ebit) if ebit and ebit > 0 else None
    m["capex_intensity"] = _div(cur.get("capex"), rev) if rev and rev > 0 else None
    ta = cur.get("total_assets")
    m["equity_ratio"] = _div(cur.get("equity"), ta) if ta and ta > 0 else None
    ebitda = cur.get("ebitda")
    m["net_debt_ebitda"] = _div(cur.get("net_debt"), ebitda) if ebitda and ebitda > 0 else None
    ta_avg = _avg(ta, p.get("total_assets"))
    if cur.get("net_profit") is not None and cur.get("ocf") is not None and ta_avg and ta_avg > 0:
        m["accruals_ratio"] = (cur["net_profit"] - cur["ocf"]) / ta_avg
    else:
        m["accruals_ratio"] = None
    m["net_profit_growth"] = _growth(cur.get("net_profit"), p.get("net_profit"))
    m["ocf_growth"] = _growth(cur.get("ocf"), p.get("ocf"))
    m["receivables_growth"] = _growth(cur.get("receivables"), p.get("receivables"))
    m["inventory_growth"] = _growth(cur.get("inventories"), p.get("inventories"))
    m["receivables_to_revenue"] = _div(cur.get("receivables"), rev) if rev and rev > 0 else None
    m["inventory_to_revenue"] = _div(cur.get("inventories"), rev) if rev and rev > 0 else None
    ci = cur.get("capex_intangible")
    m["intangible_capex_to_revenue"] = _div(abs(ci), rev) if ci is not None and rev and rev > 0 else None
    eq = cur.get("equity")
    m["goodwill_to_equity"] = _div(cur.get("goodwill_measure"), eq) if eq and eq > 0 else None
    # headline gap: profit growth minus cash-flow growth (percentage points as decimal)
    if m["net_profit_growth"] is not None and m["ocf_growth"] is not None:
        m["profit_cash_gap"] = m["net_profit_growth"] - m["ocf_growth"]
    else:
        m["profit_cash_gap"] = None
    np_, ocf, pnp, pocf, prev_rev = cur.get("net_profit"), cur.get("ocf"), p.get("net_profit"), p.get("ocf"), p.get("revenue")
    if None not in (np_, ocf, pnp, pocf) and prev_rev and prev_rev > 0:
        m["profit_cash_gap_scaled"] = ((np_ - pnp) - (ocf - pocf)) / prev_rev
    else:
        m["profit_cash_gap_scaled"] = None
    return m
