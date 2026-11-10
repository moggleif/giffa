"""Krav: K11 i KRAV.md. Test: tests/test_skanning.py.

Går igenom dokumenten i kommunhandlingars data/<kommun>/<organ>/<år>/<datum>/
från och med ett datum, sida för sida, och noterar vilka termer varje sida
nämner. Bara text läses; tabellerna bredvid dokumenten läses inte.
"""

import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from skanning.termer import monster

SIDA = re.compile(r"<!-- sida (\d+) -->")


@dataclass(frozen=True)
class Traff:
    dokument: str
    datum: date
    organ: str
    sida: int
    termer: list[str]


def dokument(data: Path, fran: date) -> list[Path]:
    return sorted(
        fil for fil in data.glob("*/*/*/*.md") if date.fromisoformat(fil.parent.name) >= fran
    )


def traffar(data: Path, fil: Path, termer: list[str]) -> list[Traff]:
    datum, organ = date.fromisoformat(fil.parent.name), fil.parts[-4]
    namn = fil.relative_to(data.parent).as_posix()
    return [
        Traff(namn, datum, organ, sida, funna)
        for sida, text in sidor(fil.read_text(encoding="utf-8"))
        if (funna := [t for t in termer if monster(t).search(text)])
    ]


def sidor(text: str) -> list[tuple[int, str]]:
    delar = SIDA.split(text)
    return [(int(nr), sida) for nr, sida in zip(delar[1::2], delar[2::2])]
