"""Krav: K11 i KRAV.md. Test: tests/test_skanning.py.

Söktermerna: orterna ur OMRADE.md, platsernas namn ur platser.csv och
diarienumren i de ärenden som inte är avslutade.
"""

import re
from pathlib import Path

from webbplats import underlag
from webbplats.arende import tolka

AVSLUTADE = ("klart", "avbrutet")


def termer(rot: Path) -> dict[str, list[str]]:
    return {
        "orter": underlag.orter(las(rot, "OMRADE.md")),
        "platser": [p["namn"] for p in underlag.platser(las(rot, "platser.csv"))],
        "diarienummer": diarienummer(rot),
    }


def las(rot: Path, namn: str) -> str:
    return (rot / namn).read_text(encoding="utf-8")


def diarienummer(rot: Path) -> list[str]:
    arenden = [
        tolka(fil.name, fil.read_text(encoding="utf-8"))
        for fil in sorted(rot.glob("bevakning/*/*.md"))
    ]
    return [
        a.falt["diarienummer"]
        for a in arenden
        if "diarienummer" in a.falt and a.falt["status"] not in AVSLUTADE
    ]


def monster(term: str) -> re.Pattern[str]:
    return re.compile(rf"(?<!\w){re.escape(term)}(?!\w)")
