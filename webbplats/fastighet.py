"""Krav: K23 i KRAV.md. Test: tests/test_fastighet.py.

Gör varje fastighetsbeteckning i en text till en länk till Kungsbackas
karta (KALLOR.md) som söker fram just den fastigheten. Kartan hämtas
aldrig; bara adressen byggs. Ett ord med versal framför hör till trakten,
som i "Ölmevalla Hallen 1:17", utom när det inleder meningen. Följs
beteckningen av "AB" är den ett bolagsnamn och länkas inte.
"""

import re
from html import escape
from urllib.parse import quote_plus

KARTA = "https://karta.kungsbacka.se/publik/#m=publik&q={}"
ORD = r"[A-ZÅÄÖ][a-zåäöé]+(?:-[A-ZÅÄÖ][a-zåäöé]+)*"
NUMMER = r"\d+:\d+(?![\w:])"
FOLJD = rf"(?:(?:, | och | samt | eller |–| – |-){NUMMER})*"
FASTIGHET = re.compile(rf"(?<![\w-])((?:{ORD} )?{ORD}) ({NUMMER})({FOLJD})(?! AB\b)")


def med_kartlankar(text: str) -> str:
    return FASTIGHET.sub(kartlankar, escape(text))


def kartlankar(traff: re.Match[str]) -> str:
    inledning, trakt = "", traff.group(1)
    if " " in trakt and meningen_borjar(traff):
        inledning, trakt = trakt.split(" ")
        inledning += " "
    forsta, foljd = traff.group(2, 3)
    resten = re.sub(NUMMER, lambda n: lank(trakt, n.group(), n.group()), foljd)
    return inledning + lank(trakt, forsta, f"{trakt} {forsta}") + resten


def meningen_borjar(traff: re.Match[str]) -> bool:
    fore = traff.string[: traff.start()]
    return fore.rstrip() == "" or fore.endswith(". ")


def lank(trakt: str, nummer: str, text: str) -> str:
    adress = escape(KARTA.format(quote_plus(f"{trakt} {nummer}")))
    return f'<a href="{adress}">{text}</a>'
