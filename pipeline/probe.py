"""Probe: inspect the API and a few reports per country at fact level.

Writes diagnostics/probe/*.json so the structure can be checked before the full build.
"""
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from . import fetch

OUT = Path("diagnostics/probe")

# A few large, well-known non-financial companies per country (matched on entity name).
SAMPLES = {
    "SE": ["atlas copco", "volvo", "hexagon"],
    "NO": ["orkla", "equinor", "telenor"],
    "DK": ["carlsberg", "dsv", "novo nordisk"],
    "FI": ["kone", "upm", "nokia"],
}


def summarise(report: dict) -> dict:
    facts = report.get("facts", {})
    consolidated = []
    dims = Counter()
    for f in facts.values():
        d = f.get("dimensions", {})
        extra = set(d) - {"concept", "entity", "period", "unit", "language"}
        for k in extra:
            dims[k.split(":")[0]] += 1
        if not extra:
            consolidated.append(
                {"c": d.get("concept"), "p": d.get("period"), "u": d.get("unit"), "v": f.get("value"), "dec": f.get("decimals")}
            )
    consolidated.sort(key=lambda x: (x["c"] or "", x["p"] or ""))
    return {
        "document_info": report.get("documentInfo", {}),
        "n_facts": len(facts),
        "n_consolidated": len(consolidated),
        "extra_dimension_prefixes": dims.most_common(10),
        "consolidated": consolidated,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    overview = {}
    for c in fetch.COUNTRIES:
        filings = fetch.list_filings(c, {"filter[period_end]": "2025-12-31"})
        overview[c] = {"n_filings_fy2025_dec": len(filings), "attribute_keys": sorted(filings[0].keys()) if filings else []}
        (OUT / f"listing_{c}_sample.json").write_text(json.dumps(filings[:5], indent=1, ensure_ascii=False))
        for want in SAMPLES[c]:
            hits = [f for f in filings if want in (f.get("_name") or "").lower()]
            overview[c][want] = [(f.get("_name"), f.get("_lei"), f.get("json_url")) for f in hits]
            if not hits:
                continue
            f = hits[0]
            rep = fetch.get_report(f.get("json_url"))
            if not rep:
                continue
            s = summarise(rep)
            s["filing"] = {k: f.get(k) for k in ("_name", "_lei", "period_end", "json_url", "viewer_url", "processed", "date_added")}
            (OUT / f"{c}_{want.replace(' ', '_')}.json").write_text(json.dumps(s, indent=1, ensure_ascii=False))
            print(c, want, s["n_facts"], s["n_consolidated"])
    (OUT / "overview.json").write_text(json.dumps(overview, indent=1, ensure_ascii=False))
    print(json.dumps({c: v["n_filings_fy2025_dec"] for c, v in overview.items()}))
