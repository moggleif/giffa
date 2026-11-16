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
from webbplats.punktkoppling import Kopplad

POOL = "https://moggleif.github.io/kungsbackakommun/kungsbacka"
FORSLAG = "Förslag till beslut"


def rubriken(punkten: Punkten) -> str:
    return punkten.punkt.rubrik or "Rubriken gick inte att läsa ur kallelsen"


def punktkort(sajt: Sajt, motet: Motet, k: Kopplad) -> str:
    punkt = k.punkten.punkt
    return (
        f'<article id="punkt-{punkt.nummer}">{markor(k)}'
        f"<h3>{sajt.karta.lanka(rubriken(k.punkten))}</h3>"
        + diarienumret(k.punkten)
        + forslag(sajt, punkt.forslag)
        + sammanfattning(k.punkten)
        + kallrad(motet, k.punkten)
        + i_giffa(sajt, k)
        + "</article>"
    )


def diarienumret(punkten: Punkten) -> str:
    nummer = punkten.numren[0]
    return f'<p class="organ">{f"Dnr {escape(nummer)}" if nummer else "Dnr saknas i kallelsen"}</p>'


# Orterna punkten berör: de som rubriken eller förslaget nämner, själva
# eller genom en plats, sedan sökorden och för sig de orter som bara
# handlingen nämner.
def markor(k: Kopplad) -> str:
    i_kallelsen = list(dict.fromkeys(t.ort for t in k.traffar if not t.i_handlingen))
    bara = [o for o in dict.fromkeys(t.ort for t in k.traffar) if o not in i_kallelsen]
    orter = "".join(f"<span>{escape(o)}</span>" for o in i_kallelsen)
    orter += "".join(f'<span class="sokord">{escape(o)}</span>' for o in k.sokord)
    if bara:
        orter += "<small>i handlingen:</small>" + "".join(
            f'<span class="svag">{escape(o)}</span>' for o in bara
        )
    nummer = f'<span class="nummer">Punkt {k.punkten.punkt.nummer}</span>'
    return f'<p class="markor">{nummer}{orter}</p>'


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
    historik = f'<a href="{bas}.html#punkt-{punkten.punkt.nummer}">Fullständig historik</a>'
    if not omfang:
        return f"<p>Ingen egen handling hittad för punkten · {historik}</p>"
    sidorna = (
        f"sidan {omfang.start}" if len(omfang) == 1 else f"sidorna {omfang.start}–{omfang[-1]}"
    )
    handling = f'<a href="{bas}/handlingar.html#sida-{omfang.start}">Handlingen, {sidorna}</a>'
    return f"<p>{handling} · {historik}</p>"


def i_giffa(sajt: Sajt, k: Kopplad) -> str:
    egna = "".join(foljs(sajt, a, "Följs i Giffå") for a in k.egna)
    osakra = "".join(
        foljs(sajt, a, "Följs kanske i Giffå, samma nummer utan förled") for a in k.osakra
    )
    namnda = "".join(f"<p>Handlingen nämner ett nummer i {lank(a)}</p>" for a in k.namnda)
    return egna + osakra + namnda


def foljs(sajt: Sajt, arende: Arende, inledning: str) -> str:
    poster = "".join(post(h, sajt.karta) for h in arende.handelser)
    antal = len(arende.handelser)
    return (
        f"<p>{inledning}: {lank(arende)}</p>"
        f"<details><summary>Historik i Giffå, {antal} {'händelse' if antal == 1 else 'händelser'}"
        f"</summary><ol>{poster}</ol></details>"
    )


def lank(arende: Arende) -> str:
    return f'<a href="{arende.sida}">{escape(arende.falt["rubrik"])}</a>'
