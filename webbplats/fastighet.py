"""Krav: K23 i KRAV.md. Test: tests/test_karta.py.

En fastighetsbeteckning som länk till kartan. Ett ord med versal framför
hör till trakten, som i "Ölmevalla Hallen 1:17", utom när det inleder
meningen. Följs beteckningen av "AB" är den ett bolagsnamn och länkas inte.
I en uppräkning får varje nummer trakten från den första beteckningen.
"""

import re

from webbplats.karta import lank

ORD = r"[A-ZÅÄÖ][a-zåäöé]+(?:-[A-ZÅÄÖ][a-zåäöé]+)*"
NUMMER = r"\d+:\d+(?![\w:])"
FOLJD = rf"(?:(?:, | och | samt | eller |–| – |-){NUMMER})*"
FASTIGHET = (
    rf"(?<![\w-])(?P<trakt>(?:{ORD} )?{ORD}) (?P<forsta>{NUMMER})(?P<foljd>{FOLJD})(?! AB\b)"
)


def fastighet(traff: re.Match[str]) -> str:
    inledning, trakt = "", traff.group("trakt")
    if " " in trakt and meningen_borjar(traff):
        inledning, trakt = trakt.split(" ")
        inledning += " "
    forsta, foljd = traff.group("forsta", "foljd")
    resten = re.sub(NUMMER, lambda n: lank(f"{trakt} {n.group()}", n.group()), foljd)
    return inledning + lank(f"{trakt} {forsta}", f"{trakt} {forsta}") + resten


def meningen_borjar(traff: re.Match[str]) -> bool:
    fore = traff.string[: traff.start()]
    return fore.rstrip() == "" or fore.endswith(". ")
