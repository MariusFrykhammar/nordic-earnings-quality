"""Rough sector classification.

1. Wikidata 'industry' (P452) and 'stock exchange' (P414), looked up by LEI (P1278). Free, best effort.
2. Data rules: banks/insurers (interest or insurance revenue, no revenue/EBIT tags), property companies
   (investment property > 40% of assets), a short manual list of investment companies.
3. Otherwise 'Unclassified'.
"""
from __future__ import annotations

import re
import time

import requests

WD = "https://query.wikidata.org/sparql"
UA = {"User-Agent": "nordic-earnings-quality/0.1 (https://github.com/MariusFrykhammar/nordic-earnings-quality)"}

FINANCIAL_SECTORS = {"Banks & financial services", "Insurance", "Investment companies"}

# checked in order; first keyword hit wins
KEYWORDS = [
    ("Insurance", ["insurance", "reinsurance"]),
    ("Banks & financial services", ["bank", "financial services", "finance", "asset management", "credit", "payment", "stock exchange", "fintech"]),
    ("Investment companies", ["investment company", "private equity", "venture capital", "holding company", "investment"]),
    ("Real estate", ["real estate", "property", "properties"]),
    ("Health care", ["pharmaceutical", "health", "medical", "biotech", "life science", "drug", "diagnostic", "dental", "hospital"]),
    ("Technology", ["software", "information technology", "computer", "internet", "semiconductor", "electronic", "video game", "it service", "technology", "cybersecurity", "artificial intelligence"]),
    ("Telecom & media", ["telecommunication", "media", "broadcast", "publishing", "mass media", "entertainment", "advertising"]),
    ("Utilities", ["utility", "electricity", "electric power", "power generation", "district heating", "renewable energy", "wind power", "hydropower"]),
    ("Energy", ["petroleum", "oil", "natural gas", "energy", "offshore", "drilling"]),
    ("Transport & shipping", ["shipping", "transport", "logistics", "airline", "aviation", "freight", "ferry", "tanker", "port"]),
    ("Materials", ["mining", "steel", "paper", "forest", "chemical", "metal", "pulp", "packaging", "building material", "cement", "aluminium", "timber"]),
    ("Consumer", ["retail", "food", "beverage", "clothing", "fashion", "consumer", "hotel", "restaurant", "gambling", "gaming", "betting", "furniture", "cosmetic", "seafood", "aquaculture", "fishing", "salmon", "brewery", "tobacco", "toy", "e-commerce", "travel"]),
    ("Industrials", ["engineering", "machinery", "construction", "manufactur", "industr", "automotive", "aerospace", "defence", "defense", "conglomerate", "vehicle", "equipment", "tool", "security", "consulting", "staffing", "services"]),
]

INVESTMENT_COMPANY_NAMES = [
    "investor ab", "investor aktiebolag", "industrivärden", "kinnevik", "latour", "lundbergföretagen", "bure equity",
    "svolder", "creades", "öresund", "spiltan", "vnv global", "traction", "aker asa", "investmentaktiebolaget",
]


def wikidata(leis: list[str]) -> dict[str, dict]:
    """{lei: {'industries': [...], 'exchanges': [...], 'wikidata': Qid}}"""
    out: dict[str, dict] = {}
    for i in range(0, len(leis), 150):
        chunk = leis[i : i + 150]
        values = " ".join(f'"{l}"' for l in chunk)
        q = f"""SELECT ?lei ?item ?industryLabel ?exchangeLabel ?ticker WHERE {{
          VALUES ?lei {{ {values} }}
          ?item wdt:P1278 ?lei .
          OPTIONAL {{ ?item wdt:P452 ?industry . }}
          OPTIONAL {{ ?item p:P414 ?st . ?st ps:P414 ?exchange . OPTIONAL {{ ?st pq:P249 ?ticker . }} }}
          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
        }}"""
        for attempt in range(3):
            try:
                r = requests.post(WD, data={"query": q, "format": "json"}, headers=UA, timeout=90)
                r.raise_for_status()
                for b in r.json()["results"]["bindings"]:
                    lei = b["lei"]["value"]
                    rec = out.setdefault(lei, {"industries": [], "exchanges": [], "tickers": [],
                                               "wikidata": b["item"]["value"].rsplit("/", 1)[-1]})
                    for k, field in (("industryLabel", "industries"), ("exchangeLabel", "exchanges"), ("ticker", "tickers")):
                        v = b.get(k, {}).get("value")
                        if v and v not in rec[field]:
                            rec[field].append(v)
                break
            except Exception as e:  # best effort
                print(f"  ! wikidata chunk {i}: {e}")
                time.sleep(5)
        time.sleep(1)
    return out


def from_industries(industries: list[str]) -> str | None:
    text = " | ".join(industries).lower()
    for sector, kws in KEYWORDS:
        if any(k in text for k in kws):
            return sector
    return None


def classify(name: str, wd: dict | None, latest: dict, registry: dict | None = None) -> tuple[str, str]:
    """Return (sector, basis). Order: manual list, statement-based rules, official registry (NACE),
    name rules for investment vehicles, Wikidata, name keywords."""
    from .sources import nace_sector

    n = (name or "").lower()
    if any(k in n for k in INVESTMENT_COMPANY_NAMES):
        return "Investment companies", "manual list"
    rev, np_ = latest.get("revenue"), latest.get("net_profit")
    if np_ is not None and np_ > 0 and rev is not None and np_ > 2 * max(rev, 0):
        return "Investment companies", "data: net profit > 2x revenue (investment gains)"
    has_rev = latest.get("revenue") is not None
    has_ebit = latest.get("ebit") is not None
    if latest.get("insurance_revenue") is not None and not has_ebit:
        return "Insurance", "data: insurance revenue"
    ii, ta0 = latest.get("interest_income"), latest.get("total_assets")
    if not has_rev and (latest.get("fee_commission_income") is not None or (ii and ta0 and ii / ta0 >= 0.02)):
        return "Banks & financial services", "data: commission or material interest income, no revenue tag"
    lc = latest.get("loans_to_customers")
    if lc and latest.get("total_assets") and lc / latest["total_assets"] > 0.3:
        return "Banks & financial services", "data: loans to customers > 30% of assets"
    ta, ip = latest.get("total_assets"), latest.get("investment_property")
    if ta and ip and ip / ta > 0.4:
        return "Real estate", "data: investment property > 40% of assets"
    if registry and registry.get("nace"):
        s = nace_sector(registry["nace"])
        if s:
            return s, f"{registry['register']}: NACE {registry['nace']} {registry.get('nace_text') or ''}".strip()
    if re.search(r"\binvest(ment|ering|eringar)?\b", n):
        return "Investment companies", "name"
    if wd and wd.get("industries"):
        s = from_industries(wd["industries"])
        if s:
            return s, "wikidata: " + "; ".join(wd["industries"][:3])
    if any(k in n for k in ("bank", "sparebank", "sparbank", "pankki", "kredit", "kreditt", "försäkring", "forsikring", "vakuutus", "insurance")):
        return ("Insurance" if any(k in n for k in ("försäkring", "forsikring", "vakuutus", "insurance")) else "Banks & financial services"), "name"
    if any(k in n for k in ("fastighet", "eiendom", "ejendom", "kiinteistö", "property", "properties", "real estate",
                            "bostad", "bostäder", "bolig", "boliger")):
        return "Real estate", "name"
    if not has_rev and not has_ebit:
        return "Financial / other (no revenue or EBIT tag)", "data: no revenue or EBIT"
    return "Unclassified", "none"
