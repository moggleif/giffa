"""Krav: K26 i KRAV.md. Test: tests/test_handlingslankar.py.

Läser ett dokument i kommunhandlingar som sidor och hittar paragrafen,
diarienumret och rubriken på en sida i ett protokoll.
"""

import re
from typing import NamedTuple

SIDA = re.compile(r"^<!-- sida (\d+) -->$", re.M)
RUBRIK = re.compile(r"§\s*(\d+)\s+(?:Dnr\s*)?((?:[A-ZÅÄÖ]{1,5}[ -]?)?\d{4}[-/]\d{4,6})")
SLUT = re.compile(r"\b(?:Beslut|Förslag till beslut|Sammanfattning)\b")


class Paragraf(NamedTuple):
    nummer: str
    diarienummer: str
    rubrik: str


def sidor(text: str) -> dict[int, str]:
    delar = SIDA.split(text)
    return {int(nr): innehall for nr, innehall in zip(delar[1::2], delar[2::2])}


def kod(text: str) -> str:
    return re.sub(r"[^0-9A-ZÅÄÖ]", "", text.upper())


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
