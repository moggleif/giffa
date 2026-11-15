"""Krav: K34 i KRAV.md, beslut 0012. Test: tests/test_ksmotet.py.

Vad en punkt på dagordningen rör: orterna i OMRADE.md och platserna i
platser.csv som punktens rubrik, förslag eller handling nämner, med det
som bara står i handlingen märkt, och de ärenden i bevakning/ som har ett
av punktens diarienummer. Ett nummer
utan förled, som kallelsen skriver det, är samma som ett med förled när
siffrorna är desamma; två nummer med förled måste vara lika.
"""

import re
from dataclasses import dataclass

from kommunhandlingar.diarienummer import normaliserat

from skanning.termer import monster
from webbplats.arende import Arende
from webbplats.kallelsen import Punkten

FORLED = re.compile(r"^[A-ZÅÄÖ]+-(?=\d)")


@dataclass(frozen=True)
class Traff:
    ort: str
    # Orten själv eller platsen som nämns.
    namn: str
    # Nämns bara i handlingen, inte i kallelsens rubrik eller förslag.
    i_handlingen: bool


@dataclass(frozen=True)
class Kopplad:
    punkten: Punkten
    traffar: list[Traff]
    egna: list[Arende]
    namnda: list[Arende]


def koppla(
    punkten: Punkten, orter: list[str], platser: list[dict[str, str]], arenden: list[Arende]
) -> Kopplad:
    return Kopplad(punkten, traffar(punkten, orter, platser), *foljda(punkten, arenden))


def traffar(punkten: Punkten, orter: list[str], platser: list[dict[str, str]]) -> list[Traff]:
    namnen = [(o, o) for o in orter] + [(p["ort"], p["namn"]) for p in platser]
    funna = [traff(punkten, ort, namn) for ort, namn in namnen]
    return sorted((t for t in funna if t), key=lambda t: t.i_handlingen)


def traff(punkten: Punkten, ort: str, namn: str) -> Traff | None:
    sok = monster(namn).search
    if sok(punkten.kallelsen):
        return Traff(ort, namn, False)
    return Traff(ort, namn, True) if sok(punkten.handlingen) else None


def foljda(punkten: Punkten, arenden: list[Arende]) -> tuple[list[Arende], list[Arende]]:
    egna = [a for a in arenden if har(a, punkten.numren[:1])]
    namnda = [a for a in arenden if a not in egna and har(a, punkten.numren[1:])]
    return egna, namnda


def har(arende: Arende, numren: tuple[str, ...]) -> bool:
    return any(samma(n, m) for n in numren for m in numren_i(arende))


def numren_i(arende: Arende) -> list[str]:
    falt = arende.falt.get("diarienummer", "")
    return [normaliserat(n.strip()) for n in falt.split(",") if n.strip()]


def samma(a: str, b: str) -> bool:
    if FORLED.match(a) and FORLED.match(b):
        return a == b
    return FORLED.sub("", a) == FORLED.sub("", b)
