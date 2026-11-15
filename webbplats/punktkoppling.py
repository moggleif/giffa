"""Krav: K34 i KRAV.md, beslut 0012. Test: tests/test_ksmotet.py.

Vad en punkt på dagordningen rör: orterna i OMRADE.md som punktens rubrik,
förslag eller handling nämner, själva eller genom en plats i platser.csv, med det
som bara står i handlingen märkt, och de ärenden i bevakning/ som har ett
av punktens diarienummer. Ett ärende med punktens eget nummer följs i
Giffå; har ärendet numret utan förled märks kopplingen som osäker, eftersom
nämnderna har egna serier med samma siffror. Ett annat nummer i handlingen
kopplas bara när det har förled och står likadant i ärendet. Sökorden
kommer ur `sokord.py`.
"""

import re
from dataclasses import dataclass

from kommunhandlingar.diarienummer import normaliserat

from skanning.termer import monster
from webbplats.arende import Arende
from webbplats.kallelsen import Punkten
from webbplats.sokord import sokord

FORLED = re.compile(r"^[A-ZÅÄÖ]+-(?=\d)")


@dataclass(frozen=True)
class Traff:
    ort: str
    # Nämns bara i handlingen, inte i kallelsens rubrik eller förslag.
    i_handlingen: bool


@dataclass(frozen=True)
class Kopplad:
    punkten: Punkten
    traffar: list[Traff]
    egna: list[Arende]
    # Ärenden med punktens nummer utan förled: troligen samma, men inte säkert.
    osakra: list[Arende]
    namnda: list[Arende]
    sokord: list[str]


def koppla(
    punkten: Punkten, orter: list[str], platser: list[dict[str, str]], arenden: list[Arende]
) -> Kopplad:
    funna = traffar(punkten, orter, platser)
    return Kopplad(punkten, funna, *foljda(punkten, arenden), sokord(punkten, platser))


def traffar(punkten: Punkten, orter: list[str], platser: list[dict[str, str]]) -> list[Traff]:
    namnen = [(o, o) for o in orter] + [(p["ort"], p["namn"]) for p in platser]
    funna = [traff(punkten, ort, namn) for ort, namn in namnen]
    return sorted((t for t in funna if t), key=lambda t: t.i_handlingen)


def traff(punkten: Punkten, ort: str, namn: str) -> Traff | None:
    sok = monster(namn).search
    if sok(punkten.kallelsen):
        return Traff(ort, False)
    return Traff(ort, True) if sok(punkten.handlingen) else None


def foljda(punkten: Punkten, arenden: list[Arende]) -> tuple[list[Arende], ...]:
    eget, andra = punkten.numren[0], [n for n in punkten.numren[1:] if FORLED.match(n)]
    egna = [a for a in arenden if eget in numren_i(a)]
    utan = FORLED.sub("", eget)
    osakra = [a for a in arenden if a not in egna and utan in numren_i(a)]
    namnda = [a for a in arenden if a not in egna + osakra and any(n in numren_i(a) for n in andra)]
    return egna, osakra, namnda


def numren_i(arende: Arende) -> list[str]:
    falt = arende.falt.get("diarienummer", "")
    return [normaliserat(n.strip()) for n in falt.split(",") if n.strip()]
