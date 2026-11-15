"""Krav: K34 i KRAV.md, beslut 0012. Test: tests/test_ksmotet.py.

En punkt på kommunstyrelsens kommande sammanträde som ett kort: numret,
orterna och platserna, rubriken, diarienumret, förslaget ur kallelsen,
sammanfattningen ur tjänsteskrivelsen, handlingens sidor, historiken i
datapoolen och ärendena i Giffå med samma diarienummer.
"""

from html import escape

from webbplats.arende import Arende
from webbplats.kallelsen import Motet, Punkten
from webbplats.kort import post
from webbplats.mall import Sajt
from webbplats.punktkoppling import Kopplad, Traff

POOL = "https://moggleif.github.io/kommunhandlingar/kungsbacka"
FORSLAG = "Förslag till beslut"


def rubriken(punkten: Punkten) -> str:
    return punkten.punkt.rubrik or "Rubriken gick inte att läsa ur kallelsen"


def punktkort(sajt: Sajt, motet: Motet, k: Kopplad) -> str:
    punkt = k.punkten.punkt
    return (
        f'<article id="punkt-{punkt.nummer}">{markor(k)}'
        f"<h3>{sajt.karta.lanka(rubriken(k.punkten))}</h3>"
        f'<p class="organ">Dnr {escape(k.punkten.numren[0])}</p>'
        + i_handlingen(k)
        + forslag(sajt, punkt.forslag)
        + sammanfattning(k.punkten)
        + kallrad(motet, k.punkten)
        + i_giffa(sajt, k)
        + "</article>"
    )


def markor(k: Kopplad) -> str:
    namn = dict.fromkeys(namnet(t) for t in k.traffar if not t.i_handlingen)
    orter = "".join(f"<span>{escape(n)}</span>" for n in namn)
    return f'<p class="markor"><span>Punkt {k.punkten.punkt.nummer}</span>{orter}</p>'


def i_handlingen(k: Kopplad) -> str:
    namn = list(dict.fromkeys(namnet(t) for t in k.traffar if t.i_handlingen))
    return f'<p class="organ">I handlingen: {escape(", ".join(namn))}</p>' if namn else ""


def namnet(t: Traff) -> str:
    return t.ort if t.namn == t.ort else f"{t.namn}, {t.ort}"


def forslag(sajt: Sajt, stycken: tuple[str, ...] | None) -> str:
    if stycken is None:
        return "<p>Förslaget gick inte att läsa ur kallelsen.</p>"
    if not stycken:
        return "<p>Inget förslag till beslut i kallelsen.</p>"
    return "".join(
        f"<h4>{escape(s)}</h4>"
        if s.startswith(FORSLAG)
        else f"<blockquote>{sajt.karta.lanka(s)}</blockquote>"
        for s in stycken
    )


def sammanfattning(punkten: Punkten) -> str:
    if not punkten.handling:
        return ""
    if not punkten.sammanfattning:
        return "<p>Ingen sammanfattning av ärendet i handlingen.</p>"
    text = "".join(f"<p>{escape(s)}</p>" for s in punkten.sammanfattning)
    return f"<details><summary>Sammanfattning ur tjänsteskrivelsen</summary>{text}</details>"


def kallrad(motet: Motet, punkten: Punkten) -> str:
    bas, omfang = f"{POOL}/{motet.katalog}", punkten.handling
    historik = f'<a href="{bas}.html#punkt-{punkten.punkt.nummer}">Historik i alla organ</a>'
    if not omfang:
        return f"<p>Ingen egen handling hittad för punkten · {historik}</p>"
    sidorna = (
        f"sidan {omfang.start}" if len(omfang) == 1 else f"sidorna {omfang.start}–{omfang[-1]}"
    )
    handling = f'<a href="{bas}/handlingar.html#sida-{omfang.start}">Handlingen, {sidorna}</a>'
    return f"<p>{handling} · {historik}</p>"


def i_giffa(sajt: Sajt, k: Kopplad) -> str:
    egna = "".join(foljs(sajt, a) for a in k.egna)
    namnda = "".join(
        f'<p>Handlingen nämner ett nummer i <a href="{a.sida}">{escape(a.falt["rubrik"])}</a></p>'
        for a in k.namnda
    )
    return egna + namnda


def foljs(sajt: Sajt, arende: Arende) -> str:
    poster = "".join(post(h, sajt.karta) for h in arende.handelser)
    return (
        f'<p>Följs i Giffå: <a href="{arende.sida}">{escape(arende.falt["rubrik"])}</a></p>'
        f"<details><summary>Historik i Giffå, {len(arende.handelser)} händelser</summary>"
        f"<ol>{poster}</ol></details>"
    )
