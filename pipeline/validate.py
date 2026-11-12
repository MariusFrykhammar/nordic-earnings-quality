"""Data checks. Results go to diagnostics/validation.json; nothing is silently 'fixed'."""
from __future__ import annotations

TOL = 0.005  # 0.5%


def _close(a, b, tol=TOL):
    return abs(a - b) <= tol * max(abs(a), abs(b), 1e-9)


def check_year(v: dict, m: dict) -> list[str]:
    issues = []
    ta, eql, eq, li = v.get("total_assets"), v.get("equity_and_liabilities"), v.get("equity"), v.get("liabilities")
    if ta is not None and eql is not None and not _close(ta, eql):
        issues.append("balance: assets != equity and liabilities")
    if ta is not None and eq is not None and li is not None and not _close(ta, eq + li):
        issues.append("balance: assets != equity + liabilities")
    if v.get("revenue") is not None and v["revenue"] < 0:
        issues.append("sign: negative revenue")
    if ta is not None and ta <= 0:
        issues.append("sign: non-positive total assets")
    if v.get("cash") is not None and v["cash"] < 0:
        issues.append("sign: negative cash")
    if m.get("ebit_margin") is not None and abs(m["ebit_margin"]) > 1.0:
        issues.append("implausible: |EBIT margin| > 100%")
    if m.get("equity_ratio") is not None and m["equity_ratio"] > 1.0:
        issues.append("implausible: equity ratio > 100%")
    if v.get("revenue") is not None and ta is not None and ta > 0 and v["revenue"] / ta > 20:
        issues.append("implausible: revenue > 20x total assets (scale error?)")
    return issues
