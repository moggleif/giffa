"""Krav: K5, K6, K7, K8 och K12 i KRAV.md. Test: tests/test_sidor.py.

Startsidan med det nya, det som pågår och det som är beslutat, historiken
med det som är klart eller avbrutet och sidan om vad som bevakas.
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

STARTSIDAN = (("pågår", "Pågår"), ("beslutat", "Beslutat"))
HISTORIKEN = ("klart", "avbrutet")


def startsida(sajt: Sajt, arenden: list[Arende], runda: Runda) -> str:
    delar = "".join(
        avsnitt(sajt, rubrik, [a for a in arenden if a.falt["status"] == status])
        for status, rubrik in STARTSIDAN
    )
    inledning = (
        "<p>Vad som beslutas, planeras och byggs i "
        f"{escape(', '.join(sajt.orter))}. Varje händelse länkar till sin källa.</p>"
    )
    paverka = tycka_till_nu(arenden, sajt.byggd.date(), adress)
    innehall = inledning + urval(sajt) + paverka + nytt(arenden, runda)
    innehall += teckenforklaring() + delar
    return sida(sajt, "index.html", "Giffå", innehall)


def nytt(arenden: list[Arende], runda: Runda) -> str:
    fran, till = runda.fran, runda.till
    korten = "".join(
        nytt_kort(a, nya, adress(a))
        for a in arenden
        if (nya := [h for h in a.handelser if fran <= h.datum <= till])
    )
    innehall = f'<div class="kort">{korten}</div>' if korten else "<p>Inga nya händelser.</p>"
    return (
        f'<h2 id="nytt">Nytt sedan förra rundan</h2>'
        f'<p class="period">Rundans period: {tid(fran)} till {tid(till)}. {escape(runda.anteckning)}</p>'
        f"{innehall}"
    )


def adress(arende: Arende) -> str:
    return "historik.html" if arende.falt["status"] in HISTORIKEN else ""


def avsnitt(sajt: Sajt, rubrik: str, arenden: list[Arende]) -> str:
    if not arenden:
        return f"<h2>{rubrik}</h2><p>Inga ärenden ännu.</p>"
    korten = "".join(kort(a, sajt) for a in arenden)
    rader = tabell(arenden, sajt.byggd.date())
    return f'<h2>{rubrik}</h2>{rader}<div class="kort">{korten}</div>'


def historik(sajt: Sajt, arenden: list[Arende]) -> str:
    klara = [a for a in arenden if a.falt["status"] in HISTORIKEN]
    inledning = "<p>Ärenden som är klara – byggda, på plats – eller avbrutna.</p>"
    innehall = inledning + urval(sajt) + teckenforklaring() + avsnitt(sajt, "Ärendena", klara)
    return sida(sajt, "historik.html", "Historik", innehall)
