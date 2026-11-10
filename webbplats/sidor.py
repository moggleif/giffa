"""Krav: K5, K6, K7 och K12 i KRAV.md. Test: tests/test_sidor.py.

Startsidan med det som går att påverka, det nya och hur många ärenden
varje lista har, och listorna: det som pågår, det som är beslutat och
historiken med det som är klart eller avbrutet.
"""

from html import escape

from webbplats.arende import Arende
from webbplats.datum import tid
from webbplats.ikoner import teckenforklaring
from webbplats.kort import kort, nytt_kort
from webbplats.mall import Sajt, sida, urval
from webbplats.paverka import tycka_till_nu
from webbplats.tabell import tabell
from webbplats.underlag import Runda

LISTOR = (
    ("pagar.html", "Pågår", ("pågår",), "Ärenden som inte är avgjorda."),
    ("beslutat.html", "Beslutat", ("beslutat",), "Ärenden som är avgjorda och att följa."),
    (
        "historik.html",
        "Historik",
        ("klart", "avbrutet"),
        "Ärenden som är klara – byggda, på plats – eller avbrutna.",
    ),
)


def startsida(sajt: Sajt, arenden: list[Arende], runda: Runda) -> str:
    inledning = (
        "<p>Vad som beslutas, planeras och byggs i "
        f"{escape(', '.join(sajt.orter))}. Varje händelse länkar till sin källa.</p>"
    )
    paverka = tycka_till_nu(arenden, sajt.byggd.date())
    innehall = inledning + urval(sajt) + paverka + nytt(arenden, runda) + oversikt(arenden)
    return sida(sajt, "index.html", "Giffå", innehall)


def oversikt(arenden: list[Arende]) -> str:
    poster = "".join(
        f'<li><a href="{adress}">{rubrik}</a>: {antal(arenden, statusar)} ärenden</li>'
        for adress, rubrik, statusar, _ in LISTOR
    )
    return f'<h2 id="alla">Alla ärenden</h2><ul class="oversikt">{poster}</ul>'


def antal(arenden: list[Arende], statusar: tuple[str, ...]) -> int:
    return sum(a.falt["status"] in statusar for a in arenden)


def nytt(arenden: list[Arende], runda: Runda) -> str:
    fran, till = runda.fran, runda.till
    korten = "".join(
        nytt_kort(a, nya)
        for a in arenden
        if (nya := [h for h in a.handelser if fran <= h.datum <= till])
    )
    innehall = f'<div class="kort">{korten}</div>' if korten else "<p>Inga nya händelser.</p>"
    return (
        f'<h2 id="nytt">Nytt sedan förra rundan</h2>'
        f'<p class="period">Rundans period: {tid(fran)} till {tid(till)}. {escape(runda.anteckning)}</p>'
        f"{innehall}"
    )


def lista(sajt: Sajt, arenden: list[Arende], listan: tuple) -> str:
    adress, rubrik, statusar, inledning = listan
    valda = [a for a in arenden if a.falt["status"] in statusar]
    innehall = f"<p>{inledning}</p>" + urval(sajt) + avsnitt(sajt, valda)
    return sida(sajt, adress, rubrik, innehall)


def avsnitt(sajt: Sajt, arenden: list[Arende]) -> str:
    if not arenden:
        return "<p>Inga ärenden ännu.</p>"
    korten = "".join(kort(a, sajt) for a in arenden)
    rader = tabell(arenden, sajt.byggd.date())
    return f'{teckenforklaring()}{rader}<div class="kort">{korten}</div>'
