"""Krav: K32 i KRAV.md. Test: tests/test_pa_vag_upp.py.

Det som organen har informerats om men ännu inte har något förslag eller
tillfälle i: det partierna kan ta upp innan det blir ett förslag. Listan
återger bara att organet har informerats och gissar inte när beslutet kommer.
"""

from datetime import date, timedelta
from html import escape

from webbplats.arende import Arende
from webbplats.datum import tid
from webbplats.mall import Sajt, urvalslista
from webbplats.paverka import kommande
from webbplats.spar import tecken

PERIOD = timedelta(days=365)
INLEDNING = (
    "<p>Det som ett organ har informerats om det senaste året, men som ännu inte har "
    "något förslag: det partierna kan ta upp först. Nyast först.</p>"
)


def pa_vag_upp(arenden: list[Arende], sajt: Sajt) -> str:
    idag = sajt.byggd.date()
    valda = sorted((a for a in arenden if pa_vag(a, idag)), key=lambda a: a.handelser[0].datum, reverse=True)
    rader = "".join(rad(a) for a in valda)
    lista = urvalslista(f'<ul class="pa-vag-upp">{rader}</ul>') if rader else "<p>Inget just nu.</p>"
    return f'<h2 id="pa-vag-upp">På väg upp</h2>{INLEDNING}{lista}'


def pa_vag(arende: Arende, idag: date) -> bool:
    senaste = arende.handelser[0]
    return (
        arende.falt["status"] == "pågår"
        and senaste.steg == "info"
        and senaste.datum >= idag - PERIOD
        and not kommande(arende, idag)
    )


def rad(arende: Arende) -> str:
    senaste = arende.handelser[0]
    return (
        f'<li data-ort="{escape("|".join(arende.orter))}">{tecken("partiet")}'
        f'<a class="arende" href="{arende.sida}">{escape(arende.falt["rubrik"])}</a> '
        f"<small>{escape(', '.join(arende.orter))}</small><br>"
        f'<small>Information {tid(senaste.datum)} · <a href="{escape(senaste.lank)}" '
        f'title="{escape(senaste.text)}">{escape(senaste.kalla)}</a></small></li>'
    )
