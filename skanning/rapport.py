"""Krav: K11 i KRAV.md. Test: tests/test_skanning.py.

Träffarna som Markdown för månadens issue: en rad per dokument med datum,
organ, sidorna, en länk till den första på kommunhandlingars webbplats och
termerna. Ingen text ur
handlingarna återges, eftersom den kan innehålla personnamn.
"""

from datetime import date

from skanning.sok import Traff

EJ_SOKT = (
    "Inte sökt automatiskt: kungsbacka.se, karta.kungsbacka.se, Norra Halland, "
    "Kungsbacka-Posten och tabellerna i kommunhandlingar. Det görs i rundan "
    "(`.claude/skills/runda-1-insamla/SKILL.md`)."
)


def rapport(traffar: list[Traff], period: tuple[date, date], sokt: str, bas: str) -> str:
    fran, till = period
    i_perioden = [t for t in traffar if t.datum <= till]
    kommande = [t for t in traffar if t.datum > till]
    return (
        f"## Träffar i kommunhandlingar {fran} – {till}\n\n{sokt}\n\n"
        + avsnitt("I perioden", i_perioden, bas)
        + avsnitt(f"Kommande sammanträden, efter {till}", kommande, bas)
        + EJ_SOKT
        + "\n"
    )


def avsnitt(rubrik: str, traffar: list[Traff], bas: str) -> str:
    if not traffar:
        return f"### {rubrik}\n\nInga träffar.\n\n"
    dokumenten = dict.fromkeys(t.dokument for t in traffar)
    rader = [rad([t for t in traffar if t.dokument == d], bas) for d in dokumenten]
    return f"### {rubrik}\n\n" + "".join(rader) + "\n"


def rad(sidorna: list[Traff], bas: str) -> str:
    forsta = sidorna[0]
    adress = f"{bas}/{forsta.dokument.removesuffix('.md')}.html#sida-{forsta.sida}"
    nummer = ", ".join(str(t.sida) for t in sidorna)
    termer = ", ".join(dict.fromkeys(term for t in sidorna for term in t.termer))
    namn = forsta.dokument.rsplit("/", 1)[-1]
    return f"- {forsta.datum} · {forsta.organ} · [{namn}]({adress}), sida {nummer} · {termer}\n"
