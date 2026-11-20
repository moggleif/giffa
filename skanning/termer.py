"""Krav: K11 i KRAV.md. Test: tests/test_skanning.py.

Söktermerna: orterna ur OMRADE.md, platsernas namn ur platser.csv,
diarienumren i de ärenden som inte är avslutade och, i regionens
handlingar, kommunens namn (K39). Ett mellanslag i en term
matchar också radbrott, och ett diarienummer skrivet med mellanslag efter
prefixet (BN 2024-00196) räknas.
"""

import re
from pathlib import Path

from webbplats import underlag
from webbplats.arende import tolka

AVSLUTADE = ("klart", "avbrutet")


def termer(rot: Path, kommunnamn: tuple[str, ...] = ()) -> dict[str, list[str]]:
    grupper = {
        "orter": underlag.orter(las(rot, "OMRADE.md")),
        "platsnamn": [p["namn"] for p in underlag.platser(las(rot, "platser.csv"))],
        "diarienummer": diarienummer(rot),
    }
    return grupper | ({"kommunnamn": list(kommunnamn)} if kommunnamn else {})


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
    text = re.escape(term).replace(r"\ ", r"\s+")
    text = re.sub(r"^([A-ZÅÄÖ]+)\\-(?=\d{4})", r"\1[-\\s]", text)
    return re.compile(rf"(?<!\w){text}(?!\w)")
