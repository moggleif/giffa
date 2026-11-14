"""Krav: K26 i KRAV.md. Test: tests/test_handlingslankar.py.

Hittar paragrafen, diarienumret och rubriken på en sida i ett protokoll,
och läser huvudet överst på en sida i handlingarna.
"""

import re
from typing import NamedTuple

from skanning.sok import sidor

RUBRIK = re.compile(r"§\s*(\d+)\s+(?:Dnr\s*)?((?:[A-ZÅÄÖ]{1,5}[ -]?)?\d{4}[-/]\d{4,6})")
SLUT = re.compile(r"\b(?:Beslut|Förslag till beslut|Sammanfattning)\b")
# Löpnumret får inte vara ett årtal, så att ett årsspann som 2024–2025 inte
# läses som ett diarienummer.
DIARIENUMMER = re.compile(r"\b(?:[A-ZÅÄÖ]{1,5}[ -]?)?20\d\d[-–](?!(?:19|20)\d\d\b)\d{3,6}\b")
# Huvudet på en tjänsteskrivelse – rubrik, datum, diarienummer och ärendets
# rubrik – ryms i de första raderna med text på sidan.
HUVUDETS_RADER = 12


class Paragraf(NamedTuple):
    nummer: str
    diarienummer: str
    rubrik: str


def siffror(diarienummer: str) -> str:
    """År och löpnummer utan inledande nollor: KS 2023-492 och KS-2023-00492 är samma."""
    ar, lopnummer = re.findall(r"\d+", diarienummer)[-2:]
    return f"{ar}-{int(lopnummer)}"


def paragraf(protokoll: dict[int, str], sida: int) -> Paragraf | None:
    for nr, sista in ((sida, False), (sida - 1, True)):
        funna = list(RUBRIK.finditer(protokoll.get(nr, "")))
        if funna:
            traff = funna[-1] if sista else funna[0]
            return Paragraf(traff[1], traff[2], rubrik(protokoll[nr][traff.end():]))
    return None


def rubrik(text: str) -> str:
    rader = " ".join(rad.strip() for rad in text.strip().splitlines()[:3])
    return SLUT.split(rader)[0].strip()


def huvud(text: str) -> str:
    return "\n".join([rad for rad in text.splitlines() if rad.strip()][:HUVUDETS_RADER])


def som_ordbok(text: str) -> dict[int, str]:
    return dict(sidor(text))
