"""Krav: K28 i KRAV.md. Test: tests/test_sok.py och tests/test_sok.js.

Sidan Sök: alla ärenden i en lista med det man kan söka på i data-sok, och
rutan som docs/sok.js filtrerar med. Utan skript står hela listan.
"""

from html import escape

from webbplats.arende import Arende
from webbplats.kort import namn_rad
from webbplats.mall import Sajt, sida


def soksida(sajt: Sajt, arenden: list[Arende]) -> str:
    poster = "".join(post(a) for a in arenden)
    innehall = (
        "<p>Sök bland alla ärenden på rubriken, namnen de kallas, orten eller organet.</p>"
        '<p class="sok" hidden><label for="sok">Sök</label> '
        '<input id="sok" type="search" autocomplete="off"></p>'
        f'<ul class="sokning">{poster}</ul>'
        '<p class="ingen-traff" hidden>Inga ärenden matchar sökningen.</p>'
        '<script src="sok.js"></script>'
    )
    return sida(sajt, "sok.html", "Sök", innehall)


def post(arende: Arende) -> str:
    falt = arende.falt
    sokbart = " ".join((falt["rubrik"], *arende.kallas, *arende.orter, falt["organ"])).lower()
    return (
        f'<li data-sok="{escape(sokbart)}"><a href="{arende.sida}">{escape(falt["rubrik"])}</a> '
        f"<small>{escape(', '.join(arende.orter))} · {falt['status']}</small>{namn_rad(arende)}</li>"
    )
