"""Krav: K9, K14, K18, K22, K28, K34 och K35 i KRAV.md. Test: tests/test_sidor.py.

Det varje sida har gemensamt: huvudet, menyn, urvalet och sidfoten med
länken till repot. Menyn följer den gemensamma menyns form (beslut 0013):
en post är en länk, eller en rubrik med länkarna i sin undermeny.
"""

from dataclasses import dataclass, field
from datetime import datetime
from html import escape

from webbplats.datum import tid
from webbplats.kartlankar import Kartlankar
from webbplats.underlag import alla_orter

MENY = (
    ("index.html#tycka-till", "Tycka till"),
    ("pagar.html", "Pågår"),
    ("Beslutat", (("beslutat.html", "Beslutat"), ("historik.html", "Historik"))),
    ("ks-motet.html", "KS-mötet"),
    ("sok.html", "Sök"),
    ("bevakar.html", "Om"),
)

AKTUELL = ' aria-current="page"'
# Sidor utan urval: valet följer inte med i länken dit (K34).
UTAN_URVAL = ("ks-motet.html",)
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
<script src="{rot}tema.js"></script>
<link rel="stylesheet" href="{rot}sajter.css">
<link rel="stylesheet" href="{rot}stil.css">
<link rel="stylesheet" href="{rot}sok.css">
<script src="{rot}sajter.js" defer></script>
<script src="{rot}sokning.js" defer></script>
<script src="{rot}sokruta.js" defer></script>
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
    poster = "".join(menypost(forsta, andra, aktuell, rot) for forsta, andra in MENY)
    namn = f'<a class="sajtnamn" href="{rot}index.html"{AKTUELL * (aktuell == "index.html")}>Giffå</a>'
    return f'<nav class="sajtmeny" aria-label="Webbplatsen">{namn}<ul>{poster}</ul></nav>'


def menypost(forsta: str, andra: str | tuple, aktuell: str, rot: str) -> str:
    if isinstance(andra, str):
        return f"<li>{lank(forsta, andra, aktuell, rot)}</li>"
    lankar = "".join(f"<li>{lank(adress, namn, aktuell, rot)}</li>" for adress, namn in andra)
    return f"<li><details><summary>{forsta}</summary><ul>{lankar}</ul></details></li>"


def lank(adress: str, namn: str, aktuell: str, rot: str) -> str:
    return (
        f'<a href="{rot}{adress}"{AKTUELL * (adress == aktuell)}'
        f"{' data-utan-urval' * (adress in UTAN_URVAL)}>{namn}</a>"
    )


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
        '<details class="ortval" hidden><summary>Ort: <span class="ortval-namn">Alla</span></summary>'
        '<div class="urval"><div role="group" aria-label="Visa förening">'
        f'<button type="button" data-alla>Alla</button>{foreningar}</div>'
        f'<div role="group" aria-label="Visa ort" class="orter">{ortknappar}</div></div></details>'
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
