"""Krav: K28 i KRAV.md, beslut 0018. Test: tests/test_sokindex.py och tests/test_sokruta.js.

Giffås sökindex `sok.json`, i det format som alla projektets sajter skriver
sitt i (beslut 0018): grupper med poster, där varje post har det som visas
(`rubrik`, `adress` från indexets plats, `om`), det som söks i först
(`traff`) och texten (`text`), i små bokstäver. Ärendena har också orterna
och namnen i folkmun, och indexet föreningarnas orter, så att urvalet i
adressen gäller också här.
"""

import json

from webbplats.arende import Arende
from webbplats.datum import klartext
from webbplats.kallelsen import Motet, Punkten
from webbplats.ksmotet import SIDA as KS_MOTET
from webbplats.mall import Sajt
from webbplats.motespunkt import rubriken


def sokindex(sajt: Sajt, arenden: list[Arende], motet: Motet | None) -> str:
    grupper = [{"rubrik": "Ärenden", "poster": [arende(a) for a in arenden]}]
    if motet is not None and motet.punkter is not None:
        poster = [punkt(p) for p in motet.punkter]
        grupper.append({"rubrik": f"KS-mötet {klartext(motet.datum)}", "poster": poster})
    index = {"foreningar": sajt.foreningar, "grupper": grupper}
    return json.dumps(index, ensure_ascii=False, separators=(",", ":"))


def arende(a: Arende) -> dict:
    falt = a.falt
    traff = (falt["rubrik"], *a.orter, falt["organ"], falt.get("diarienummer", ""), *a.kallas)
    text = (a.ingress, *(p.text for p in a.forslaget), *(h.text for h in a.handelser + a.tillfallen))
    return {
        "rubrik": falt["rubrik"],
        "adress": a.sida,
        "om": [", ".join(a.orter), falt["status"]],
        "orter": a.orter,
        "kallas": list(a.kallas),
        "traff": sma(traff),
        "text": sma(text),
    }


def punkt(punkten: Punkten) -> dict:
    p = punkten.punkt
    nummer = punkten.numren[0]
    return {
        "rubrik": rubriken(punkten),
        "adress": f"{KS_MOTET}#punkt-{p.nummer}",
        "om": [f"Punkt {p.nummer}", *([f"Dnr {nummer}"] if nummer else [])],
        "traff": sma((rubriken(punkten), nummer)),
        "text": sma((*(p.forslag or ()), *punkten.sammanfattning)),
    }


def sma(delar: tuple[str, ...]) -> str:
    return " ".join(" ".join(d for d in delar if d).split()).lower()
