"""Krav: K37 i KRAV.md. Test: tests/test_tidningar.py.

Skriver träffarna som en lista i ärendenas format för *I media och debatt*,
med orden som träffade efter, och säger vilka flöden som lästes och vilka
som inte gick att läsa.
"""

from tidningar.flode import Artikel
from tidningar.matcha import rad

INGA = "Inga nya träffar."


def rapport(
    traffar: list[tuple[Artikel, list[str]]], lasta: dict[str, int], fel: list[str]
) -> str:
    rader = [rad(a, f) for a, f in sorted(traffar, key=lambda t: t[0].datum, reverse=True)]
    delar = ["\n".join(rader) if rader else INGA, lasning(lasta, fel)]
    return "\n\n".join(delar) + "\n"


def lasning(lasta: dict[str, int], fel: list[str]) -> str:
    lista = ", ".join(f"{t} ({n} artiklar)" for t, n in lasta.items()) or "inga"
    text = f"Lästa flöden: {lista}."
    if fel:
        text += "\nGick inte att läsa: " + ", ".join(fel) + "."
    return text
