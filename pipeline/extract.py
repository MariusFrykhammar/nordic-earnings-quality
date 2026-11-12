"""Extract consolidated (group-level) monetary facts from an xBRL-JSON report.

A consolidated fact has only the core dimensions concept, entity, period, unit (and language).
Any other dimension means a segment or breakdown, which v1 skips.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from datetime import date, timedelta
from pathlib import Path

from . import fetch

CORE_DIMS = {"concept", "entity", "period", "unit", "language"}
FACT_CACHE = fetch.CACHE / "facts"


def consolidated_facts(report: dict) -> list[list]:
    """Return [[concept, period, unit, value], ...] for numeric monetary consolidated facts."""
    out = []
    seen = set()
    for f in (report.get("facts") or {}).values():
        d = f.get("dimensions") or {}
        if set(d) - CORE_DIMS:
            continue
        unit = d.get("unit") or ""
        if not unit.startswith("iso4217:") or "/" in unit:
            continue
        try:
            v = float(f.get("value"))
        except (TypeError, ValueError):
            continue
        key = (d.get("concept"), d.get("period"), unit)
        if key in seen:  # duplicate facts (same value, different decimals/ids)
            continue
        seen.add(key)
        out.append([d.get("concept"), d.get("period"), unit, v])
    return out


def get_facts(json_url: str) -> list[list] | None:
    """Download + extract, cached as small gz files so reruns don't refetch."""
    p = FACT_CACHE / (hashlib.sha1(json_url.encode()).hexdigest() + ".json.gz")
    if p.exists():
        return json.loads(gzip.decompress(p.read_bytes()))
    url = json_url if json_url.startswith("http") else fetch.BASE + json_url
    rep = fetch.get_json(url, use_cache=False, store=False)
    if rep is None:
        return None
    facts = consolidated_facts(rep)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(gzip.compress(json.dumps(facts).encode()))
    return facts


# ---------------------------------------------------------------- periods

def _d(s: str) -> date:
    return date.fromisoformat(s[:10])


def parse_period(p: str):
    """('D', start, end_boundary) for durations, ('I', None, boundary) for instants.

    xBRL-JSON uses exclusive end boundaries: '2025-01-01T00:00:00/2026-01-01T00:00:00' is FY2025;
    the instant '2026-01-01T00:00:00' is the balance at 31 Dec 2025.
    """
    if not p:
        return None
    if "/" in p:
        s, e = p.split("/")
        return ("D", _d(s), _d(e))
    return ("I", None, _d(p))


def fy_end(boundary: date) -> date:
    """Last day of the fiscal year from an exclusive boundary."""
    return boundary - timedelta(days=1)


def annual(start: date, end: date) -> bool:
    return 330 <= (end - start).days <= 400
