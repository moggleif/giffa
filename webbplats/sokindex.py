"""Krav: K28 i KRAV.md, beslut 0018. Test: tests/test_sokindex.py och tests/test_sokning.js.

Sökindexet `sok.json` som knappen Sök (docs/sokruta.js) hämtar: för varje
ärende det som visas i träfflistan, det som söks i först (`traff`) och
texten (`text`), i små bokstäver; punkterna på KS-mötet på samma sätt;
och föreningarnas orter, så att urvalet i adressen gäller också här.
"""

import json

from webbplats.arende import Arende
from webbplats.datum import klartext
from webbplats.kallelsen import Motet, Punkten
from webbplats.ksmotet import SIDA as KS_MOTET
from webbplats.mall import Sajt
from webbplats.motespunkt import rubriken


def sokindex(sajt: Sajt, arenden: list[Arende], motet: Motet | None) -> str:
    index = {
        "foreningar": sajt.foreningar,
        "arenden": [arende(a) for a in arenden],
        "motet": motesposter(motet),
    }
    return json.dumps(index, ensure_ascii=False, separators=(",", ":"))


def arende(a: Arende) -> dict:
    falt = a.falt
    traff = (falt["rubrik"], *a.orter, falt["organ"], falt.get("diarienummer", ""), *a.kallas)
    text = (a.ingress, *(p.text for p in a.forslaget), *(h.text for h in a.handelser + a.tillfallen))
    return {
        "rubrik": falt["rubrik"],
        "adress": a.sida,
        "orter": a.orter,
        "status": falt["status"],
        "kallas": list(a.kallas),
        "traff": sma(traff),
        "text": sma(text),
    }


def motesposter(motet: Motet | None) -> dict | None:
    if motet is None or motet.punkter is None:
        return None
    return {
        "rubrik": f"KS-mötet {klartext(motet.datum)}",
        "punkter": [punkt(p) for p in motet.punkter],
    }


def punkt(punkten: Punkten) -> dict:
    p = punkten.punkt
    return {
        "rubrik": rubriken(punkten),
        "adress": f"{KS_MOTET}#punkt-{p.nummer}",
        "nummer": p.nummer,
        "dnr": punkten.numren[0],
        "traff": sma((rubriken(punkten), punkten.numren[0])),
        "text": sma((*(p.forslag or ()), *punkten.sammanfattning)),
    }


def sma(delar: tuple[str, ...]) -> str:
    return " ".join(" ".join(d for d in delar if d).split()).lower()
