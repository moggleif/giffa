"""Krav: K9, K14, K18 och K22 i KRAV.md. Test: tests/test_sidor.py.

Det varje sida har gemensamt: huvudet, menyn, urvalet och sidfoten med
länken till repot.
"""

from dataclasses import dataclass, field
from datetime import datetime
from html import escape

from webbplats.datum import tid
from webbplats.kartlankar import Kartlankar
from webbplats.underlag import alla_orter

MENY = (
    ("index.html", "Start"),
    ("pagar.html", "Pågår"),
    ("beslutat.html", "Beslutat"),
    ("historik.html", "Historik"),
    ("bevakar.html", "Vad vi bevakar"),
)

AKTUELL = ' aria-current="page"'
SVENSKA_SIST = str.maketrans("åäö", "{|}")


@dataclass(frozen=True)
class Sajt:
    repo: str
    byggd: datetime
    foreningar: dict[str, list[str]]
    karta: Kartlankar = field(default_factory=Kartlankar)

    @property
    def orter(self) -> list[str]:
        return alla_orter(self.foreningar)


def sida(sajt: Sajt, adress: str, rubrik: str, innehall: str) -> str:
    rot = "../" * adress.count("/")
    return f"""<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(rubrik)} – Giffå</title>
<link rel="stylesheet" href="{rot}stil.css">
</head>
<body>
<a class="hoppa" href="#innehall">Hoppa till innehållet</a>
{meny(adress, rot)}
<main id="innehall" tabindex="-1">
<h1>{sajt.karta.lanka(rubrik)}</h1>
{innehall}
</main>
{sidfot(sajt)}
<script src="{rot}urval.js"></script>
</body>
</html>
"""


def meny(aktuell: str, rot: str) -> str:
    poster = "".join(
        f'<li><a href="{rot}{adress}"{AKTUELL * (adress == aktuell)}>{namn}</a></li>'
        for adress, namn in MENY
    )
    return f'<nav aria-label="Webbplatsen"><ul>{poster}</ul></nav>'


def urval(sajt: Sajt) -> str:
    foreningar = "".join(knapp("forening", namn) for namn in sajt.foreningar)
    orter = sorted(
        ((ort, namn) for namn, lista in sajt.foreningar.items() for ort in lista),
        key=lambda par: bokstavsordning(par[0]),
    )
    ortknappar = "".join(
        f'<button type="button" data-urval-ort="{escape(ort)}" data-urval-i="{escape(namn)}">'
        f"{escape(ort)}</button>"
        for ort, namn in orter
    )
    return (
        '<div class="urval" hidden><div role="group" aria-label="Visa förening">'
        f'<button type="button" data-alla>Alla</button>{foreningar}</div>'
        f'<div role="group" aria-label="Visa ort" class="orter">{ortknappar}</div></div>'
    )


def bokstavsordning(namn: str) -> str:
    return namn.lower().translate(SVENSKA_SIST)


def knapp(slag: str, namn: str) -> str:
    return f'<button type="button" data-urval-{slag}="{escape(namn)}">{escape(namn)}</button>'


def urvalslista(innehall: str) -> str:
    return (
        f'<div class="urvalslista">{innehall}'
        '<p class="inget-val" hidden>Inget här för det valet.</p></div>'
    )


def sidfot(sajt: Sajt) -> str:
    repo = escape(sajt.repo)
    return (
        f'<footer><p>Källkod, ärenden och källor: <a href="{repo}">{repo}</a>. '
        f"Sidan byggdes {tid(sajt.byggd.date())} klockan {sajt.byggd:%H.%M}.</p></footer>"
    )
