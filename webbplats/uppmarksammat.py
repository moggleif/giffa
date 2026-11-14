"""Krav: K27 i KRAV.md. Test: tests/test_uppmarksammat.py.

Läser bevakning/uppmarksammade.csv – namnen folk använder på ärendena, i
den ordning projektägaren skrivit dem – och ger rutan Uppmärksammat på
startsidan.
"""

import csv
from collections.abc import Sequence
from dataclasses import dataclass
from html import escape
from io import StringIO

from webbplats.arende import LANK, Arende
from webbplats.mall import urvalslista

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


def ruta(namnen: Sequence[Namn], arenden: list[Arende]) -> str:
    if not namnen:
        return ""
    per_id = {a.id: a for a in arenden}
    poster = "".join(post(namn, [per_id[i] for i in namn.arenden]) for namn in namnen)
    return (
        '<h2 id="uppmarksammat">Uppmärksammat</h2>'
        "<p>Ärenden som många följer, under namnen de har i folkmun eller ett "
        "gemensamt ämne. Projektägaren väljer dem; vid varje namn står var det "
        "kommer ifrån.</p>"
        + urvalslista(f'<ul class="uppmarksammat">{poster}</ul>')
    )


def post(namn: Namn, arenden: list[Arende]) -> str:
    orter = sorted({ort for a in arenden for ort in a.orter})
    rader = "".join(
        f'<li data-ort="{escape("|".join(a.orter))}"><a href="{a.sida}">{escape(a.falt["rubrik"])}</a> '
        f"<small>{escape(', '.join(a.orter))} · {a.falt['status']}</small></li>"
        for a in arenden
    )
    return (
        f'<li data-ort="{escape("|".join(orter))}"><strong>{escape(namn.namn)}</strong> '
        f'<small>Namnet: {", ".join(kalla(k) for k in namn.kallor)}</small><ul>{rader}</ul></li>'
    )


def kalla(text: str) -> str:
    if traff := LANK.fullmatch(text):
        return f'<a href="{escape(traff.group(2))}">{escape(traff.group(1))}</a>'
    return escape(text)
