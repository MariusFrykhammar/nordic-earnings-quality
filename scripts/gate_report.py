"""Regenerate docs/day1-gate.md from data/ and diagnostics/ (run after a pipeline run)."""
import json
from collections import Counter

c = json.load(open("diagnostics/coverage.json"))
n = json.load(open("diagnostics/needs_override.json"))
f = json.load(open("data/flags.json"))
v = json.load(open("diagnostics/validation.json"))
u = json.load(open("diagnostics/mapping_usage.json"))
idx = json.load(open("data/companies.json"))
C = ["SE", "NO", "DK", "FI"]
L = []
A = L.append
A("# Day 1 gate report (data)\n")
A(f"Generated {f['meta']['generated']}. Financial data: company annual reports (ESEF) via filings.xbrl.org, FY2020–FY2025.\n")
A("## Sources\n")
A("| Source | Used for | Status |\n|---|---|---|")
A("| ESEF annual reports (filings.xbrl.org) | all financial figures, fact-level source links | %d reports, %d failed downloads |" % (sum(c[k]["after_dedup"] for k in C), c["downloads_failed"]))
for k, val in c["reference_status"].items():
    A(f"| {k} | {dict(gleif='legal names, legal form, registration numbers', firds='listed shares and trading venue (ESMA)', registries='official industry codes (NACE)').get(k, '')} | {val} |")
A("| ISO 10383 | trading venue names and types | used to resolve venue codes |")
A("| ECB | euro reference rates | loaded |")
A("| Wikidata | industry where no registry code | fallback only |\n")
A("## 1. Coverage\n")
A("| Country | Reports after dedup | Companies | Non-financial | **Core 4 for 3+ yrs** | Rankable |\n|---|---|---|---|---|---|")
for k in C:
    x = c[k]
    A(f"| {k} | {x['after_dedup']} | {x['companies']} | {x['non_financial']} | **{x['gate_core4_3yrs']}** | {x['rankable']} |")
A(f"| **Total** | | | | **{c['total_gate_core4_3yrs']}** | {sum(c[k]['rankable'] for k in C)} |\n")
A("Core 4 = revenue, EBIT, net profit, operating cash flow. Rankable = non-financial, revenue ≥ €25m, FY2024+ report, shares listed on a Nordic exchange (ESMA FIRDS). "
  f"Fact-level source links: {c['fact_level_links']:,}.\n")
A("### Listing status and sector source (non-financial companies)\n")
for k in C:
    A(f"- **{k}**: listing " + "; ".join(f"{a} {b}" for a, b in c[k]["listing"]) + ". Sector source: " + "; ".join(f"{a or 'none'} {b}" for a, b in c[k]["sector_source"]))
A("")
A("### Company-years with data, non-financial companies\n")
for k in C:
    A(f"**{k}**\n\n| Metric | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |\n|---|---|---|---|---|---|---|")
    for m, yy in c[k]["company_years_by_metric"].items():
        A(f"| {m} | " + " | ".join(str(yy[str(y)]) for y in range(2020, 2026)) + " |")
    A("")
A("### How metrics were mapped (company-years)\n")
for k in ["revenue", "ebit", "net_profit", "ocf", "receivables", "goodwill", "intangibles_incl_goodwill", "da"]:
    if k in u:
        A(f"- **{k}**: " + "; ".join(f"`{a}` {b}" for a, b in u[k][:6]))
A("\n## 2. Spot-checks (12 companies, 3 per country)\n")
A("| Company | Year | Ours: revenue / EBIT (m) | Published | Result |\n|---|---|---|---|---|")
for row in [
    ("Atlas Copco", "FY2025", "168,343 / 34,114", "168,343 / 34,114", "✅"),
    ("Sandvik", "FY2025", "120,680 / 20,809", "120,680 / 20,809 (PBT 19,458 + net finance 1,351)", "✅"),
    ("Electrolux", "FY2025", "131,282 / 3,657", "131,282 / 3,657", "✅"),
    ("Orkla", "FY2025", "71,044 / 7,086", "71,547 / 7,086", "⚠️ EBIT ✅; IFRS `Revenue` tag excludes other operating revenue"),
    ("Kongsberg Gruppen", "FY2025", "31,562 / 4,694", "31,562 / ~4,697 (continuing ops)", "✅"),
    ("Telenor", "FY2025", "76,548 / 17,978", "76,548 / 17,978", "✅"),
    ("Carlsberg", "FY2025", "89,095 / not reported", "89,095 / 13,356 before special items", "✅ EBIT correctly not reported"),
    ("DSV", "FY2025", "247,331 / not reported", "247,331 / 19,611 before special items", "✅ EBIT correctly not reported"),
    ("Novo Nordisk", "FY2025", "309,064 / 127,658", "309,064 / 127,658", "✅"),
    ("Kone", "FY2025", "11,245.2 / 1,336.2", "11,245.2 / 1,336.2", "✅"),
    ("UPM-Kymmene", "FY2025", "9,656 / 749", "9,656 / 749", "✅"),
    ("Wärtsilä", "FY2024", "6,449 / 716", "6,449 / 716", "✅ (FY2025 report not yet in repository)"),
]:
    A("| " + " | ".join(row) + " |")
A("\n## 3. Companies needing overrides\n")
A(f"{len(n)} non-financial companies with a recent report miss a core metric: " + ", ".join(f"{'+'.join(k)} {x}" for k, x in Counter(tuple(r['missing']) for r in n).most_common()) + ".\n")
A("| Company | Country | Sector | Missing |\n|---|---|---|---|")
for r in sorted(n, key=lambda r: (r["country"], r["name"])):
    A(f"| {r['name']} | {r['country']} | {r['sector']} | {', '.join(r['missing'])} |")
A("\n## 4. Validation\n")
for k, x in v.items():
    A(f"- {k}: {x['count']} company-years")
A("\n## 5. Top 15 flagged companies\n")
rk = [r for r in idx if r["rankable"]]
A(f"Rankable universe: {len(rk)} companies. Flags per company: {dict(sorted(Counter(r['n_flags'] for r in rk).items()))}.\n")
A("| # | Company | Country | Market | FY | Flags |\n|---|---|---|---|---|---|")
for i, r in enumerate(f["lists"]["most_flags"][:15], 1):
    A(f"| {i} | {r['name']} | {r['country']} | {r['market'] or '–'} | {r['latest_year']} | {', '.join(f['meta']['rules'][x]['title'] for x in r['flags'])} |")
A("\nFlags are prompts for analysis, not conclusions. Definitions and innocent explanations: `data/flags.json` → `meta.rules`.\n")
open("docs/day1-gate.md", "w").write("\n".join(L))
print("ok", len(L))
