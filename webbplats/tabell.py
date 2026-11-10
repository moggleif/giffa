"""Krav: K4 i KRAV.md. Test: tests/test_sidor.py.

Tidslinjen som på kommunhandlingars sidor om initiativ och lokalbehov: en
rad per ärende, en kolumn per år och årets händelser som ikoner på ett band
från första till sista året.
"""

from html import escape

from webbplats.arende import Arende
from webbplats.ikoner import ikon


def tabell(arenden: list[Arende]) -> str:
    aren = arsspann(arenden)
    huvud = "".join(f'<th scope="col">{ar}</th>' for ar in aren)
    rader = "".join(rad(a, aren) for a in arenden)
    return (
        '<div class="tabell"><table class="tidslinje">'
        f'<colgroup><col class="rubrik"></colgroup>'
        f'<thead><tr><th scope="col">Ärende</th>{huvud}</tr></thead>'
        f"<tbody>{rader}</tbody></table></div>"
    )


def arsspann(arenden: list[Arende]) -> range:
    aren = [h.datum.year for a in arenden for h in a.handelser]
    return range(min(aren), max(aren) + 1)


def rad(arende: Arende, aren: range) -> str:
    egna = range(arende.handelser[-1].datum.year, arende.handelser[0].datum.year + 1)
    celler = "".join(cell(arende, ar, egna) for ar in aren)
    return (
        f'<tr data-ort="{escape("|".join(arende.orter))}"><th scope="row">'
        f'<a href="#{arende.id}">{escape(arende.falt["rubrik"])}</a> '
        f"<small>{escape(', '.join(arende.orter))}</small></th>{celler}</tr>"
    )


def cell(arende: Arende, ar: int, egna: range) -> str:
    if ar not in egna:
        return "<td></td>"
    klass = "band" + " start" * (ar == egna[0]) + " slut" * (ar == egna[-1])
    arets = [h for h in reversed(arende.handelser) if h.datum.year == ar]
    return f'<td class="{klass}">{"".join(ikon(h) for h in arets)}</td>'
