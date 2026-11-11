"""Krav: K23 i KRAV.md. Test: tests/test_fastighet.py.

Gör varje fastighetsbeteckning i en text till en länk till Kungsbackas
karta (KALLOR.md) som söker fram just den fastigheten. Kartan hämtas
aldrig; bara adressen byggs.
"""

import re
from html import escape
from urllib.parse import quote

KARTA = "https://karta.kungsbacka.se/publik/?fastighet={}"
TRAKT = r"[A-ZÅÄÖ][a-zåäöé]+(?:-[A-ZÅÄÖ][a-zåäöé]+)*"
FASTIGHET = re.compile(rf"(?<![\w-]){TRAKT} \d+:\d+(?![\d:])")


def med_kartlankar(text: str) -> str:
    return FASTIGHET.sub(kartlank, escape(text))


def kartlank(traff: re.Match[str]) -> str:
    beteckning = traff.group()
    adress = KARTA.format(quote(beteckning))
    return f'<a class="fastighet" href="{adress}">{beteckning}</a>'
