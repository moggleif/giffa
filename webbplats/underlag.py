"""Krav: K6, K8, K11 och K22 i KRAV.md. Test: tests/test_underlag.py.

Läser det sidan bygger på utöver ärendena: föreningarna och deras orter ur
OMRADE.md, platserna
ur platser.csv, källorna ur KALLOR.md och förra rundans period ur
bevakning/rundor.csv.
"""

import csv
from dataclasses import dataclass
from datetime import date
from io import StringIO


def foreningar(omrade: str) -> dict[str, list[str]]:
    fore_platser = omrade.split("\n## Platser", 1)[0]
    avsnitt = [del_.splitlines() for del_ in fore_platser.split("\n## ")[1:]]
    return {
        rader[0].strip(): [rad[2:].strip() for rad in rader if rad.startswith("- ")]
        for rader in avsnitt
    }


def orter(omrade: str) -> list[str]:
    return alla_orter(foreningar(omrade))


def alla_orter(foreningar: dict[str, list[str]]) -> list[str]:
    return [ort for lista in foreningar.values() for ort in lista]


def platser(text: str) -> list[dict[str, str]]:
    return list(csv.DictReader(StringIO(text)))


def kallor(text: str) -> list[list[str]]:
    rader = [rad for rad in text.splitlines() if rad.startswith("|")][2:]
    return [[cell.strip() for cell in rad.strip("|").split("|")] for rad in rader]


@dataclass(frozen=True)
class Runda:
    fran: date
    till: date
    anteckning: str


def senaste_runda(text: str) -> Runda:
    rundor = list(csv.DictReader(StringIO(text)))
    if not rundor:
        raise ValueError("bevakning/rundor.csv har ingen runda")
    sista = rundor[-1]
    fran, till = date.fromisoformat(sista["fran"]), date.fromisoformat(sista["till"])
    return Runda(fran, till, sista["anteckning"])
