"""Krav: K28 i KRAV.md, beslut 0018. Test: tests/test_sok.py.

Sidan Sök: alla ärenden i en lista. Med skript fäller docs/sokruta.js ut
sökfältet överst (data-sok-oppen); utan skript går listan att söka i med
webbläsarens egen sökning.
"""

from html import escape

from webbplats.arende import Arende
from webbplats.kort import namn_rad
from webbplats.mall import Sajt, sida


def soksida(sajt: Sajt, arenden: list[Arende]) -> str:
    poster = "".join(post(a) for a in arenden)
    return sida(sajt, "sok.html", "Sök", f'<ul class="sokning" data-sok-oppen>{poster}</ul>')


def post(arende: Arende) -> str:
    falt = arende.falt
    return (
        f'<li><a href="{arende.sida}">{escape(falt["rubrik"])}</a> '
        f"<small>{escape(', '.join(arende.orter))} · {falt['status']}</small>{namn_rad(arende)}</li>"
    )
