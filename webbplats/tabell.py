"""Krav: K4, K12 och K27 i KRAV.md. Test: tests/test_sidor.py.

Tidslinjen som på kommunhandlingars sidor om initiativ och lokalbehov: en
rad per ärende, en kolumn per år och årets händelser som ikoner på ett band
från första till sista året. Ett ärende med ett kommande tillfälle att
tycka till får en markering med datumet.
"""

from datetime import date
from html import escape

from webbplats.arende import Arende
from webbplats.datum import tid
from webbplats.ikoner import ikon
from webbplats.paverka import kommande


def tabell(arenden: list[Arende], idag: date) -> str:
    aren = arsspann(arenden)
    huvud = "".join(f'<th scope="col">{ar}</th>' for ar in aren)
    rader = "".join(rad(a, aren, idag) for a in arenden)
    return (
        '<div class="tabell"><table class="tidslinje">'
        f'<colgroup><col class="rubrik"></colgroup>'
        f'<thead><tr><th scope="col">Ärende</th>{huvud}</tr></thead>'
        f"<tbody>{rader}</tbody></table></div>"
    )


def arsspann(arenden: list[Arende]) -> range:
    aren = [h.datum.year for a in arenden for h in a.handelser]
    return range(min(aren), max(aren) + 1)


def rad(arende: Arende, aren: range, idag: date) -> str:
    egna = range(arende.handelser[-1].datum.year, arende.handelser[0].datum.year + 1)
    celler = "".join(cell(arende, ar, egna) for ar in aren)
    return (
        f'<tr data-ort="{escape("|".join(arende.orter))}"><th scope="row">'
        f'<a href="{arende.sida}">{escape(arende.falt["rubrik"])}</a> '
        f"<small>{escape(', '.join(arende.orter))}</small>{namn_liten(arende)}"
        f"{tycka_till_marke(arende, idag)}"
        f"</th>{celler}</tr>"
    )


def tycka_till_marke(arende: Arende, idag: date) -> str:
    if not (tillfallen := kommande(arende, idag)):
        return ""
    forsta = tillfallen[0]
    preliminart = " (preliminärt)" if forsta.steg == "vantas" else ""
    return f' <small class="paverka">Tycka till {tid(forsta.datum)}{preliminart}</small>'


def cell(arende: Arende, ar: int, egna: range) -> str:
    if ar not in egna:
        return "<td></td>"
    klass = "band" + " start" * (ar == egna[0]) + " slut" * (ar == egna[-1])
    arets = [h for h in reversed(arende.handelser) if h.datum.year == ar]
    return f'<td class="{klass}">{"".join(ikon(h) for h in arets)}</td>'


def namn_liten(arende: Arende) -> str:
    namn = ", ".join(arende.kallas)
    return f' <small class="kallas">Uppmärksammat som {escape(namn)}</small>' if namn else ""
