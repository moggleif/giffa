"""Krav: K37 i KRAV.md. Test: tests/test_tidningar.py.

Väljer ut artiklarna som nämner en ort, en plats eller ett uppmärksammat
namn och samtidigt något kommunen beslutar om, och som varken ett ärende
eller veckans issue redan länkar. Orden om kommunens beslut gäller alla
orter och står därför här; de matchar som början av ett ord, och ord som
finns i nästan varje artikel, som *Halland* och *kommunen*, är inte med.
"""

import csv
import re
from io import StringIO

from skanning.termer import monster
from tidningar.flode import Artikel
from webbplats import underlag

AMNEN = re.compile(
    r"(?<!\w)(detaljplan|planprogram|planer|bygg|bostä|bostad|skol|förskol"
    r"|boende|väg|cykel|station|tåg|dagvatten|översvämn|skyfall|kommunstyrelse"
    r"|fullmäktige|politik|nämnd|beslut|samråd|överklag|park|idrott|sporthall"
    r"|idrottshall|arena|lokal|centrum|tomt)",
    re.IGNORECASE,
)


def termer(omrade: str, platser: str, uppmarksammade: str) -> list[str]:
    alla = (
        underlag.orter(omrade)
        + [plats["namn"] for plats in underlag.platser(platser)]
        + [rad["namn"] for rad in csv.DictReader(StringIO(uppmarksammade))]
    )
    return list(dict.fromkeys(alla))


def traffar(
    artiklar: list[Artikel], termer: list[str], kanda: str
) -> list[tuple[Artikel, list[str]]]:
    return [
        (artikel, funna)
        for artikel in artiklar
        if artikel.lank not in kanda
        and AMNEN.search(artikel.text)
        and (funna := [t for t in termer if monster(t).search(artikel.text)])
    ]

