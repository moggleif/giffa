"""Krav: K37 i KRAV.md. Test: tests/test_tidningar.py.

python3 -m tidningar [redan.txt]

Körs från repots rot, läser flödena i tidningar/floden.csv och skriver
artiklarna som inget ärende länkar till stdout. Länkar som står i
redan.txt, veckans och förra veckans issue, tas inte med igen. Ett
flöde som inte går att hämta eller tolka står i rapporten.
"""

import csv
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

from tidningar.flode import Artikel, artiklar
from tidningar.hamta import hamta
from tidningar.matcha import termer, traffar
from tidningar.rapport import rapport


def las(namn: str) -> str:
    return Path(namn).read_text(encoding="utf-8")


def floden() -> tuple[list[Artikel], dict[str, int], list[str]]:
    alla, lasta, fel = [], {}, []
    for rad in csv.DictReader(las("tidningar/floden.csv").splitlines()):
        try:
            nya = artiklar(rad["tidning"], hamta(rad["adress"]))
        except (OSError, ValueError, ET.ParseError) as orsak:
            fel.append(f"{rad['tidning']} ({orsak})")
            continue
        alla += nya
        lasta[rad["tidning"]] = len(nya)
    return alla, lasta, fel


def lankade(redan: str) -> str:
    filer = sorted(Path("bevakning").glob("*/*.md"))
    return redan + "".join(fil.read_text(encoding="utf-8") for fil in filer)


alla, lasta, fel = floden()
sokta = termer(las("OMRADE.md"), las("platser.csv"), las("bevakning/uppmarksammade.csv"))
redan = las(sys.argv[1]) if len(sys.argv) > 1 else ""
print(rapport(traffar(alla, sokta, lankade(redan)), lasta, fel), end="")
