"""Krav: K34 i KRAV.md, beslut 0012. Test: tests/test_ksmotet.py.

Kommunstyrelsens kommande sammanträde ur en utcheckning av kommunhandlingar:
det första datumet från byggdagen i kalendern, eller det föregående i
väntan på nästa kallelse, och kallelsens dagordning
med handlingens sidor och sammanfattningen. Dagordningen och handlingen
tolkas med datapoolens egen kod (K54 där), så att samma sak inte räknas
fram två gånger.
"""

import csv
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

from kommunhandlingar.frontmatter import brodtext
from kommunhandlingar.webbplats.dagordning import Punkt, dagordning
from kommunhandlingar.webbplats.punktsidor import (
    ar_punktens,
    diarienummer,
    handlingen,
    sammanfattning,
    sidor,
)

KOMMUN = "kungsbacka"
ORGAN = "ks"


@dataclass(frozen=True)
class Punkten:
    punkt: Punkt
    # Punktens fulla diarienummer först, sedan de andra i handlingen.
    numren: tuple[str, ...]
    handling: range | None
    sammanfattning: tuple[str, ...]
    # Rubriken och förslaget, och för sig handlingens sidor: orterna söks i dem.
    kallelsen: str
    handlingen: str


@dataclass(frozen=True)
class Motet:
    datum: date
    # Sammanträdets katalog i kommunens: `ks/2026/2026-11-24`.
    katalog: str
    # `None` när kallelsen inte finns i poolen än.
    punkter: list[Punkten] | None
    handlingar: bool
    # Ett sammanträde före byggdagen, som visas i väntan på nästa kallelse.
    foregaende: bool = False
    # Nästa sammanträde i kalendern när det föregående visas.
    nasta: date | None = None


# Nästa sammanträde när dess kallelse finns, annars det senaste före
# byggdagen som har en kallelse, och annars nästa utan punkter.
def kommande(pool: Path, dag: date) -> Motet | None:
    alla = sorted(datumen(pool))
    nasta = next((d for d in alla if d >= dag), None)
    tidigare = [d for d in alla if d < dag and kallelsen(pool, d).exists()]
    if (nasta and kallelsen(pool, nasta).exists()) or not tidigare:
        return motet(pool, nasta) if nasta else None
    return replace(motet(pool, tidigare[-1]), foregaende=True, nasta=nasta)


def motet(pool: Path, datum: date) -> Motet:
    mapp = kallelsen(pool, datum).parent
    punkter = punkterna(mapp) if (mapp / "kallelse.md").exists() else None
    return Motet(datum, katalog(datum), punkter, (mapp / "handlingar.md").exists())


def katalog(datum: date) -> str:
    return f"{ORGAN}/{datum.year}/{datum}"


def kallelsen(pool: Path, datum: date) -> Path:
    return pool / "data" / KOMMUN / katalog(datum) / "kallelse.md"


def datumen(pool: Path) -> set[date]:
    with (pool / "kalender" / f"{KOMMUN}.csv").open(encoding="utf-8") as fil:
        rader = [r for r in csv.DictReader(fil) if r["organ"] == ORGAN]
    return {date.fromisoformat(r["datum"]) for r in rader}


def punkterna(mapp: Path) -> list[Punkten]:
    punkter = dagordning(text(mapp / "kallelse.md"))
    fil = mapp / "handlingar.md"
    handlingar = sidor(text(fil)) if fil.exists() else {}
    omfang = handlingen(handlingar, punkter)
    return [punkten(p, handlingar, omfang.get(p.nummer)) for p in punkter]


def punkten(punkt: Punkt, handlingar: dict[int, str], omfang: range | None) -> Punkten:
    sidorna = [handlingar[s] for s in omfang or ()]
    i_handlingen = [n for s in sidorna for n in diarienummer(s)]
    fullt = next((n for n in i_handlingen if ar_punktens(n, punkt)), med_forled(punkt))
    return Punkten(
        punkt,
        tuple(dict.fromkeys([fullt, *i_handlingen])),
        omfang,
        sammanfattning(handlingar, omfang) if omfang else (),
        "\n".join([punkt.rubrik, *(punkt.forslag or ())]),
        "\n".join(sidorna),
    )


# Kallelsen skriver kommunstyrelsens nummer utan förled.
def med_forled(punkt: Punkt) -> str:
    nummer = punkt.diarienummer
    return f"{ORGAN.upper()}-{nummer}" if nummer[:1].isdigit() else nummer


def text(fil: Path) -> str:
    return brodtext(fil.read_text(encoding="utf-8"))
