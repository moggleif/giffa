"""Krav: K27 i KRAV.md. Test: tests/test_uppmarksammat.py.

Läser bevakning/uppmarksammade.csv – namnen folk använder på ärendena, i
den ordning projektägaren skrivit dem – och ger varje ärende sina namn.
"""

import csv
from dataclasses import dataclass
from io import StringIO

from webbplats.arende import LANK

KOLUMNER = ["namn", "arende", "kalla"]


@dataclass(frozen=True)
class Namn:
    namn: str
    arenden: tuple[str, ...]
    kallor: tuple[str, ...]


def las(text: str, finns: set[str]) -> list[Namn]:
    lasare = csv.DictReader(StringIO(text))
    if lasare.fieldnames != KOLUMNER:
        raise ValueError(f"kolumnerna ska vara {','.join(KOLUMNER)}")
    namnen: dict[str, Namn] = {}
    for rad in ({k: (v or "").strip() for k, v in r.items()} for r in lasare):
        kontrollera(rad, finns)
        if rad["arende"] in namnen.get(rad["namn"], Namn("", (), ())).arenden:
            raise ValueError(f"samma namn och ärende två gånger: {rad['namn']}, {rad['arende']}")
        tidigare = namnen.get(rad["namn"], Namn(rad["namn"], (), ()))
        namnen[rad["namn"]] = Namn(
            tidigare.namn,
            tidigare.arenden + (rad["arende"],),
            tidigare.kallor + (rad["kalla"],) * (rad["kalla"] not in tidigare.kallor),
        )
    return list(namnen.values())


def kontrollera(rad: dict[str, str], finns: set[str]) -> None:
    if tomma := [kolumn for kolumn in KOLUMNER if not rad[kolumn]]:
        raise ValueError(f"tomt fält {', '.join(tomma)} på raden {rad}")
    if rad["arende"] not in finns:
        raise ValueError(f"ärendet finns inte: {rad['arende']}")
    if rad["kalla"].startswith("[") and not LANK.fullmatch(rad["kalla"]):
        raise ValueError(f"källan är ingen https-länk: {rad['kalla']}")


def namn_per_arende(namnen: list[Namn]) -> dict[str, tuple[str, ...]]:
    per_arende: dict[str, tuple[str, ...]] = {}
    for namn in namnen:
        for arende in namn.arenden:
            per_arende[arende] = per_arende.get(arende, ()) + (namn.namn,)
    return per_arende
