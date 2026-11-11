"""Krav: K23 i KRAV.md. Test: tests/test_fastighet.py.

Gör varje fastighetsbeteckning i en text till en länk till Kungsbackas
karta (KALLOR.md) som söker fram just den fastigheten. Kartan hämtas
aldrig; bara adressen byggs. Står ett ord med versal framför, som i
"Ölmevalla Berg 1:2", kan trakten ha två ord, och då länkas inget hellre
än fel fastighet.
"""

import re
from html import escape
from urllib.parse import quote_plus

KARTA = "https://karta.kungsbacka.se/publik/#m=publik&q={}"
ORD = r"[A-ZÅÄÖ][a-zåäöé]+(?:-[A-ZÅÄÖ][a-zåäöé]+)*"
NUMMER = r"\d+:\d+(?![\d:])"
FOLJD = rf"(?:(?:, | och | samt | eller |–| – |-){NUMMER})*"
FASTIGHET = re.compile(rf"(?<![\w-])({ORD} )?({ORD}) ({NUMMER})({FOLJD})")


def med_kartlankar(text: str) -> str:
    return FASTIGHET.sub(kartlankar, escape(text))


def kartlankar(traff: re.Match[str]) -> str:
    framfor, trakt, forsta, foljd = traff.groups()
    if framfor:
        return traff.group()
    resten = re.sub(NUMMER, lambda n: lank(trakt, n.group(), n.group()), foljd)
    return lank(trakt, forsta, f"{trakt} {forsta}") + resten


def lank(trakt: str, nummer: str, text: str) -> str:
    adress = escape(KARTA.format(quote_plus(f"{trakt} {nummer}")))
    return f'<a href="{adress}">{text}</a>'
