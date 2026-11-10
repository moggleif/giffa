"""Krav: K6, K8 och K11 i KRAV.md. Test: tests/test_underlag.py.

Läser det sidan bygger på utöver ärendena: orterna ur OMRADE.md, platserna
ur platser.csv, källorna ur KALLOR.md och förra rundans period ur
bevakning/rundor.csv.
"""

import csv
from dataclasses import dataclass
from datetime import date
from io import StringIO


def orter(omrade: str) -> list[str]:
    fore_platser = omrade.split("\n## ", 1)[0]
    return [rad[2:].strip() for rad in fore_platser.splitlines() if rad.startswith("- ")]


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
