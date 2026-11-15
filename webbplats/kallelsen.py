"""Krav: K34 i KRAV.md, beslut 0012. Test: tests/test_ksmotet.py.

Kommunstyrelsens kommande sammanträde ur en utcheckning av kommunhandlingar:
det första datumet från byggdagen i kalendern eller bland sammanträdenas
kataloger, och kallelsens dagordning med handlingens sidor och
sammanfattningen. Dagordningen och handlingen tolkas med datapoolens egen
kod (K54 där), så att samma sak inte räknas fram två gånger.
"""

import csv
from dataclasses import dataclass
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


def kommande(pool: Path, dag: date) -> Motet | None:
    datum = min((d for d in datumen(pool) if d >= dag), default=None)
    if datum is None:
        return None
    katalog = f"{ORGAN}/{datum.year}/{datum}"
    mapp = pool / "data" / KOMMUN / katalog
    kallelse = mapp / "kallelse.md"
    return Motet(datum, katalog, punkterna(mapp) if kallelse.exists() else None)


def datumen(pool: Path) -> set[date]:
    with (pool / "kalender" / f"{KOMMUN}.csv").open(encoding="utf-8") as fil:
        rader = [r for r in csv.DictReader(fil) if r["organ"] == ORGAN]
    mappar = (pool / "data" / KOMMUN / ORGAN).glob("*/*-*-*")
    return {date.fromisoformat(r["datum"]) for r in rader} | {
        date.fromisoformat(m.name) for m in mappar
    }


def punkterna(mapp: Path) -> list[Punkten]:
    punkter = dagordning(text(mapp / "kallelse.md"))
    fil = mapp / "handlingar.md"
    handlingar = sidor(text(fil)) if fil.exists() else {}
    omfang = handlingen(handlingar, punkter)
    return [punkten(p, handlingar, omfang.get(p.nummer)) for p in punkter]


def punkten(punkt: Punkt, handlingar: dict[int, str], omfang: range | None) -> Punkten:
    sidorna = [handlingar[s] for s in omfang or ()]
    i_handlingen = [n for s in sidorna for n in diarienummer(s)]
    fullt = next((n for n in i_handlingen if ar_punktens(n, punkt)), punkt.diarienummer)
    return Punkten(
        punkt,
        tuple(dict.fromkeys([fullt, *i_handlingen])),
        omfang,
        sammanfattning(handlingar, omfang) if omfang else (),
        "\n".join([punkt.rubrik, *(punkt.forslag or ())]),
        "\n".join(sidorna),
    )


def text(fil: Path) -> str:
    return brodtext(fil.read_text(encoding="utf-8"))
