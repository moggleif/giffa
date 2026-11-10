"""Krav: K6 och K8 i KRAV.md. Test: tests/test_underlag.py.

Läser det sidan bygger på utöver ärendena: orterna ur OMRADE.md, platserna
ur platser.csv, källorna ur KALLOR.md och förra rundans period ur
bevakning/rundor.csv.
"""

import csv
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


def senaste_runda(text: str) -> tuple[date, date]:
    sista = list(csv.DictReader(StringIO(text)))[-1]
    return date.fromisoformat(sista["fran"]), date.fromisoformat(sista["till"])
