"""Krav: K33 i KRAV.md. Test: tests/test_stege.py.

Processtegen: stegen ett pågående ärende av sitt slag går igenom, vilka som
är gjorda, var det står nu och vad som kommer, med spåret för varje steg
(K30). Stegen läses ur händelserna och tillfällena att tycka till. Antagandet
är ett beslut vars text säger att planen antogs, så att andra beslut i
ärendet, som exploateringsavtal, inte räknas; ett kommande steg utan
tillfälle står som inte känt än. Steget nu är det med den senaste
händelsen, så att en plan som börjat om efter ett upphävt antagande står
på sitt nya steg.
"""

import re
from datetime import date
from html import escape

from webbplats.arende import Arende
from webbplats.datum import tid
from webbplats.paverka import PBL, kommande
from webbplats.spar import tecken

FATTAT = ("beslut", "vantas")
DETALJPLAN = (
    ("Uppdrag", "partiet", (), (), ""),
    ("Samråd", "alla", ("samrad",), ("samrad",), ""),
    ("Granskning", "alla", ("granskning",), ("granskning",), ""),
    ("Antagande", "partiet", ("beslut",), FATTAT, r"\bantog\b|\bantagit\b"),
)
PLANPROGRAM = (
    DETALJPLAN[0],
    DETALJPLAN[1],
    ("Godkännande", "partiet", ("beslut",), FATTAT, r"\bgodkände planprogrammet\b"),
)
OVRIGT = (
    ("Information", "partiet", (), (), ""),
    ("Förslag", "partiet", ("forslag", "yttrande", "beslut"), ("yttrande",), ""),
    ("Beslut", "partiet", (), FATTAT, ""),
)
SLAG = (("Detaljplan", DETALJPLAN), ("Planprogram", PLANPROGRAM))
FORFARANDE = (
    '<p class="forfarande">Stegen följer plan- och bygglagens standardförfarande; vid '
    f'begränsat förfarande blir det ingen granskning. <a href="{PBL}">Plan- och bygglagen 5 kap.</a></p>'
)
LAGE = {-1: "gjord", 0: "nu", 1: "kommande"}
ORD = {"gjord": "gjort", "nu": "nu", "kommande": "kommer"}


def stege(arende: Arende, idag: date) -> str:
    if arende.falt["status"] != "pågår":
        return ""
    stegen = steg_for(arende)
    nu = nadd(arende, stegen)
    poster = "".join(post(arende, s, LAGE[(i > nu) - (i < nu)], idag) for i, s in enumerate(stegen))
    noten = FORFARANDE if stegen is not OVRIGT else ""
    return f'<div class="stege"><p>Var ärendet står</p><ol>{poster}</ol>{noten}</div>'


def steg_for(arende: Arende) -> tuple:
    rubrik = arende.falt["rubrik"]
    return next((stegen for borjan, stegen in SLAG if rubrik.startswith(borjan)), OVRIGT)


def nadd(arende: Arende, stegen: tuple) -> int:
    senaste = [(max(d), i) for i, s in enumerate(stegen) if (d := traffar(arende, s))]
    return max(senaste)[1] if senaste else 0


def traffar(arende: Arende, steget: tuple) -> list[date]:
    _, _, handelser, _, ord_ = steget
    return [h.datum for h in arende.handelser if h.steg in handelser and re.search(ord_, h.text)]


def post(arende: Arende, steget: tuple, lage: str, idag: date) -> str:
    namn, spar, _, tillfallen, _ = steget
    nar = nasta(arende, tillfallen, idag) if lage != "gjord" else ""
    nar = nar or (senast(arende, steget) if lage != "kommande" else "datum inte känt än")
    return (
        f'<li class="{lage} {spar}">{tecken(spar)}<strong>{escape(namn)}</strong> '
        f"<small>{ORD[lage]}{', ' + nar if nar else ''}</small></li>"
    )


def senast(arende: Arende, steget: tuple) -> str:
    if not steget[2]:
        return tid(arende.handelser[-1].datum)
    datum = traffar(arende, steget)
    return tid(max(datum)) if datum else ""


def nasta(arende: Arende, tillfallen: tuple[str, ...], idag: date) -> str:
    datum = [t.datum for t in kommande(arende, idag) if t.steg in tillfallen]
    return tid(datum[0]) if datum else ""
