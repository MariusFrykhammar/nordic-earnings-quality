"""ECB euro reference rates (units of currency per 1 EUR), monthly average and end-of-month.

Income and cash-flow items convert at the average over the fiscal year; balance-sheet items
at the rate for the fiscal year-end month.
"""
from __future__ import annotations

import csv
import io
from datetime import date

import requests

CURRENCIES = ["SEK", "NOK", "DKK", "USD", "GBP", "CHF", "ISK", "PLN", "JPY", "CAD", "AUD", "CNY"]
URL = (
    "https://data-api.ecb.europa.eu/service/data/EXR/M.{cur}.EUR.SP00.A+E"
    "?format=csvdata&startPeriod=2018-01"
)


def load() -> dict:
    """{'avg': {cur: {'YYYY-MM': rate}}, 'end': {...}}"""
    out = {"avg": {}, "end": {}}
    r = requests.get(URL.format(cur="+".join(CURRENCIES)), timeout=60)
    r.raise_for_status()
    for row in csv.DictReader(io.StringIO(r.text)):
        suffix = row.get("EXR_SUFFIX") or row.get("KEY", "")[-1:]
        kind = "avg" if suffix == "A" else "end"
        try:
            out[kind].setdefault(row["CURRENCY"], {})[row["TIME_PERIOD"]] = float(row["OBS_VALUE"])
        except (KeyError, ValueError):
            continue
    return out


def _months_back(end: date, n: int) -> list[str]:
    y, m = end.year, end.month
    res = []
    for _ in range(n):
        res.append(f"{y:04d}-{m:02d}")
        m -= 1
        if m == 0:
            y, m = y - 1, 12
    return res


def rate(rates: dict, cur: str, fy_end: date, kind: str) -> float | None:
    """Units of `cur` per EUR. kind 'avg' (12-month average to fy_end) or 'end'."""
    if cur == "EUR":
        return 1.0
    table = rates.get(kind, {}).get(cur)
    if not table:
        return None
    if kind == "end":
        return table.get(f"{fy_end.year:04d}-{fy_end.month:02d}")
    vals = [table[m] for m in _months_back(fy_end, 12) if m in table]
    return sum(vals) / len(vals) if len(vals) >= 10 else None
