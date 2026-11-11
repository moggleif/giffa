"""Krav: K23 och K24 i KRAV.md. Test: tests/test_karta.py.

Gör det i en text som går att söka fram i kommunens karta till länkar:
fastighetsbeteckningar, platserna i platser.csv, gatunamn och detaljplaner
med plannummer. Allt annat escapas.
"""

import re
from dataclasses import dataclass
from html import escape

from webbplats.fastighet import FASTIGHET, fastighet
from webbplats.karta import lank

PLAN = r"[A-ZÅÄÖ]{1,4}\d{1,4}"
PLANER = rf"(?P<planord>\b(?:[Dd]etaljplan(?:en|erna)?|[Pp]lan(?:en|erna)?)) (?P<planer>{PLAN}(?:(?:, | och ){PLAN})*)\b"
GATA = r"(?<![\w-])(?P<gata>[A-ZÅÄÖ][a-zåäö]+(?:vägen|gatan|leden|gränd|stigen|allén))\b"


@dataclass(frozen=True)
class Kartlankar:
    platser: tuple[str, ...] = ()

    @property
    def monster(self) -> str:
        namn = sorted((re.escape(escape(p)) for p in self.platser), key=len, reverse=True)
        plats = rf"(?<![\w-])(?P<plats>{'|'.join(namn) or '(?!)'})(?![\w-])"
        return f"{FASTIGHET}|{plats}|{PLANER}|{GATA}"

    def lanka(self, text: str) -> str:
        return re.sub(self.monster, ersatt, escape(text))


def ersatt(traff: re.Match[str]) -> str:
    if plats := traff.group("plats"):
        return lank(plats, plats)
    if gata := traff.group("gata"):
        return lank(gata, gata)
    if planer := traff.group("planer"):
        lankade = re.sub(PLAN, lambda p: lank(p.group(), p.group()), planer)
        return f"{traff.group('planord')} {lankade}"
    return fastighet(traff)


INTE_PA_KARTAN = ("förening", "hemtjänst", "detaljplan", "planprogram", "planbesked")


def ur_platser(platser: list[dict[str, str]]) -> Kartlankar:
    return Kartlankar(tuple(p["namn"] for p in platser if p["typ"] not in INTE_PA_KARTAN))
