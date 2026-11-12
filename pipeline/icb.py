"""Industry Classification Benchmark (ICB, FTSE Russell): the classification Nordic exchanges use.

Two levels are used: 11 industries and 20 supersectors. Exchange data (Euronext) gives ICB directly; official
NACE codes from business registers and Wikidata industries are mapped onto the same supersectors.
"""
from __future__ import annotations

SUPERSECTORS: dict[str, str] = {
    "Technology": "Technology",
    "Telecommunications": "Telecommunications",
    "Health Care": "Health Care",
    "Banks": "Financials",
    "Financial Services": "Financials",
    "Insurance": "Financials",
    "Real Estate": "Real Estate",
    "Automobiles and Parts": "Consumer Discretionary",
    "Consumer Products and Services": "Consumer Discretionary",
    "Media": "Consumer Discretionary",
    "Retail": "Consumer Discretionary",
    "Travel and Leisure": "Consumer Discretionary",
    "Food, Beverage and Tobacco": "Consumer Staples",
    "Personal Care, Drug and Grocery Stores": "Consumer Staples",
    "Construction and Materials": "Industrials",
    "Industrial Goods and Services": "Industrials",
    "Basic Resources": "Basic Materials",
    "Chemicals": "Basic Materials",
    "Energy": "Energy",
    "Utilities": "Utilities",
}
FINANCIAL_SUPERSECTORS = {"Banks", "Financial Services", "Insurance"}

# ICB supersector codes (2019 structure) as published by exchanges, e.g. "4510, Food, Beverage and Tobacco"
CODE_TO_SUPERSECTOR = {
    "1010": "Technology", "1510": "Telecommunications", "2010": "Health Care", "3010": "Banks",
    "3020": "Financial Services", "3030": "Insurance", "3510": "Real Estate", "4010": "Automobiles and Parts",
    "4020": "Consumer Products and Services", "4030": "Media", "4040": "Retail", "4050": "Travel and Leisure",
    "4510": "Food, Beverage and Tobacco", "4520": "Personal Care, Drug and Grocery Stores",
    "5010": "Construction and Materials", "5020": "Industrial Goods and Services", "5510": "Basic Resources",
    "5520": "Chemicals", "6010": "Energy", "6510": "Utilities",
}


def nace_supersector(code: str) -> str | None:
    """Map a NACE / SNI / TOL / DB code (any of the national variants) to an ICB supersector."""
    c = "".join(ch for ch in (code or "") if ch.isdigit())
    if len(c) < 2:
        return None
    if c.startswith(("642", "701")):
        return None  # holding companies and head offices say nothing about the business
    pre = [
        ("411", "Real Estate"), ("325", "Health Care"), ("582", "Technology"), ("643", "Financial Services"),
        ("649", "Financial Services"), ("091", "Energy"), ("471", "Personal Care, Drug and Grocery Stores"),
        ("472", "Personal Care, Drug and Grocery Stores"), ("4773", "Personal Care, Drug and Grocery Stores"),
    ]
    for p, s in pre:
        if c.startswith(p):
            return s
    d = int(c[:2])
    table = [
        ((1, 3), "Food, Beverage and Tobacco"), ((5, 6), "Energy"), ((7, 9), "Basic Resources"),
        ((10, 12), "Food, Beverage and Tobacco"), ((13, 15), "Consumer Products and Services"),
        ((16, 17), "Basic Resources"), ((18, 18), "Industrial Goods and Services"), ((19, 19), "Energy"),
        ((20, 20), "Chemicals"), ((21, 21), "Health Care"), ((22, 22), "Industrial Goods and Services"),
        ((23, 23), "Construction and Materials"), ((24, 24), "Basic Resources"), ((25, 25), "Industrial Goods and Services"),
        ((26, 26), "Technology"), ((27, 28), "Industrial Goods and Services"), ((29, 29), "Automobiles and Parts"),
        ((30, 30), "Industrial Goods and Services"), ((31, 32), "Consumer Products and Services"),
        ((33, 33), "Industrial Goods and Services"), ((35, 39), "Utilities"), ((41, 43), "Construction and Materials"),
        ((45, 45), "Retail"), ((46, 46), "Industrial Goods and Services"), ((47, 47), "Retail"),
        ((49, 53), "Industrial Goods and Services"), ((55, 56), "Travel and Leisure"), ((58, 60), "Media"),
        ((61, 61), "Telecommunications"), ((62, 63), "Technology"), ((64, 64), "Banks"), ((65, 65), "Insurance"),
        ((66, 66), "Financial Services"), ((68, 68), "Real Estate"), ((69, 71), "Industrial Goods and Services"),
        ((72, 72), "Health Care"), ((73, 73), "Media"), ((74, 82), "Industrial Goods and Services"),
        ((85, 85), "Consumer Products and Services"), ((86, 88), "Health Care"), ((90, 93), "Travel and Leisure"),
        ((95, 96), "Consumer Products and Services"),
    ]
    for (lo, hi), s in table:
        if lo <= d <= hi:
            return s
    return None


# Wikidata industry labels -> supersector; checked in order, first keyword hit wins
KEYWORDS: list[tuple[str, list[str]]] = [
    ("Insurance", ["insurance", "reinsurance"]),
    ("Banks", ["bank"]),
    ("Financial Services", ["financial services", "asset management", "investment company", "private equity",
                            "venture capital", "payment", "stock exchange", "fintech", "credit", "investment"]),
    ("Real Estate", ["real estate", "property", "properties"]),
    ("Health Care", ["pharmaceutical", "health", "medical", "biotech", "life science", "drug", "diagnostic", "dental", "hospital"]),
    ("Telecommunications", ["telecommunication"]),
    ("Technology", ["software", "information technology", "computer", "internet", "semiconductor", "electronic", "it service",
                    "technology", "cybersecurity", "artificial intelligence"]),
    ("Media", ["media", "broadcast", "publishing", "entertainment", "advertising", "video game"]),
    ("Utilities", ["utility", "electricity", "electric power", "power generation", "district heating", "renewable energy",
                   "wind power", "hydropower", "waste management"]),
    ("Energy", ["petroleum", "oil", "natural gas", "energy", "offshore", "drilling"]),
    ("Basic Resources", ["mining", "steel", "paper", "forest", "metal", "pulp", "aluminium", "timber"]),
    ("Chemicals", ["chemical"]),
    ("Construction and Materials", ["construction", "building material", "cement", "building"]),
    ("Automobiles and Parts", ["automotive", "car manufactur", "vehicle"]),
    ("Food, Beverage and Tobacco", ["food", "beverage", "brewery", "tobacco", "seafood", "aquaculture", "fishing", "salmon", "agricultur"]),
    ("Personal Care, Drug and Grocery Stores", ["grocery", "supermarket", "pharmacy", "cosmetic", "personal care"]),
    ("Retail", ["retail", "e-commerce", "fashion", "clothing"]),
    ("Travel and Leisure", ["hotel", "restaurant", "gambling", "gaming", "betting", "travel", "airline", "cruise"]),
    ("Consumer Products and Services", ["consumer", "furniture", "toy", "home appliance", "education"]),
    ("Industrial Goods and Services", ["shipping", "transport", "logistics", "freight", "engineering", "machinery",
                                       "manufactur", "industr", "aerospace", "defence", "defense", "conglomerate",
                                       "equipment", "tool", "security", "consulting", "staffing", "services", "packaging"]),
]


def from_wikidata(industries: list[str]) -> str | None:
    text = " | ".join(industries).lower()
    for ss, kws in KEYWORDS:
        if any(k in text for k in kws):
            return ss
    return None
