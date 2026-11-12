"""Full Day-1 pipeline: list -> deduplicate -> extract -> map -> metrics -> flags -> validate -> write."""
from __future__ import annotations

import json
import re
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
from pathlib import Path

from . import extract, fetch, flags, fx, mapping, metrics, names, sectors, sources, validate

YEARS = list(range(2020, 2026))
FIRST_YEAR_KEPT = 2019  # base year for 2020 growth (from FY2020 comparatives)
CORE = ["revenue", "ebit", "net_profit", "ocf"]
REPORT_METRICS = [
    "revenue", "ebit", "net_profit", "ocf", "total_assets", "equity", "cash", "borrowings", "receivables",
    "inventories", "goodwill_measure", "capex", "capex_intangible", "da",
]
MIN_REVENUE_EUR_M = 25  # rankings only include companies at least this size (latest year)
# Danish ApS and Norwegian AS (not ASA) are private company forms; HoldCo/BidCo/TopCo are financing vehicles.
PRIVATE_FORM = re.compile(r"\bApS\b|\sAS$|\bA\.S\.$|holdco|bidco|topco|midco", re.I)
RAW_PROBE = ["axfood", "lindab", "clas ohlson", "ncc aktiebolag", "flsmidth"]
IFRS_CAND = re.compile(r"Revenue|Sales|Income|Operating|ProfitLoss|CashFlows", re.I)
DATA = Path("data")
CAND = re.compile(r"revenue|sales|turnover|omsättning|omsattning|inntekt|omsætning|liikevaihto|operat|rörelse|drift|liike|ebit|"
                  r"profit|result|cashflow|kassaflöde|kontantstr", re.I)
DIAG = Path("diagnostics")
SPOTCHECK = {
    "SE": ["atlas copco", "sandvik", "electrolux"],
    "NO": ["orkla", "kongsberg gruppen", "telenor"],
    "DK": ["carlsberg a/s", "dsv a/s", "novo nordisk a/s"],
    "FI": ["kone", "upm", "wärtsilä"],
}


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


def rnd(x, n=4):
    return None if x is None else round(x, n)


# ------------------------------------------------------------------ 1. list + dedupe

def list_all() -> tuple[list[dict], dict]:
    stats = {}
    keep: dict[tuple, dict] = {}
    for c in fetch.COUNTRIES:
        fl = fetch.list_filings(c)
        n_in_range = 0
        for f in fl:
            pe = f.get("period_end") or ""
            if not f.get("json_url") or not f.get("_lei") or not pe:
                continue
            if not ("2020-01-01" <= pe <= "2025-12-31"):
                continue
            n_in_range += 1
            k = (f["_lei"], pe)
            # keep one per company and period: latest processed wins
            if k not in keep or (f.get("processed") or "") > (keep[k].get("processed") or ""):
                keep[k] = f
        stats[c] = {"filings_listed": len(fl), "filings_fy2020_2025": n_in_range}
        log(c, stats[c])
    filings = list(keep.values())
    for c in fetch.COUNTRIES:
        stats[c]["after_dedup"] = sum(1 for f in filings if f.get("country") == c)
    return filings, stats


# ------------------------------------------------------------------ 2. per company series

def company_years(filings: list[dict], facts_by_url: dict[str, list]) -> dict:
    """Assemble {boundary: {'D': {concept: v}, 'I': {...}, 'cur': unit, 'src': filing, 'own': bool}}.

    Own-year facts win; gaps are filled from the nearest later report's comparatives.
    """
    filings = sorted(filings, key=lambda f: f["period_end"])
    years: dict[date, dict] = {}
    restated: list[dict] = []
    per_filing = []
    for f in filings:
        facts = facts_by_url.get(f["json_url"]) or []
        if not facts:
            continue
        units = Counter(x[2] for x in facts)
        cur = units.most_common(1)[0][0]
        own_b = date.fromisoformat(f["period_end"]) + timedelta(days=1)
        parsed = []
        for c, p, u, v, fid in facts:
            if u != cur:
                continue
            pp = extract.parse_period(p)
            if not pp:
                continue
            kind, s, b = pp
            if kind == "D" and not extract.annual(s, b):
                continue
            parsed.append((kind, b, c, v, fid))
        per_filing.append((f, cur, own_b, parsed))

    def slot(b, cur, f, own):
        y = years.setdefault(b, {"D": {}, "I": {}, "ids": {}, "cur": cur, "src": f, "own": own})
        return y

    # pass 1: own-year facts
    for f, cur, own_b, parsed in per_filing:
        for kind, b, c, v, fid in parsed:
            if b == own_b:
                y = slot(b, cur, f, True)
                y["own"], y["src"], y["cur"] = True, f, cur
                y[kind][c] = v
                y["ids"][(kind, c)] = (fid, f)
    # pass 2: comparatives, nearest later report first
    for f, cur, own_b, parsed in per_filing:
        for kind, b, c, v, fid in parsed:
            if b == own_b:
                continue
            y = slot(b, cur, f, False)
            if y["cur"] != cur:
                continue
            if c not in y[kind]:
                y[kind][c] = v
                y["ids"][(kind, c)] = (fid, f)
            elif c == "ifrs-full:Revenue" and kind == "D" and y["own"] and v and abs(y[kind][c] / v - 1) > 0.02:
                restated.append({"fy_end": str(b - timedelta(days=1)), "own": y[kind][c], "later_comparative": v})
    return {"years": years, "restated": restated}


def icb_industry(ss: str) -> str | None:
    from .icb import SUPERSECTORS
    return SUPERSECTORS.get(ss)


def fact_concept(prov: str) -> str | None:
    """Full concept name behind a provenance string; None for sums."""
    if "+" in prov:
        return None
    for pre in ("override:", "extension-auto:"):
        if prov.startswith(pre):
            return prov[len(pre):]
    for pre in ("specific-line:", "fallback:"):
        if prov.startswith(pre):
            return mapping.I + prov[len(pre):]
    return mapping.I + prov


# ------------------------------------------------------------------ 3. build

def main() -> None:
    DATA.mkdir(exist_ok=True)
    (DATA / "company").mkdir(exist_ok=True)
    DIAG.mkdir(exist_ok=True)

    filings, list_stats = list_all()
    log("unique filings to process:", len(filings))

    urls = sorted({f["json_url"] for f in filings})
    facts_by_url: dict[str, list] = {}
    t0 = time.time()
    with ThreadPoolExecutor(8) as ex:
        for i, (u, fs) in enumerate(zip(urls, ex.map(extract.get_facts, urls))):
            facts_by_url[u] = fs
            if i % 250 == 0:
                log(f"  facts {i}/{len(urls)} ({time.time() - t0:.0f}s)")
    failed = [u for u, fs in facts_by_url.items() if fs is None]
    log("downloads failed:", len(failed))

    by_lei: dict[str, list[dict]] = defaultdict(list)
    for f in filings:
        by_lei[f["_lei"]].append(f)

    try:
        rates = fx.load()
        log("ECB rates loaded:", sorted(rates["avg"]))
    except Exception as e:
        log("! ECB rates failed:", e)
        rates = {"avg": {}, "end": {}}

    log("wikidata lookup for", len(by_lei), "LEIs")
    wd = sectors.wikidata(sorted(by_lei))
    log("wikidata hits:", len(wd))

    companies = {}
    mapping_prov = defaultdict(Counter)  # metric -> concept -> n company-years
    ext_auto = []
    validation = defaultdict(list)
    restatements = 0

    for lei, fl in by_lei.items():
        latest_f = max(fl, key=lambda f: f["period_end"])
        name, country = latest_f.get("_name"), latest_f.get("country")
        assembled = company_years(fl, facts_by_url)
        restatements += len(assembled["restated"])
        series: dict[int, dict] = {}
        for b, y in sorted(assembled["years"].items()):
            fy_end = b - timedelta(days=1)
            label = fy_end.year
            if label < FIRST_YEAR_KEPT or label > 2025:
                continue
            vals, prov = mapping.map_year(lei, y["D"], y["I"])
            if not vals:
                continue
            if label in series and len(series[label]["raw"]) >= len(vals):
                continue  # keep the richer of two boundaries in the same label year
            cur = y["cur"].split(":")[1]
            v = {k: x / 1e6 for k, x in vals.items()}  # millions, reporting currency
            v.update(metrics.derived(v))
            src = y["src"]
            refs = {}
            for metric, pv in prov.items():
                concept = fact_concept(pv)
                hit = y["ids"].get((mapping.CONCEPTS[metric][0], concept)) if concept else None
                if hit and hit[1].get("viewer_url"):
                    refs[metric] = (fetch.BASE + hit[1]["viewer_url"], hit[0])
            series[label] = {
                "refs": refs,
                "raw": vals, "prov": prov,
                "ifrs_d": sorted(k.split(":", 1)[1] for k in y["D"] if k.startswith("ifrs-full:")),
                "ext": sorted({k.split(":", 1)[1] for k in list(y["D"]) + list(y["I"]) if not k.startswith("ifrs-full:")}), "v": v, "fy_end": str(fy_end), "currency": cur,
                "own_report": y["own"], "source": fetch.BASE + (src.get("viewer_url") or ""),
                "source_period_end": src.get("period_end"),
                "fx_avg": fx.rate(rates, cur, fy_end, "avg"), "fx_end": fx.rate(rates, cur, fy_end, "end"),
            }
        if not series:
            continue
        years_sorted = sorted(series)
        for t in years_sorted:
            prev = series.get(t - 1)
            if prev and prev["currency"] != series[t]["currency"]:
                prev = None
            series[t]["m"] = metrics.year_metrics(series[t]["v"], prev["v"] if prev else None)
        for t in years_sorted:
            series[t]["m"]["cash_conversion_3y"] = flags.cash_conversion_3y(series, t)
            for k, c in series[t]["prov"].items():
                mapping_prov[k][c.split(":")[0] + ":" if c.startswith("extension-auto") else c] += 1
                if c.startswith("extension-auto") and t >= 2020:
                    ext_auto.append({"lei": lei, "name": name, "country": country, "year": t, "metric": k, "concept": c.split(":", 1)[1]})
            for iss in validate.check_year(series[t]["v"], series[t]["m"]):
                if t >= 2020:
                    validation[iss].append({"lei": lei, "name": name, "year": t})
        latest_t = max(t for t in years_sorted)
        companies[lei] = {
            "lei": lei, "name": name, "country": country,
            "wikidata": (wd.get(lei) or {}).get("wikidata"), "exchanges": (wd.get(lei) or {}).get("exchanges", []),
            "tickers": (wd.get(lei) or {}).get("tickers", []),
            "series": series, "latest_year": latest_t,
        }
    log("companies assembled:", len(companies))

    # ---------------- official reference data: GLEIF, ESMA FIRDS, national registers
    ref_status = {}
    try:
        gl = sources.gleif(sorted(companies))
        ref_status["gleif"] = f"ok: {len(gl)} of {len(companies)} LEIs"
    except Exception as e:
        gl, ref_status["gleif"] = {}, f"failed: {e}"
    try:
        fr = sources.firds_equities(set(companies))
        ref_status["firds"] = f"ok: {len(fr)} issuers with listed equity"
    except Exception as e:
        fr, ref_status["firds"] = None, f"failed: {e}"
    n_reg = 0
    for lei, c in companies.items():
        g = gl.get(lei, {})
        c.update(legal_name=g.get("legal_name"), legal_form_elf=g.get("legal_form_elf"),
                 org_number=g.get("registered_as"), jurisdiction=g.get("jurisdiction"))
        c["display_name"] = names.display_name(lei, g.get("legal_name") or c["name"])
        reg = sources.registry_lookup(g.get("jurisdiction") or c["country"], g.get("registered_as"))
        if reg:
            n_reg += 1
        c["registry"] = reg
        eq = (fr or {}).get(lei)
        c["equity"] = eq
        exch = None
        if eq and eq.get("venue_mic") and sources.NORDIC_OPERATING_OSLO(eq):
            exch = sources.euronext_icb(eq["isins"], ["XOSL", "XOAS", "MERK"])
        c["icb_exchange"] = exch
        industry, supersector, basis = sectors.classify(c["name"], wd.get(lei), c["series"][c["latest_year"]]["v"], reg, exch)
        c["sector"], c["supersector"], c["sector_basis"] = industry, supersector, basis
    ref_status["registries"] = f"ok: industry codes for {n_reg} companies (NO, FI; SE/DK need credentials)"
    log("reference data:", ref_status)

    # ---------------- universe + peers
    def in_universe(c):
        return c["sector"] not in sectors.FINANCIAL_INDUSTRIES

    def size_eur(c):
        s = c["series"][c["latest_year"]]
        rev, r = s["v"].get("revenue"), s.get("fx_avg")
        return rev / r if rev is not None and r else None

    excluded = names.manual_exclusions()

    def listing_status(c):
        if fr is not None:  # ESMA FIRDS available: authoritative
            eq = c["equity"]
            if eq and eq.get("home_market"):
                return "listed shares: " + (eq["venue"] or eq["venue_mic"])
            if eq and c["latest_year"] >= 2025:
                # shares on EU venues and a current annual report: listed, home venue not in FIRDS data
                return "listed shares: home venue not identified (ESMA FIRDS)"
            if eq:
                return "shares traded only outside Nordic exchanges (ESMA FIRDS)"
            return "no listed shares (ESMA FIRDS)"
        if c["exchanges"]:
            return "listed shares (Wikidata)"
        if PRIVATE_FORM.search(c["name"] or ""):
            return "no listed shares (private legal form)"
        return "unknown"

    def rankable(c):
        se = size_eur(c)
        return (in_universe(c) and c["latest_year"] >= 2024 and se is not None and se >= MIN_REVENUE_EUR_M
                and c["listing_status"].startswith(("listed shares", "unknown")) and c["lei"] not in excluded)

    for c in companies.values():
        c["listing_status"] = listing_status(c)

    peer_pool = [c for c in companies.values() if rankable(c) and c["sector"] != "Real Estate"]
    peer_keys = ["cash_conversion_3y", "accruals_ratio", "intangible_capex_to_revenue"]

    def thresholds(group):
        lat = [c["series"][c["latest_year"]]["m"] for c in group]
        return {
            "cash_conversion_3y_p10": flags.percentile([m.get("cash_conversion_3y") for m in lat], 10),
            "accruals_ratio_p90": flags.percentile([m.get("accruals_ratio") for m in lat], 90),
            "intangible_capex_to_revenue_p90": flags.percentile([m.get("intangible_capex_to_revenue") for m in lat], 90),
            "n": len(group),
        }

    all_thr = thresholds(peer_pool)
    by_ss, by_ind = defaultdict(list), defaultdict(list)
    for c in peer_pool:
        by_ss[c["supersector"]].append(c)
        by_ind[c["sector"]].append(c)
    sector_thr = {}
    for ss in {c["supersector"] for c in companies.values()}:
        ind = icb_industry(ss)
        if ss != "Unclassified" and len(by_ss.get(ss, [])) >= 10:
            g, label = by_ss[ss], ss
        elif ind and ind != "Unclassified" and len(by_ind.get(ind, [])) >= 10:
            g, label = by_ind[ind], ind
        else:
            g, label = None, "all non-financial companies"
        th = thresholds(g) if g else {}
        sector_thr[ss] = {k: (th.get(k) if th.get(k) is not None else all_thr.get(k)) for k in all_thr}
        sector_thr[ss]["peer_group"] = label
        sector_thr[ss]["n"] = len(g) if g else all_thr["n"]

    for c in companies.values():
        c["in_universe"] = in_universe(c)
        c["rankable"] = rankable(c)
        c["revenue_eur_m"] = rnd(size_eur(c), 1)
        if not c["in_universe"]:
            c["flags"] = []
            continue
        thr = sector_thr.get(c["supersector"]) or dict(all_thr, peer_group="all non-financial companies")
        c["peer_group"] = thr.get("peer_group", "all non-financial")
        c["flags"] = flags.evaluate(c["series"], c["latest_year"], c["sector"], thr)

    # ---------------- outputs
    write_outputs(companies, list_stats, mapping_prov, ext_auto, validation, restatements, failed, all_thr, sector_thr, ref_status)
    log("done")


# ------------------------------------------------------------------ 4. outputs

def _clean(d: dict, n=4):
    return {k: (rnd(v, n) if isinstance(v, float) else v) for k, v in d.items() if v is not None}


def write_outputs(companies, list_stats, mapping_prov, ext_auto, validation, restatements, failed, all_thr, sector_thr, ref_status):
    index = []
    for c in companies.values():
        lat = c["series"][c["latest_year"]]
        index.append({
            "lei": c["lei"], "name": c["display_name"], "legal_name": c["legal_name"] or c["name"],
            "country": c["country"], "sector": c["sector"], "supersector": c["supersector"], "market": (c["equity"] or {}).get("venue"),
            "currency": lat["currency"], "latest_year": c["latest_year"], "in_universe": c["in_universe"],
            "listing_status": c["listing_status"],
            "rankable": c["rankable"], "revenue_eur_m": c["revenue_eur_m"],
            "n_flags": len(c["flags"]), "flags": [f["flag"] for f in c["flags"]],
            "profit_cash_gap": rnd(lat["m"].get("profit_cash_gap")),
            "profit_cash_gap_scaled": rnd(lat["m"].get("profit_cash_gap_scaled")),
            "net_profit_growth": rnd(lat["m"].get("net_profit_growth")), "ocf_growth": rnd(lat["m"].get("ocf_growth")),
            "receivables_growth": rnd(lat["m"].get("receivables_growth")), "revenue_growth": rnd(lat["m"].get("revenue_growth")),
            "ebit_margin": rnd(lat["m"].get("ebit_margin")), "cash_conversion_3y": rnd(lat["m"].get("cash_conversion_3y")),
        })
        detail = {
            k: c[k] for k in ("lei", "display_name", "legal_name", "country", "sector", "supersector", "icb_exchange", "sector_basis", "org_number",
                              "legal_form_elf", "registry", "equity", "tickers", "wikidata", "exchanges", "latest_year",
                              "in_universe", "rankable", "listing_status", "revenue_eur_m", "flags")
        }
        detail["esef_entity_name"] = c["name"]
        detail["peer_group"] = c.get("peer_group")
        # report viewers referenced by this company's figures; refs point into this list
        reports = sorted({u for s in c["series"].values() for u, _ in s["refs"].values()} | {s["source"] for s in c["series"].values()})
        detail["reports"] = reports
        ridx = {u: i for i, u in enumerate(reports)}
        detail["years"] = {
            str(t): {
                "fy_end": s["fy_end"], "currency": s["currency"], "own_report": s["own_report"], "report": ridx[s["source"]],
                "refs": {m: [ridx[u], fid] for m, (u, fid) in s["refs"].items()},
                "fx_eur_avg": rnd(s["fx_avg"], 6), "fx_eur_end": rnd(s["fx_end"], 6),
                "values": _clean({k: x for k, x in s["v"].items() if not isinstance(x, str)}, 3),
                "bases": {k: x for k, x in s["v"].items() if isinstance(x, str)},
                "metrics": _clean(s["m"]), "concepts": s["prov"],
            }
            for t, s in sorted(c["series"].items())
        }
        for f in detail["flags"]:
            f["evidence"] = _clean(f["evidence"]) if isinstance(f["evidence"], dict) else f["evidence"]
        (DATA / "company" / f"{c['lei']}.json").write_text(json.dumps(detail, ensure_ascii=False, separators=(",", ":")))
    index.sort(key=lambda r: (r["country"] or "", r["name"] or ""))
    (DATA / "companies.json").write_text(json.dumps(index, ensure_ascii=False, separators=(",", ":")))

    ranked = [r for r in index if r["rankable"]]
    lists = {
        "most_flags": sorted([r for r in ranked if r["n_flags"]], key=lambda r: (-r["n_flags"], -(r["profit_cash_gap_scaled"] or -9)))[:50],
        # profit up, cash flow down; ranked by (change in net profit - change in OCF) / prior-year revenue,
        # which avoids the base effects of growth rates on small numbers
        "widest_profit_cash_gap": sorted(
            [r for r in ranked if r["profit_cash_gap_scaled"] is not None and r["sector"] != "Real Estate"
             and (r["net_profit_growth"] or 0) > 0 and (r["ocf_growth"] or 0) < 0],
            key=lambda r: -r["profit_cash_gap_scaled"])[:50],
        "fastest_receivables_build_up": sorted(
            [r for r in ranked if r["receivables_growth"] is not None and r["revenue_growth"] is not None
             and r["sector"] != "Real Estate"],
            key=lambda r: -(r["receivables_growth"] - r["revenue_growth"]))[:50],
    }
    meta = {
        "generated": time.strftime("%Y-%m-%d"), "source": "Company annual reports (ESEF) via filings.xbrl.org",
        "reference_sources": {
            "GLEIF": "legal names, legal form, registration numbers (CC0)",
            "ESMA FIRDS": "shares admitted to trading and primary venue",
            "Brønnøysundregistrene / PRH": "official industry codes (NACE), Norway and Finland",
            "ECB": "euro reference exchange rates", "Wikidata": "industry where no registry code (CC0)",
        },
        "reference_status": ref_status,
        "min_revenue_eur_m_for_rankings": MIN_REVENUE_EUR_M, "rules": flags.RULES,
        "sector_exclusions": {k: sorted(v) for k, v in flags.EXCLUDE_BY_SECTOR.items()},
        "peer_thresholds": {"all": all_thr, **{k: v for k, v in sector_thr.items()}},
    }
    (DATA / "flags.json").write_text(json.dumps({"meta": meta, "lists": lists}, ensure_ascii=False, indent=1))

    # ---------------- diagnostics
    cov = {}
    for ctry in fetch.COUNTRIES:
        cs = [c for c in companies.values() if c["country"] == ctry]
        uni = [c for c in cs if c["in_universe"]]
        per_metric = {}
        for mtr in REPORT_METRICS:
            per_metric[mtr] = {str(y): sum(1 for c in uni if c["series"].get(y, {}).get("v", {}).get(mtr) is not None) for y in YEARS}
        gate = sum(
            1 for c in uni
            if sum(1 for y in YEARS if all(c["series"].get(y, {}).get("v", {}).get(k) is not None for k in CORE)) >= 3
        )
        cov[ctry] = {
            **list_stats.get(ctry, {}), "companies": len(cs), "non_financial": len(uni),
            "excluded_financial_or_untagged": len(cs) - len(uni),
            "gate_core4_3yrs": gate, "rankable": sum(1 for c in uni if c["rankable"]),
            "sectors": Counter(c["sector"] for c in cs).most_common(),
            "supersectors": Counter(c["supersector"] for c in uni).most_common(),
            "sector_source": Counter((c["sector_basis"] or "").split(":")[0] for c in uni).most_common(),
            "listing": Counter(c["listing_status"].split(":")[0] for c in uni).most_common(),
            "venues": Counter((c["equity"] or {}).get("venue") for c in uni if c["equity"]).most_common(),
            "company_years_by_metric": per_metric,
        }
    cov["total_gate_core4_3yrs"] = sum(cov[c]["gate_core4_3yrs"] for c in fetch.COUNTRIES)
    cov["downloads_failed"] = len(failed)
    cov["reference_status"] = ref_status
    cov["fact_level_links"] = sum(len(s["refs"]) for c in companies.values() for s in c["series"].values())
    cov["revenue_restatements_over_2pct"] = restatements
    (DIAG / "coverage.json").write_text(json.dumps(cov, ensure_ascii=False, indent=1))

    (DIAG / "mapping_usage.json").write_text(json.dumps(
        {k: v.most_common() for k, v in sorted(mapping_prov.items())}, ensure_ascii=False, indent=1))

    # companies needing overrides: in universe, latest year >= 2024, missing a core metric
    needs = []
    for c in companies.values():
        if not c["in_universe"] or c["latest_year"] < 2024:
            continue
        s = c["series"][c["latest_year"]]
        missing = [k for k in CORE if s["v"].get(k) is None]
        if missing:
            needs.append({"lei": c["lei"], "name": c["name"], "country": c["country"], "sector": c["sector"],
                          "year": c["latest_year"], "missing": missing,
                          "candidate_extension_concepts": [e for e in s["ext"] if CAND.search(e)][:15],
                          "ifrs_duration_concepts": [e for e in s["ifrs_d"] if IFRS_CAND.search(e)][:25],
                          "source": s["source"]})
    (DIAG / "needs_override.json").write_text(json.dumps(needs, ensure_ascii=False, indent=1))
    (DIAG / "extension_auto_matches.json").write_text(json.dumps(ext_auto, ensure_ascii=False, indent=1))
    (DIAG / "validation.json").write_text(json.dumps(
        {k: {"count": len(v), "examples": v[:25]} for k, v in sorted(validation.items())}, ensure_ascii=False, indent=1))

    spot = {}
    for ctry, names in SPOTCHECK.items():
        for nm in names:
            hits = [c for c in companies.values() if c["country"] == ctry and (c["name"] or "").lower().startswith(nm)]
            hits.sort(key=lambda c: -(c["revenue_eur_m"] or 0))
            if not hits:
                spot[nm] = "not found"
                continue
            c = hits[0]
            spot[nm] = {
                "name": c["name"], "lei": c["lei"], "sector": c["sector"],
                "years": {str(t): {"currency": s["currency"], **{k: rnd(s["v"].get(k), 1) for k in CORE + ["total_assets", "equity"]},
                                   "concepts": {k: s["prov"].get(k) for k in CORE}}
                          for t, s in sorted(c["series"].items()) if t >= 2023},
            }
    (DIAG / "spotcheck.json").write_text(json.dumps(spot, ensure_ascii=False, indent=1))
