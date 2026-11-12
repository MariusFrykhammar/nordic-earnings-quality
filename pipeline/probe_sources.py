"""Probe additional official sources and write small samples to diagnostics/sources/."""
from __future__ import annotations

import io
import json
import zipfile
from pathlib import Path

import requests

OUT = Path("diagnostics/sources")
UA = {"User-Agent": "nordic-earnings-quality (github.com/MariusFrykhammar/nordic-earnings-quality)"}
LEIS = ["213800T8PC8Q4FYJZR07", "529900X41C0BSLK67H70", "5299001O0WJQYB5GYZ19"]  # Atlas Copco, DSV, Carlsberg


def save(name, obj):
    (OUT / name).write_text(json.dumps(obj, indent=1, ensure_ascii=False)[:200_000])


def tryget(name, url, **kw):
    try:
        r = requests.get(url, headers=UA, timeout=120, **kw)
        info = {"url": url, "status": r.status_code, "ctype": r.headers.get("content-type"), "len": len(r.content)}
        try:
            info["json"] = r.json()
        except ValueError:
            info["text"] = r.text[:3000]
        save(name, info)
        print(name, r.status_code, len(r.content))
        return r
    except Exception as e:
        save(name, {"url": url, "error": str(e)})
        print(name, "ERROR", e)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    tryget("gleif.json", "https://api.gleif.org/api/v1/lei-records?filter[lei]=" + ",".join(LEIS) + "&page[size]=10")
    tryget("gleif_isins.json", f"https://api.gleif.org/api/v1/lei-records/{LEIS[0]}/isins?page[size]=50")
    tryget("brreg_orkla.json", "https://data.brreg.no/enhetsregisteret/api/enheter/910747711")
    tryget("prh_kone.json", "https://avoindata.prh.fi/opendata-ytj-api/v3/companies?businessId=1927400-1")
    tryget("virk_offentliggoerelser.json",
           "http://distribution.virk.dk/offentliggoerelser/_search?q=cvrNummer:24256790&size=2")
    tryget("cvr_open.json", "http://distribution.virk.dk/cvr-permanent/virksomhed/_search?q=Vrvirksomhed.cvrNummer:24256790&size=1")
    tryget("scb_fr.json", "https://privateapi.scb.se/nv0101/v1/sokpavar/api/je/HamtaForetag")
    r = tryget("firds_files.json",
               "https://registers.esma.europa.eu/solr/esma_registers_firds_files/select?q=*&fq=publication_date:%5B2026-11-01T00:00:00Z%20TO%202026-11-12T23:59:59Z%5D&wt=json&rows=200")
    # download one equity full file and sample it
    try:
        docs = r.json()["response"]["docs"]
        fulins = sorted([d for d in docs if d.get("file_name", "").startswith("FULINS_E")], key=lambda d: d["file_name"])
        save("firds_fulins_e_list.json", fulins[:20])
        if fulins:
            z = requests.get(fulins[0]["download_link"], headers=UA, timeout=600).content
            zf = zipfile.ZipFile(io.BytesIO(z))
            name = zf.namelist()[0]
            with zf.open(name) as fh:
                head = fh.read(20000).decode("utf-8", "replace")
            save("firds_sample.json", {"zip_name": fulins[0]["file_name"], "xml_name": name, "zip_bytes": len(z), "head": head})
            print("firds sample ok", len(z))
    except Exception as e:
        save("firds_sample.json", {"error": str(e)})
        print("firds ERROR", e)
    # iXBRL viewer: check fact ids in xBRL-JSON
    try:
        rep = requests.get("https://filings.xbrl.org/213800T8PC8Q4FYJZR07/2025-12-31/ESEF/SE/1/atla-2025-12-31-1-en.json", headers=UA, timeout=120).json()
        ids = list(rep.get("facts", {}).keys())[:10]
        save("xbrljson_fact_ids.json", {"ids": ids})
    except Exception as e:
        save("xbrljson_fact_ids.json", {"error": str(e)})
