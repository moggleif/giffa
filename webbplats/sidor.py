"""Krav: K5, K6, K7 och K8 i KRAV.md. Test: tests/test_sidor.py.

Startsidan med det nya, det som pågår och det som är beslutat, historiken
med det som är klart eller avbrutet och sidan om vad som bevakas.
"""

from datetime import date
from html import escape

from webbplats.arende import Arende
from webbplats.ikoner import teckenforklaring
from webbplats.kort import kort, nytt_kort
from webbplats.mall import Sajt, sida, urval
from webbplats.tabell import tabell

STARTSIDAN = (("pågår", "Pågår"), ("beslutat", "Beslutat"))
HISTORIKEN = ("klart", "avbrutet")


def startsida(sajt: Sajt, arenden: list[Arende], runda: tuple[date, date]) -> str:
    delar = "".join(
        avsnitt(sajt, rubrik, [a for a in arenden if a.falt["status"] == status])
        for status, rubrik in STARTSIDAN
    )
    inledning = (
        "<p>Vad som beslutas, planeras och byggs i "
        f"{escape(', '.join(sajt.orter))}. Varje händelse länkar till sin källa.</p>"
    )
    innehall = inledning + urval(sajt) + nytt(arenden, runda) + teckenforklaring() + delar
    return sida(sajt, "index.html", "Giffå", innehall)


def nytt(arenden: list[Arende], runda: tuple[date, date]) -> str:
    fran, till = runda
    korten = "".join(
        nytt_kort(a, nya, adress(a))
        for a in arenden
        if (nya := [h for h in a.handelser if fran <= h.datum <= till])
    )
    innehall = f'<div class="kort">{korten}</div>' if korten else "<p>Inga nya händelser.</p>"
    return (
        f'<h2 id="nytt">Nytt sedan förra rundan</h2>'
        f'<p class="period">Rundans period: {fran} till {till}.</p>{innehall}'
    )


def adress(arende: Arende) -> str:
    return "historik.html" if arende.falt["status"] in HISTORIKEN else ""


def avsnitt(sajt: Sajt, rubrik: str, arenden: list[Arende]) -> str:
    if not arenden:
        return f"<h2>{rubrik}</h2><p>Inga ärenden ännu.</p>"
    korten = "".join(kort(a, sajt.repo) for a in arenden)
    return f'<h2>{rubrik}</h2>{tabell(arenden)}<div class="kort">{korten}</div>'


def historik(sajt: Sajt, arenden: list[Arende]) -> str:
    klara = [a for a in arenden if a.falt["status"] in HISTORIKEN]
    inledning = "<p>Ärenden som är klara – byggda, på plats – eller avbrutna.</p>"
    innehall = inledning + urval(sajt) + teckenforklaring() + avsnitt(sajt, "Ärendena", klara)
    return sida(sajt, "historik.html", "Historik", innehall)
