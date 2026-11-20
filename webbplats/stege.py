"""Krav: K33 i KRAV.md. Test: tests/test_stege.py.

Processtegen för planerna: stegen en detaljplan eller ett planprogram går
igenom enligt plan- och bygglagen, vilka som är klara, var planen står nu
och vad som kommer härnäst, med färg, tecken och ord för varje läge. Bara
det som händelserna säger räknas: samråd och granskning på sitt steg,
antagandet och godkännandet på ett beslut som säger att planen antogs
eller godkändes, uppdraget på ett förslag eller beslut om uppdrag att
upprätta planen eller en godkänd projektbeställning. Ett steg före steget
nu utan egen händelse är passerat men inte klart, och ett kommande steg
utan tillfälle sägs inte komma. Kommer inget steg fram står läget som
okänt i stället för gissat. En plan som nått sitt sista steg är klar, och
då visas vad som händer i ärendet efter planen. Andra ärenden har ingen
fastslagen process och ingen stege.
"""

import re
from datetime import date
from html import escape
from typing import NamedTuple

from webbplats.arende import Arende, Handelse
from webbplats.datum import tid
from webbplats.paverka import PBL, kommande


class Steg(NamedTuple):
    namn: str
    handelse: tuple[str, str]
    tillfalle: tuple[str, str]


FATTAT = "beslut|vantas"
UPPDRAG = Steg(
    "Uppdrag",
    ("forslag|beslut", r"uppdrag att upprätta|bad \w+ upprätta|godkände projektbeställning"),
    (FATTAT, r"uppdraget att upprätta"),
)
SAMRAD = Steg("Samråd", ("samrad", ""), ("samrad", ""))
ANTAGANDE = Steg("Antagande", ("beslut", r"\b(antog|antagit)\b"), (FATTAT, r"^(?!.*föreslå att).*\banta[rs]? (detalj)?planen"))
GODKANNANDE = Steg("Godkännande", ("beslut", r"godkände planprogrammet"), (FATTAT, r"godkänn\w* planprogrammet"))
DETALJPLAN = (UPPDRAG, SAMRAD, Steg("Granskning", ("granskning", ""), ("granskning", "")), ANTAGANDE)
PLANPROGRAM = (UPPDRAG, SAMRAD, GODKANNANDE)
SLAG = (
    (r"(ändring av (del av )?|upphävande av (del av )?)?detaljplan", DETALJPLAN),
    (r"planprogram", PLANPROGRAM),
)
UPPHAVT = re.compile(r"upphäv\w* (antagandet|detaljplanen|planen|\w+ beslut att anta)")
FORFARANDE = f'<p class="forfarande"><a href="{PBL}">Stegen i plan- och bygglagen</a></p>'
TECKEN = {"gjord": "✓", "tidigare": "✓", "nu": "●", "nasta": "→", "kommande": "○", "okand": "○"}
ORD = {"gjord": "klart", "nu": "nu", "nasta": "nästa", "kommande": "kommer", "okand": "kommer"}
UTAN_DATUM = {"tidigare": "passerat", "nasta": "nästa, inget datum än", "kommande": "inget datum än"}
KLAR = {"Antagande": "antagen", "Godkännande": "godkänd"}
LAGA_KRAFT = re.compile(r"(fick|vann|fått|vunnit) laga kraft", re.IGNORECASE)


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
    klar = lagen[-1] == "nu" and not (upphavt and not borjat_om)
    if klar:
        lagen[-1] = "gjord"
    poster = "".join(post(s, l, nar(s, l, handelser, tillfallen)) for s, l in zip(stegen, lagen, strict=True))
    rubrik, sedan = ("Var planen står" + (": okänt" if nu is None else ""), "")
    if klar:
        rubrik, sedan = klar_plan(stegen[-1], handelser, tillfallen)
    noten = sedan + upphavd(upphavt, borjat_om) + FORFARANDE
    return f'<div class="stege"><p>{rubrik}</p><ol>{poster}</ol>{noten}</div>'


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
    if index == nu:
        return "nu"
    return "nasta" if index == nu + 1 else "kommande"


def nar(steget: Steg, lage_: str, handelser: list[Handelse], tillfallen: list[Handelse]) -> str:
    kommer = [t.datum for t in tillfallen if passar(steget.tillfalle, t)]
    if kommer and lage_ not in ("gjord", "tidigare"):
        return f"{ORD[lage_]}, {tid(kommer[0])}"
    if lage_ in ("gjord", "nu"):
        senast = max(h.datum for h in handelser if passar(steget.handelse, h))
        return f"{ORD[lage_]}, {tid(senast)}"
    return UTAN_DATUM.get(lage_, "")


def post(steget: Steg, lage_: str, text: str) -> str:
    return (
        f'<li class="{lage_}"><span aria-hidden="true">{TECKEN[lage_]}</span> '
        f"<strong>{escape(steget.namn)}</strong> <small>{text}</small></li>"
    )


def upphavd(upphavt: Handelse | None, borjat_om: bool) -> str:
    if not upphavt:
        return ""
    sedan = "det som hänt sedan dess" if borjat_om else "planen fram till upphävandet"
    return (
        f'<p class="forfarande">{tid(upphavt.datum)}: {escape(upphavt.text)} '
        f'<a href="{escape(upphavt.lank)}">{escape(upphavt.kalla)}</a> Stegen visar {sedan}.</p>'
    )


def klar_plan(sista: Steg, handelser: list[Handelse], tillfallen: list[Handelse]) -> tuple[str, str]:
    slut = max(h.datum for h in handelser if passar(sista.handelse, h))
    rubrik = f"Var planen står: {KLAR[sista.namn]}{laga_kraft(handelser, slut)}"
    return rubrik, efter_planen(handelser, slut, tillfallen)


def laga_kraft(handelser: list[Handelse], slut: date) -> str:
    traffar = [h.datum for h in handelser if h.datum >= slut and LAGA_KRAFT.search(h.text)]
    return f", laga kraft {tid(min(traffar))}" if traffar else ""


def efter_planen(handelser: list[Handelse], slut: date, tillfallen: list[Handelse]) -> str:
    senare = [h for h in handelser if h.datum > slut and not LAGA_KRAFT.search(h.text)]
    if tillfallen:
        rubrik, handelse = "Härnäst", tillfallen[0]
    elif senare:
        rubrik, handelse = "Senast", max(senare, key=lambda h: h.datum)
    else:
        return ""
    return (
        f'<p class="efter-planen"><strong>{rubrik}, {tid(handelse.datum)}:</strong> {escape(handelse.text)} '
        f'<a href="{escape(handelse.lank)}">{escape(handelse.kalla)}</a></p>'
    )
