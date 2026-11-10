"""Krav: K12 i KRAV.md. Test: tests/test_sidor.py.

När man kan tycka till: ärendenas kommande samråd, granskningar, yttranden
och beslut i tur och ordning överst på startsidan, och som en markering på
varje ärendes kort och rad. Det som har passerat visas inte.
"""

from collections.abc import Callable
from datetime import date
from html import escape

from webbplats.arende import Arende, Handelse

TILLFALLE = {
    "samrad": "Samråd – synpunkter senast",
    "granskning": "Granskning – synpunkter senast",
    "yttrande": "Yttrande",
    "beslut": "Beslut",
    "vantas": "Beslut väntas, preliminärt",
}
INLEDNING = (
    "<p>Det som går att påverka i de bevakade ärendena, med det som ligger "
    "närmast först. Varje rad länkar till källan och till ärendet.</p>"
)


def kommande(arende: Arende, idag: date) -> list[Handelse]:
    return sorted((t for t in arende.tillfallen if t.datum >= idag), key=lambda t: t.datum)


def tillfalle(t: Handelse) -> str:
    return (
        f"<strong>{TILLFALLE[t.steg]} <time>{t.datum}</time></strong> {escape(t.text)} "
        f'<a href="{escape(t.lank)}">{escape(t.kalla)}</a>'
    )


def markering(arende: Arende, idag: date) -> str:
    poster = "".join(f"<li>{tillfalle(t)}</li>" for t in kommande(arende, idag))
    return f'<div class="paverka"><p>Tycka till</p><ul>{poster}</ul></div>' if poster else ""


def tycka_till_nu(arenden: list[Arende], idag: date, adress: Callable[[Arende], str]) -> str:
    par = sorted(((t, a) for a in arenden for t in kommande(a, idag)), key=lambda p: p[0].datum)
    rader = "".join(rad(t, a, adress(a)) for t, a in par)
    lista = f'<ol class="tillfallen">{rader}</ol>' if rader else "<p>Inga kända tillfällen.</p>"
    return f'<h2 id="tycka-till">Tycka till nu</h2>{INLEDNING}{lista}{forklaring()}'


def rad(t: Handelse, arende: Arende, adress: str) -> str:
    return (
        f'<li data-ort="{escape("|".join(arende.orter))}">{tillfalle(t)} · '
        f'<a href="{adress}#{arende.id}">{escape(arende.falt["rubrik"])}</a></li>'
    )


PBL = (
    "https://www.riksdagen.se/sv/dokument-och-lagar/dokument/svensk-forfattningssamling/"
    "plan-och-bygglag-2010900_sfs-2010-900/"
)
KALENDER = "https://github.com/moggleif/kommunhandlingar/blob/main/kalender/kungsbacka.csv"
LOKALPLAN = (
    "https://moggleif.github.io/kommunhandlingar/kungsbacka/fg/2026/2026-10-14/"
    "protokoll.html#sida-13"
)
STEGEN = (
    "<li><strong>Inför ett beslut</strong> i en nämnd, ett arbetsutskott, kommunstyrelsen "
    "eller fullmäktige, också om lokalbehov, handlingsplaner och initiativ: förslaget står i "
    "arbetsutskottets protokoll och i kallelsen till sammanträdet. Före sammanträdet går "
    "ledamöterna och partierna att nå med synpunkter. Ett datum märkt preliminärt är "
    "organets nästa sammanträde, innan kallelsen har kommit. "
    f'<a href="{KALENDER}">Kommunhandlingars kalender</a></li>'
    "<li><strong>Lokalbehov</strong>: nämndernas behov sammanställs i kommunens lokalplan, "
    f'som är en del av flerårsbudgeten. <a href="{LOKALPLAN}">FG protokoll § 102</a></li>'
    "<li><strong>Samråd</strong> om ett planprogram eller en detaljplan: kommunen samråder "
    "bland andra med sakägare, boende som berörs och enskilda med väsentligt intresse. "
    f'<a href="{PBL}">Plan- och bygglagen 5 kap. 11 §</a></li>'
    "<li><strong>Granskning</strong> av ett planförslag, minst två veckor och vid utökat "
    "förfarande tre: den som inte "
    "senast under granskningstiden har lämnat skriftliga synpunkter kan förlora rätten att "
    f'överklaga beslutet att anta planen. <a href="{PBL}">'
    "Plan- och bygglagen 5 kap. 18–19 §§</a></li>"
)


def forklaring() -> str:
    rubrik = "<summary>Så kan du påverka, steg för steg</summary>"
    return f"<details>{rubrik}<ul>{STEGEN}</ul></details>"
