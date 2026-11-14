"""Krav: K33 i KRAV.md. Test: tests/test_stege.py.

Processtegen: stegen ett pågående ärende av sitt slag går igenom, vilka som
är gjorda, var det står nu och vad som kommer, med spåret för varje steg
(K30). Ett steg känns igen på händelsens eller tillfällets steg och, där
steget delas med annat, på orden i texten: ett antagande är ett beslut som
säger att planen antas, inte ett exploateringsavtal. Steget nu är det med
den senaste händelsen, och ett antagande som har upphävts räknas inte; det
som hänt sedan dess räknas om något av det är ett steg, annars planen
fram till upphävandet, och noten säger vilket. Ett upphävande är en
information om att en domstol eller länsstyrelsen upphävt antagandet. Det som inte går att
läsa ut står som okänt.
"""

import re
from datetime import date
from html import escape
from typing import NamedTuple

from webbplats.arende import Arende, Handelse
from webbplats.datum import tid
from webbplats.paverka import PBL, kommande
from webbplats.spar import tecken


class Steg(NamedTuple):
    namn: str
    spar: str
    handelser: tuple[str, ...]
    tillfallen: tuple[str, ...]
    monster: str = ""


FATTAT = ("beslut", "vantas")
UPPDRAG = Steg("Uppdrag", "partiet", ("forslag", "beslut"), FATTAT, r"uppdrag|projektbeställning|återuppta")
SAMRAD = Steg("Samråd", "alla", ("samrad",), ("samrad",))
DETALJPLAN = (
    UPPDRAG,
    SAMRAD,
    Steg("Granskning", "alla", ("granskning",), ("granskning",)),
    Steg("Antagande", "partiet", FATTAT, FATTAT, r"\bant(a|ar|as|og|ogs|agit|agande[nt]?)\b"),
)
PLANPROGRAM = (UPPDRAG, SAMRAD, Steg("Godkännande", "partiet", FATTAT, FATTAT, r"godkän\w* planprogram"))
OVRIGT = (
    Steg("Beredning", "partiet", ("info", "forslag", "yttrande", "beslut"), ("yttrande",)),
    Steg("Beslut", "partiet", (), FATTAT),
)
SLAG = (
    (r"(ändring av (del av )?|upphävande av (del av )?)?detaljplan", DETALJPLAN),
    (r"planprogram", PLANPROGRAM),
)
UPPHAVT = re.compile(r"upphäv\w* (antagandet|detaljplanen|planen|\w+ beslut att anta)")
ORD = {"gjord": "gjort", "nu": "nu", "kommande": "kommer"}
FORFARANDE = (
    '<p class="forfarande">Stegen följer plan- och bygglagens standardförfarande; vid '
    f'begränsat förfarande blir det ingen granskning. <a href="{PBL}">Plan- och bygglagen 5 kap.</a></p>'
)


def stege(arende: Arende, idag: date) -> str:
    if arende.falt["status"] != "pågår":
        return ""
    stegen = steg_for(arende)
    upphavt = upphavande(arende) if stegen is not OVRIGT else None
    efter = [h for h in arende.handelser if upphavt and h.datum > upphavt.datum]
    borjat_om = steget_nu(efter, stegen) is not None
    handelser = efter if borjat_om else arende.handelser
    nu = steget_nu(handelser, stegen) or 0
    tillfallen = kommande(arende, idag)
    poster = "".join(
        post(s, lage(i, nu), nar(s, lage(i, nu), handelser, tillfallen)) for i, s in enumerate(stegen)
    )
    return f'<div class="stege"><p>Var ärendet står</p><ol>{poster}</ol>{noter(stegen, upphavt, borjat_om)}</div>'


def steg_for(arende: Arende) -> tuple[Steg, ...]:
    rubrik = arende.falt["rubrik"].lower()
    return next((stegen for monster, stegen in SLAG if re.match(monster, rubrik)), OVRIGT)


def upphavande(arende: Arende) -> Handelse | None:
    return next((h for h in arende.handelser if h.steg == "info" and UPPHAVT.search(h.text)), None)


def passar(steget: Steg, steg: str, text: str, tillfalle: bool) -> bool:
    stegen = steget.tillfallen if tillfalle else steget.handelser
    return steg in stegen and bool(re.search(steget.monster, text, re.IGNORECASE))


def steget_nu(handelser: list[Handelse], stegen: tuple[Steg, ...]) -> int | None:
    senaste = [
        (h.datum, i) for i, s in enumerate(stegen) for h in handelser if passar(s, h.steg, h.text, False)
    ]
    return max(senaste)[1] if senaste else None


def lage(index: int, nu: int) -> str:
    if index < nu:
        return "gjord"
    return "nu" if index == nu else "kommande"


def nar(steget: Steg, lage_: str, handelser: list[Handelse], tillfallen: list[Handelse]) -> str:
    kommer = [t.datum for t in tillfallen if passar(steget, t.steg, t.text, True)]
    if kommer and lage_ != "gjord":
        return tid(kommer[0])
    if lage_ == "kommande":
        return "datum inte känt än"
    gjort = [h.datum for h in handelser if passar(steget, h.steg, h.text, False)]
    return tid(max(gjort)) if gjort else "inget datum i källorna"


def post(steget: Steg, lage_: str, datum: str) -> str:
    return (
        f'<li class="{lage_} {steget.spar}">{tecken(steget.spar)}<strong>{escape(steget.namn)}</strong> '
        f"<small>{ORD[lage_]}, {datum}</small></li>"
    )


def noter(stegen: tuple[Steg, ...], upphavt: Handelse | None, borjat_om: bool) -> str:
    if stegen is OVRIGT:
        return ""
    if not upphavt:
        return FORFARANDE
    sedan = "det som hänt sedan dess" if borjat_om else "planen fram till upphävandet"
    return (
        f'<p class="forfarande">{tid(upphavt.datum)}: {escape(upphavt.text)} '
        f'<a href="{escape(upphavt.lank)}">{escape(upphavt.kalla)}</a> Stegen visar {sedan}.</p>'
        + FORFARANDE
    )
