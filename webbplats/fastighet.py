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
FASTIGHET = re.compile(rf"(?<![\w-])({ORD} )?({ORD} \d+:\d+)(?![\d:])")


def med_kartlankar(text: str) -> str:
    return FASTIGHET.sub(kartlank, escape(text))


def kartlank(traff: re.Match[str]) -> str:
    framfor, beteckning = traff.groups()
    if framfor:
        return traff.group()
    adress = escape(KARTA.format(quote_plus(beteckning)))
    return f'<a href="{adress}">{beteckning}</a>'
