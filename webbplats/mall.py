"""Krav: K9 och K14 i KRAV.md. Test: tests/test_sidor.py.

Det varje sida har gemensamt: huvudet, menyn, urvalet och sidfoten med
länken till repot.
"""

from dataclasses import dataclass
from datetime import datetime
from html import escape

from webbplats.datum import tid

MENY = (("index.html", "Start"), ("historik.html", "Historik"), ("bevakar.html", "Vad vi bevakar"))

AKTUELL = ' aria-current="page"'


@dataclass(frozen=True)
class Sajt:
    repo: str
    byggd: datetime
    orter: list[str]


def sida(sajt: Sajt, adress: str, rubrik: str, innehall: str) -> str:
    return f"""<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(rubrik)} – Giffå</title>
<link rel="stylesheet" href="stil.css">
</head>
<body>
<a class="hoppa" href="#innehall">Hoppa till innehållet</a>
{meny(adress)}
<main id="innehall" tabindex="-1">
<h1>{escape(rubrik)}</h1>
{innehall}
</main>
{sidfot(sajt)}
<script src="urval.js"></script>
</body>
</html>
"""


def meny(aktuell: str) -> str:
    poster = "".join(
        f'<li><a href="{adress}"{AKTUELL * (adress == aktuell)}>{namn}</a></li>'
        for adress, namn in MENY
    )
    return f'<nav aria-label="Webbplatsen"><ul>{poster}</ul></nav>'


def urval(sajt: Sajt) -> str:
    knappar = "".join(
        f'<button type="button" data-urval="{escape(ort)}">{escape(ort)}</button>'
        for ort in ["Alla", *sajt.orter]
    )
    return f'<div class="urval" role="group" aria-label="Visa ort" hidden>{knappar}</div>'


def sidfot(sajt: Sajt) -> str:
    repo = escape(sajt.repo)
    return (
        f'<footer><p>Källkod, ärenden och källor: <a href="{repo}">{repo}</a>. '
        f"Sidan byggdes {tid(sajt.byggd.date())} klockan {sajt.byggd:%H.%M}.</p></footer>"
    )
