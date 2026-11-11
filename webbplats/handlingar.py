"""Krav: K25 i KRAV.md. Test: tests/test_handlingar.py.

Handlingarna som ett steg bygger på, intill steget, och förslaget i korthet
med en källa för varje punkt.
"""

from html import escape

from webbplats.arende import Arende, Handelse
from webbplats.kartlankar import Kartlankar


def handlingar(handelse: Handelse) -> str:
    if not handelse.handlingar:
        return ""
    lankar = " · ".join(f'<a href="{escape(u)}">{escape(t)}</a>' for t, u in handelse.handlingar)
    return f'<span class="handlingar"><strong>Handlingar:</strong> {lankar}</span>'


def forslaget(arende: Arende, karta: Kartlankar) -> str:
    if not arende.forslaget:
        return ""
    punkter = "".join(
        f'<li>{karta.lanka(p.text)} <a href="{escape(p.lank)}">{escape(p.kalla)}</a></li>'
        for p in arende.forslaget
    )
    return f'<h2>Förslaget i korthet</h2><ul class="forslaget">{punkter}</ul>'
