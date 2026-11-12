"""Download filing lists and xBRL-JSON reports from filings.xbrl.org, with a disk cache."""
from __future__ import annotations

import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urlencode

import requests

BASE = "https://filings.xbrl.org"
CACHE = Path(".cache")
COUNTRIES = ["SE", "NO", "DK", "FI"]

_session = requests.Session()
_session.headers["User-Agent"] = "nordic-earnings-quality (github.com/MariusFrykhammar/nordic-earnings-quality)"


def _cache_path(url: str) -> Path:
    return CACHE / "http" / (hashlib.sha1(url.encode()).hexdigest() + ".json")


def get_json(url: str, use_cache: bool = True) -> dict | None:
    """GET a JSON document; cached on disk. Returns None on 404 / persistent failure."""
    p = _cache_path(url)
    if use_cache and p.exists():
        return json.loads(p.read_text())
    for attempt in range(4):
        try:
            r = _session.get(url, timeout=60)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            data = r.json()
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(json.dumps(data))
            return data
        except (requests.RequestException, ValueError) as e:
            if attempt == 3:
                print(f"  ! failed {url}: {e}")
                return None
            time.sleep(2 * (attempt + 1))
    return None


def list_filings(country: str, extra: dict | None = None, use_cache: bool = False) -> list[dict]:
    """All filings for a country (JSON:API, paginated). Returns flat dicts with entity info merged in."""
    params = {"filter[country]": country, "include": "entity", "page[size]": 200}
    params.update(extra or {})
    url = f"{BASE}/api/filings?{urlencode(params)}"
    out: list[dict] = []
    page = 0
    while url:
        page += 1
        doc = get_json(url, use_cache=use_cache)
        if not doc:
            break
        entities = {e["id"]: e.get("attributes", {}) for e in doc.get("included", []) if e.get("type") == "entity"}
        for f in doc.get("data", []):
            a = dict(f.get("attributes", {}))
            a["_id"] = f.get("id")
            rel = (f.get("relationships", {}).get("entity", {}) or {}).get("data") or {}
            ent = entities.get(rel.get("id"), {})
            a["_entity_id"] = rel.get("id")
            a["_lei"] = ent.get("identifier")
            a["_name"] = ent.get("name")
            out.append(a)
        nxt = (doc.get("links") or {}).get("next")
        url = (nxt if nxt.startswith("http") else BASE + nxt) if nxt else None
        if page > 200:
            break
    return out


def get_report(json_url: str) -> dict | None:
    if not json_url:
        return None
    url = json_url if json_url.startswith("http") else BASE + json_url
    return get_json(url)


def get_reports(json_urls: list[str], workers: int = 8) -> dict[str, dict | None]:
    with ThreadPoolExecutor(workers) as ex:
        return dict(zip(json_urls, ex.map(get_report, json_urls)))
