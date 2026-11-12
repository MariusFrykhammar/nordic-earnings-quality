"""Display names and manual lists.

Display name = legal name (GLEIF, else ESEF entity name) with legal-form words removed and
ALL-CAPS names title-cased. mapping/display_names.yaml overrides by LEI; mapping/exclude.yaml
removes companies from rankings (with a reason) when official data cannot.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

LEGAL_SUFFIX = re.compile(
    r"[\s,]*(\(publ\)|\bAktiebolag\b|\bAB\b|\bASA\b|\bAS\b|\bA/S\b|\bApS\b|\bOyj\b|\bAbp\b|\bOy\b|\bplc\b|\bPLC\b|"
    r"\bLimited\b|\bLtd\.?|\bInc\.?|\bS\.A\.|\bSA\b|\bSE\b|\bN\.V\.|\bNV\b|\bA\.S\.|\bASA\.)[\s,.]*$",
    re.I,
)
LEGAL_PREFIX = re.compile(r"^(Aktiebolaget|Aktiebolag|Telefonaktiebolaget|Investmentaktiebolaget)\s+", re.I)


def _yaml(path: str) -> dict:
    p = Path(path)
    return (yaml.safe_load(p.read_text()) or {}) if p.exists() else {}


_OVR: dict | None = None


def _smart_case(name: str) -> str:
    letters = [ch for ch in name if ch.isalpha()]
    if not letters or not all(ch.isupper() for ch in letters):
        return name
    out = []
    for w in name.split(" "):
        core = re.sub(r"[^A-Za-zÅÄÖÆØÜåäöæøü]", "", w)
        if len(core) <= 3:  # short words are usually acronyms: DSV, UPM, NKT, BW
            out.append(w)
        else:
            out.append("-".join(part if len(part) <= 3 else part[:1].upper() + part[1:].lower() for part in w.split("-")))
    return " ".join(out)


def display_name(lei: str, legal_name: str | None) -> str:
    global _OVR
    if _OVR is None:
        _OVR = _yaml("mapping/display_names.yaml")
    if lei in _OVR:
        return _OVR[lei]
    n = (legal_name or "").strip()
    for _ in range(3):
        n2 = LEGAL_SUFFIX.sub("", n).strip()
        if n2 == n:
            break
        n = n2
    n = LEGAL_PREFIX.sub("", n).strip() or (legal_name or "")
    return _smart_case(n)


def manual_exclusions() -> dict:
    return _yaml("mapping/exclude.yaml")
