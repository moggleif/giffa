"""Krav: K27 i KRAV.md. Test: tests/test_uppmarksammat.py.

Läser bevakning/uppmarksammade.csv – namnen folk använder på ärendena, i
den ordning projektägaren skrivit dem – och ger varje ärende sina namn
med källan till varje namn.
"""

import csv
from io import StringIO

from webbplats.arende import LANK, Namn

KOLUMNER = ["namn", "arende", "kalla"]


def las(text: str, finns: set[str]) -> dict[str, tuple[Namn, ...]]:
    lasare = csv.DictReader(StringIO(text))
    if lasare.fieldnames != KOLUMNER:
        raise ValueError(f"kolumnerna ska vara {','.join(KOLUMNER)}")
    per_arende: dict[str, tuple[Namn, ...]] = {}
    for rad in ({k: (v or "").strip() for k, v in r.items()} for r in lasare):
        kontrollera(rad, finns)
        tidigare = per_arende.get(rad["arende"], ())
        if rad["namn"] in (n.namn for n in tidigare):
            raise ValueError(f"samma namn och ärende två gånger: {rad['namn']}, {rad['arende']}")
        per_arende[rad["arende"]] = tidigare + (Namn(rad["namn"], rad["kalla"]),)
    return per_arende


def kontrollera(rad: dict[str, str], finns: set[str]) -> None:
    if tomma := [kolumn for kolumn in KOLUMNER if not rad[kolumn]]:
        raise ValueError(f"tomt fält {', '.join(tomma)} på raden {rad}")
    if rad["arende"] not in finns:
        raise ValueError(f"ärendet finns inte: {rad['arende']}")
    if rad["kalla"].startswith("[") and not LANK.fullmatch(rad["kalla"]):
        raise ValueError(f"källan är ingen https-länk: {rad['kalla']}")
