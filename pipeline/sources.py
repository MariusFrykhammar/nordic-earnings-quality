"""Official reference sources used alongside the ESEF reports.

- GLEIF (Global LEI Foundation): legal name, legal form, national registration number. CC0.
- ESMA FIRDS (Financial Instruments Reference Data System): equity instruments admitted to trading
  in the EU/EEA, with issuer LEI and the most relevant trading venue. Used to tell equity-listed
  companies from bond-only issuers.
- National business registers for official industry (NACE) codes:
  Brønnøysundregistrene (Norway, open API), PRH / YTJ (Finland, open API, CC BY 4.0).
  Sweden (Bolagsverket) and Denmark (CVR) need free credentials; supported via env vars when set.
Every lookup is cached under .cache/ref/ and failures degrade gracefully (field left empty).
"""
from __future__ import annotations

import hashlib
import io
import json
import os
import re
import time
import zipfile
from datetime import date, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET



import requests

CACHE = Path(".cache/ref")
UA = {"User-Agent": "nordic-earnings-quality (github.com/MariusFrykhammar/nordic-earnings-quality)"}
S = requests.Session()
S.headers.update(UA)


def _get_json(url: str, ttl_days: float = 7, **kw) -> dict | None:
    p = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".json")
    if p.exists() and time.time() - p.stat().st_mtime < ttl_days * 86400:
        return json.loads(p.read_text())
    for attempt in range(5):
        try:
            r = S.get(url, timeout=60, **kw)
            if r.status_code == 404:
                data = None
            elif r.status_code == 429 or r.status_code >= 500:
                time.sleep(float(r.headers.get("Retry-After") or 0) or 5 * (attempt + 1))
                continue
            else:
                r.raise_for_status()
                data = r.json()
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(data))
            return data
        except (requests.RequestException, ValueError) as e:
            if attempt == 4:
                print(f"  ! {url[:90]}: {e}")
            time.sleep(2 * (attempt + 1))
    return None


# ------------------------------------------------------------------ GLEIF

def gleif(leis: list[str]) -> dict[str, dict]:
    out = {}
    for i in range(0, len(leis), 100):
        chunk = leis[i : i + 100]
        url = "https://api.gleif.org/api/v1/lei-records?filter[lei]=" + ",".join(chunk) + "&page[size]=100"
        doc = _get_json(url, ttl_days=7)
        for rec in (doc or {}).get("data", []):
            e = rec["attributes"]["entity"]
            out[rec["id"]] = {
                "legal_name": (e.get("legalName") or {}).get("name"),
                "legal_form_elf": (e.get("legalForm") or {}).get("id"),
                "registered_as": e.get("registeredAs"),
                "registration_authority": (e.get("registeredAt") or {}).get("id"),
                "jurisdiction": e.get("jurisdiction"),
                "entity_status": e.get("status"),
            }
        time.sleep(1.1)  # GLEIF allows 60 requests/minute
    return out


# ------------------------------------------------------------------ ESMA FIRDS

NORDIC_VENUES = {
    "XSTO": "Nasdaq Stockholm", "XHEL": "Nasdaq Helsinki", "XCSE": "Nasdaq Copenhagen", "XICE": "Nasdaq Iceland",
    "XOSL": "Oslo Børs", "XOAS": "Euronext Expand Oslo", "MERK": "Euronext Growth Oslo", "XNGM": "NGM Main Regulated",
    "SSME": "Nasdaq First North Sweden", "FNSE": "Nasdaq First North Sweden", "FNFI": "Nasdaq First North Finland",
    "DSME": "Nasdaq First North Denmark", "FNDK": "Nasdaq First North Denmark", "XSAT": "Spotlight Stock Market",
    "NMTF": "NGM Nordic SME", "FSME": "Nasdaq First North Finland",
}
REGULATED = {"XSTO", "XHEL", "XCSE", "XICE", "XOSL", "XOAS", "XNGM"}
_NS = "{urn:iso:std:iso:20022:tech:xsd:auth.017.001.02}"


def firds_equities(leis: set[str]) -> dict[str, dict]:
    """{lei: {'isins': [...], 'venue_mic': 'XSTO', 'venue': 'Nasdaq Stockholm', 'regulated': bool, 'name': ...}}"""
    files = None
    for back in (14, 30):
        start = (date.today() - timedelta(days=back)).isoformat()
        url = ("https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*"
               f"&fq=publication_date:%5B{start}T00:00:00Z%20TO%20{date.today().isoformat()}T23:59:59Z%5D&wt=json&rows=500")
        doc = _get_json(url, ttl_days=0.5)
        docs = [d for d in (doc or {}).get("response", {}).get("docs", []) if d.get("file_name", "").startswith("FULINS_E")]
        if docs:
            latest = max(d["file_name"].split("_")[2] for d in docs)
            files = sorted([d for d in docs if d["file_name"].split("_")[2] == latest], key=lambda d: d["file_name"])
            break
    if not files:
        raise RuntimeError("no FIRDS FULINS_E files found")
    out: dict[str, dict] = {}
    for f in files:
        z = S.get(f["download_link"], timeout=600).content
        zf = zipfile.ZipFile(io.BytesIO(z))
        with zf.open(zf.namelist()[0]) as fh:
            for _, el in ET.iterparse(fh, events=("end",)):
                if el.tag != _NS + "RefData":
                    continue
                issr = el.findtext(_NS + "Issr")
                if issr in leis:
                    g = el.find(_NS + "FinInstrmGnlAttrbts")
                    cfi = g.findtext(_NS + "ClssfctnTp") or ""
                    if cfi.startswith("E"):
                        isin = g.findtext(_NS + "Id")
                        rel = el.find(_NS + "TechAttrbts").findtext(_NS + "RlvntTradgVn")
                        rec = out.setdefault(issr, {"isins": [], "venues": [], "name": g.findtext(_NS + "FullNm")})
                        if isin not in rec["isins"]:
                            rec["isins"].append(isin)
                        if rel and rel not in rec["venues"]:
                            rec["venues"].append(rel)
                el.clear()
        print(f"  FIRDS {f['file_name']}: {len(out)} issuers so far")
    for rec in out.values():
        nordic = [v for v in rec["venues"] if v in NORDIC_VENUES]
        mic = (sorted(nordic, key=lambda v: (v not in REGULATED, v)) or rec["venues"] or [None])[0]
        rec["venue_mic"] = mic
        rec["venue"] = NORDIC_VENUES.get(mic, mic)
        rec["regulated_market"] = mic in REGULATED
    return out


# ------------------------------------------------------------------ national registers (NACE)

def brreg(orgnr: str) -> dict | None:
    d = _get_json(f"https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr}", ttl_days=30)
    if not d:
        return None
    nk = d.get("naeringskode1") or {}
    return {"nace": (nk.get("kode") or "").replace(".", ""), "nace_text": nk.get("beskrivelse"),
            "legal_form": (d.get("organisasjonsform") or {}).get("kode"), "register": "Brønnøysundregistrene"}


def prh(business_id: str) -> dict | None:
    d = _get_json(f"https://avoindata.prh.fi/opendata-ytj-api/v3/companies?businessId={business_id}", ttl_days=30)
    cs = (d or {}).get("companies") or []
    if not cs:
        return None
    mbl = cs[0].get("mainBusinessLine") or {}
    text = next((x["description"] for x in mbl.get("descriptions", []) if x.get("languageCode") == "3"), None)
    return {"nace": mbl.get("type") or "", "nace_text": text, "register": "PRH / YTJ"}


def registry_lookup(country: str, reg_no: str | None) -> dict | None:
    if not reg_no:
        return None
    reg = reg_no.replace(" ", "")
    try:
        if country == "NO" and reg.isdigit() and len(reg) == 9:
            return brreg(reg)
        if country == "FI" and len(reg) == 9 and reg[7] == "-":
            return prh(reg)
    except Exception as e:  # best effort
        print(f"  ! registry {country} {reg}: {e}")
    # SE (Bolagsverket) and DK (CVR) need credentials: BOLAGSVERKET_CLIENT_ID/SECRET, CVR_USER/CVR_PASSWORD
    if country == "SE" and os.environ.get("BOLAGSVERKET_CLIENT_ID"):
        return bolagsverket(reg)
    return None


_BV_TOKEN: dict = {}


def bolagsverket(orgnr: str) -> dict | None:
    """Bolagsverket 'värdefulla datamängder' API (free, OAuth client credentials). SNI codes come from SCB.

    Untested until credentials exist: the response is parsed defensively and failures leave the sector empty.
    """
    if "t" not in _BV_TOKEN or _BV_TOKEN["exp"] < time.time():
        r = S.post("https://portal.api.bolagsverket.se/oauth2/token", data={
            "grant_type": "client_credentials", "client_id": os.environ["BOLAGSVERKET_CLIENT_ID"],
            "client_secret": os.environ["BOLAGSVERKET_CLIENT_SECRET"], "scope": "vardefulla-datamangder:read"}, timeout=60)
        r.raise_for_status()
        j = r.json()
        _BV_TOKEN.update(t=j["access_token"], exp=time.time() + int(j.get("expires_in", 3000)) - 60)
    p = CACHE / f"bv_{orgnr}.json"
    if p.exists() and time.time() - p.stat().st_mtime < 30 * 86400:
        d = json.loads(p.read_text())
    else:
        r = S.post("https://gw.api.bolagsverket.se/vardefulla-datamangder/v1/organisationer",
                   json={"identitetsbeteckning": orgnr.replace("-", "")},
                   headers={"Authorization": "Bearer " + _BV_TOKEN["t"]}, timeout=60)
        if r.status_code != 200:
            return None
        d = r.json()
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(d))
    text = json.dumps(d)
    m = re.search(r'"(?:kod|code)"\s*:\s*"(\d{5})"', text)  # first 5-digit SNI code in the response
    return {"nace": m.group(1) if m else "", "nace_text": None, "register": "Bolagsverket (SNI from SCB)"} if m else None


# NACE division (2 digits) -> scanner sector. Holding/head-office codes are deliberately unmapped.
def nace_sector(code: str) -> str | None:
    c = (code or "").replace(".", "")
    if len(c) < 2 or not c[:2].isdigit():
        return None
    d = int(c[:2])
    if c.startswith(("642", "701")):  # holding companies / head offices say nothing about the business
        return None
    if c.startswith("411"):
        return "Real estate"  # development of building projects
    if c.startswith("325"):
        return "Health care"  # medical and dental instruments
    if c.startswith("582"):
        return "Technology"  # software publishing
    if c.startswith("643"):
        return "Investment companies"
    table = [
        ((1, 3), "Consumer"), ((5, 5), "Materials"), ((6, 6), "Energy"), ((7, 8), "Materials"), ((9, 9), "Energy"),
        ((10, 15), "Consumer"), ((16, 17), "Materials"), ((18, 18), "Industrials"), ((19, 19), "Energy"),
        ((20, 20), "Materials"), ((21, 21), "Health care"), ((22, 24), "Materials"), ((25, 25), "Industrials"),
        ((26, 26), "Technology"), ((27, 30), "Industrials"), ((31, 32), "Consumer"), ((33, 33), "Industrials"),
        ((35, 39), "Utilities"), ((41, 43), "Industrials"), ((45, 45), "Consumer"), ((46, 46), "Industrials"),
        ((47, 47), "Consumer"), ((49, 53), "Transport & shipping"), ((55, 56), "Consumer"),
        ((58, 61), "Telecom & media"), ((62, 63), "Technology"), ((64, 64), "Banks & financial services"),
        ((65, 65), "Insurance"), ((66, 66), "Banks & financial services"), ((68, 68), "Real estate"),
        ((69, 71), "Industrials"), ((72, 72), "Health care"), ((73, 73), "Telecom & media"), ((74, 82), "Industrials"),
        ((85, 85), "Consumer"), ((86, 88), "Health care"), ((90, 93), "Consumer"),
    ]
    for (lo, hi), s in table:
        if lo <= d <= hi:
            return s
    return None
