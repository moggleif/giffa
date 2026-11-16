"""Krav: K4, K5, K6, K9, K12, K18, K23, K24, K27 och K33 i KRAV.md. Test: tests/test_sidor.py.

Ett kort per ärende under tabellen, korten för det som är nytt sedan
förra rundan överst på startsidan, och delarna som ärendets egen sida
återanvänder.
"""

from html import escape

from webbplats.arende import LANK, STEG, Arende, Handelse, Namn
from webbplats.datum import tid
from webbplats.handlingar import handlingar
from webbplats.kartlankar import Kartlankar
from webbplats.mall import Sajt
from webbplats.paverka import markering
from webbplats.stege import stege

TIDNING = (
    '<svg viewBox="0 0 16 16" width="1.2em" height="1.2em" aria-hidden="true">'
    '<path d="M2 3h10v10H3a1 1 0 0 1-1-1zM12 6h2v6a1 1 0 0 1-2 0M4 5h6M4 8h6M4 11h4" '
    'fill="none" stroke="currentColor" stroke-width="1.5"/></svg>'
)


def kort(arende: Arende, sajt: Sajt) -> str:
    falt, senaste = arende.falt, arende.handelser[0]
    return (
        f'<article id="{arende.id}" data-ort="{escape("|".join(arende.orter))}">'
        f"{markor(arende)}<h3>{sajt.karta.lanka(falt['rubrik'])}</h3>{namn_rad(arende)}"
        f'<p class="organ">{escape(organ(arende))}</p>'
        + stege(arende, sajt.byggd.date())
        + (f"<p>{sajt.karta.lanka(arende.ingress)}</p>" if arende.ingress else "")
        + f"<p>Senaste steget: {STEG[senaste.steg]}, {tid(senaste.datum)}</p>"
        + markering(arende, sajt)
        + f'<p><a href="{arende.sida}">Läs mer: alla {len(arende.handelser)} '
        "händelser med källor</a></p></article>"
    )


def markor(arende: Arende) -> str:
    forsta, sista = arende.handelser[-1].datum.year, arende.handelser[0].datum.year
    aren = str(forsta) if forsta == sista else f"Pågått {forsta}–{sista}"
    orter = "".join(f"<span>{escape(o)}</span>" for o in arende.orter)
    return f'<p class="markor"><span>{aren}</span>{orter}</p>'


def namn_rad(arende: Arende) -> str:
    return f'<p class="kallas">Uppmärksammat som {etiketter(arende)}</p>' if arende.kallas else ""


def etiketter(arende: Arende) -> str:
    return " ".join(etikett(n) for n in arende.kallas)


def etikett(namn: Namn) -> str:
    if traff := LANK.fullmatch(namn.kalla):
        return f'<a class="etikett" href="{escape(traff.group(2))}" title="Namnet: {escape(traff.group(1))}">{escape(namn.namn)}</a>'
    return f'<span class="etikett" title="Namnet: {escape(namn.kalla)}">{escape(namn.namn)}</span>'


def organ(arende: Arende) -> str:
    diarienummer = arende.falt.get("diarienummer")
    return arende.falt["organ"] + (f" · {diarienummer}" if diarienummer else "")


def post(handelse: Handelse, karta: Kartlankar) -> str:
    return (
        f"<li>{tid(handelse.datum)} <strong>{STEG[handelse.steg]}</strong> "
        f"{karta.lanka(handelse.text)} "
        f'<a href="{escape(handelse.lank)}">{escape(handelse.kalla)}</a>'
        f"{handlingar(handelse)}</li>"
    )


def media(arende: Arende) -> str:
    if not arende.media:
        return ""
    poster = "".join(
        f'<li><span class="media">{TIDNING}<strong>{escape(m.var)}</strong></span> '
        f'{tid(m.datum)} <a href="{escape(m.lank)}">{escape(m.rubrik)}</a></li>'
        for m in arende.media
    )
    return f"<h2>I media och debatt</h2><ul>{poster}</ul>"


def nytt_kort(arende: Arende, nya: list[Handelse], karta: Kartlankar) -> str:
    return (
        f'<article data-ort="{escape("|".join(arende.orter))}">{markor(arende)}'
        f"<h3>{karta.lanka(arende.falt['rubrik'])}</h3>"
        f"<details><summary>{len(nya)} ny{'a' * (len(nya) > 1)} "
        f"händelse{'r' * (len(nya) > 1)}</summary>"
        f"<ol>{''.join(post(h, karta) for h in nya)}</ol></details>"
        f'<p><a href="{arende.sida}">Hela ärendet</a></p></article>'
    )
