"""Krav: K33 i KRAV.md. Test: tests/test_stege.py.

Processtegen för planerna: stegen en detaljplan eller ett planprogram går
igenom enligt plan- och bygglagen, vilka som är gjorda, var planen står nu
och vad som kommer, med spåret för varje steg (K30). Bara det som
händelserna säger räknas: samråd och granskning på sitt steg, antagandet
och godkännandet på ett beslut som säger att planen antogs eller
godkändes, uppdraget på ett förslag eller beslut om uppdrag att upprätta
planen. Ett steg före steget nu utan egen händelse sägs inte vara gjort,
och ett kommande steg utan tillfälle sägs inte komma. Kommer inget steg
fram står läget som okänt i stället för gissat. Andra ärenden har ingen fastslagen process och ingen stege.
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
    handelse: tuple[str, str]
    tillfalle: tuple[str, str]


FATTAT = "beslut|vantas"
UPPDRAG = Steg(
    "Uppdrag", "partiet", ("forslag|beslut", r"uppdrag att upprätta|bad \w+ upprätta"), (FATTAT, r"uppdraget att upprätta")
)
SAMRAD = Steg("Samråd", "alla", ("samrad", ""), ("samrad", ""))
ANTAGANDE = Steg(
    "Antagande", "partiet", ("beslut", r"\b(antog|antagit)\b"), (FATTAT, r"^(?!.*föreslå att).*\banta[rs]? (detalj)?planen")
)
GODKANNANDE = Steg(
    "Godkännande", "partiet", ("beslut", r"godkände planprogrammet"), (FATTAT, r"godkänn\w* planprogrammet")
)
DETALJPLAN = (UPPDRAG, SAMRAD, Steg("Granskning", "alla", ("granskning", ""), ("granskning", "")), ANTAGANDE)
PLANPROGRAM = (UPPDRAG, SAMRAD, GODKANNANDE)
SLAG = (
    (r"(ändring av (del av )?|upphävande av (del av )?)?detaljplan", DETALJPLAN),
    (r"planprogram", PLANPROGRAM),
)
UPPHAVT = re.compile(r"upphäv\w* (antagandet|detaljplanen|planen|\w+ beslut att anta)")
OKAND = '<p class="forfarande">Var planen står går inte att läsa ut ur händelserna.</p>'
FORFARANDE = (
    '<p class="forfarande">Stegen följer plan- och bygglagens standardförfarande; vid '
    f'begränsat förfarande blir det ingen granskning. <a href="{PBL}">Plan- och bygglagen 5 kap.</a></p>'
)


def stege(arende: Arende, idag: date) -> str:
    if arende.falt["status"] != "pågår" or not (stegen := steg_for(arende)):
        return ""
    upphavt = upphavande(arende)
    efter = [h for h in arende.handelser if upphavt and h.datum > upphavt.datum]
    borjat_om = steget_nu(efter, stegen) is not None
    handelser = efter if borjat_om else arende.handelser
    nu = steget_nu(handelser, stegen)
    tillfallen = kommande(arende, idag)
    lagen = [lage(i, nu, s, handelser) for i, s in enumerate(stegen)]
    poster = "".join(post(s, l, nar(s, l, handelser, tillfallen)) for s, l in zip(stegen, lagen, strict=True))
    noten = (OKAND if nu is None else "") + upphavd(upphavt, borjat_om) + FORFARANDE
    return f'<div class="stege"><p>Var planen står</p><ol>{poster}</ol>{noten}</div>'


def steg_for(arende: Arende) -> tuple[Steg, ...]:
    rubrik = arende.falt["rubrik"].lower()
    return next((stegen for monster, stegen in SLAG if re.match(monster, rubrik)), ())


def upphavande(arende: Arende) -> Handelse | None:
    traffar = [h for h in arende.handelser if h.steg == "info" and UPPHAVT.search(h.text)]
    return min(traffar, key=lambda h: h.datum) if traffar else None


def passar(villkor: tuple[str, str], handelse: Handelse) -> bool:
    steg, monster = villkor
    if not steg or not re.fullmatch(steg, handelse.steg):
        return False
    return re.search(monster, handelse.text, re.IGNORECASE) is not None


def steget_nu(handelser: list[Handelse], stegen: tuple[Steg, ...]) -> int | None:
    senaste = [(h.datum, i) for i, s in enumerate(stegen) for h in handelser if passar(s.handelse, h)]
    return max(senaste)[1] if senaste else None


def lage(index: int, nu: int | None, steget: Steg, handelser: list[Handelse]) -> str:
    if nu is None:
        return "okand"
    if index < nu:
        return "gjord" if any(passar(steget.handelse, h) for h in handelser) else "tidigare"
    return "nu" if index == nu else "kommande"


def nar(steget: Steg, lage_: str, handelser: list[Handelse], tillfallen: list[Handelse]) -> str:
    kommer = [t.datum for t in tillfallen if passar(steget.tillfalle, t)]
    if kommer and lage_ != "gjord":
        return f"{'nu' if lage_ == 'nu' else 'kommer'}, {tid(kommer[0])}"
    if lage_ in ("gjord", "nu"):
        senast = max(h.datum for h in handelser if passar(steget.handelse, h))
        return f"{'gjort' if lage_ == 'gjord' else 'nu'}, {tid(senast)}"
    return {"tidigare": "ingen händelse i källorna", "kommande": "inget i källorna än"}.get(lage_, "")


def post(steget: Steg, lage_: str, text: str) -> str:
    return (
        f'<li class="{lage_} {steget.spar}">{tecken(steget.spar)}<strong>{escape(steget.namn)}</strong> '
        f"<small>{text}</small></li>"
    )


def upphavd(upphavt: Handelse | None, borjat_om: bool) -> str:
    if not upphavt:
        return ""
    sedan = "det som hänt sedan dess" if borjat_om else "planen fram till upphävandet"
    return (
        f'<p class="forfarande">{tid(upphavt.datum)}: {escape(upphavt.text)} '
        f'<a href="{escape(upphavt.lank)}">{escape(upphavt.kalla)}</a> Stegen visar {sedan}.</p>'
    )
