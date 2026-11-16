"""Krav: K37 i KRAV.md. Test: tests/test_tidningar.py.

Skriver träffarna i ärendenas format för *I media och debatt*, med orden
som träffade på en egen rad under, och säger vilka flöden som lästes och
vilka som inte gick att läsa. Rapporten börjar med INGA bara när det inte
finns något att föra in: inga träffar och inga flöden som fallerade.
"""

from tidningar.flode import Artikel

INGA = "Inga nya träffar."


def rapport(
    traffar: list[tuple[Artikel, list[str]]], lasta: dict[str, int], fel: list[str]
) -> str:
    ordnade = sorted(traffar, key=lambda t: t[0].datum, reverse=True)
    rader = [rad(artikel, funna) for artikel, funna in ordnade]
    if not rader:
        rader = [INGA if not fel else "Inga nya träffar, men alla flöden gick inte att läsa."]
    return "\n".join(rader) + "\n\n" + lasning(lasta, fel) + "\n"


def rad(artikel: Artikel, funna: list[str]) -> str:
    return (
        f"- {artikel.datum} · [{artikel.rubrik}]({artikel.lank}) · {artikel.tidning}\n"
        f"  - Träffade: {', '.join(funna)}"
    )


def lasning(lasta: dict[str, int], fel: list[str]) -> str:
    lista = ", ".join(f"{t} ({n} artiklar)" for t, n in lasta.items()) or "inga"
    text = f"Lästa flöden: {lista}."
    if fel:
        text += "\nGick inte att läsa: " + ", ".join(fel) + "."
    return text
