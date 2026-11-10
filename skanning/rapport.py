"""Krav: K11 i KRAV.md. Test: tests/test_skanning.py.

Träffarna som Markdown för månadens issue: en rad per dokument med datum,
organ, sidorna, en länk till den första på kommunhandlingars webbplats och
termerna. Protokoll och kallelser står först; handlingarna, där en
lång bilaga kan ge träffar på hundratals sidor, ligger hopfällda sist i
varje avsnitt. Ingen text ur handlingarna återges, eftersom den kan innehålla
personnamn. Rapporten kortas så att den ryms i ett issue.
"""

from datetime import date

from skanning.sok import Traff

GRANS = 60000
STANG = "\n</details>"
KORTAD = "\n\nRapporten är kortad. Hela finns som artefakt i körningen.\n"


def rapport(traffar: list[Traff], period: tuple[date, date], omfattning: str, bas: str) -> str:
    fran, till = period
    i_perioden = [t for t in traffar if t.datum <= till]
    kommande = [t for t in traffar if t.datum > till]
    return (
        f"## Träffar i kommunhandlingar {fran} – {till}\n\n{omfattning}\n\n"
        + avsnitt("I perioden", i_perioden, bas)
        + avsnitt(f"Kommande sammanträden, efter {till}", kommande, bas)
    )


def korta(text: str) -> str:
    if len(text) <= GRANS:
        return text
    kortad = text[: text.rindex("\n", 0, GRANS - len(KORTAD) - len(STANG))]
    oppen = kortad.count("<details>") > kortad.count("</details>")
    return kortad + (STANG if oppen else "") + KORTAD


def avsnitt(rubrik: str, traffar: list[Traff], bas: str) -> str:
    if not traffar:
        return f"### {rubrik}\n\nInga träffar.\n\n"
    dokumenten = list(dict.fromkeys(t.dokument for t in traffar))
    handlingar = [d for d in dokumenten if ar_handlingar(d)]
    ovriga = [d for d in dokumenten if not ar_handlingar(d)]
    forst = rader(ovriga, traffar, bas)
    return f"### {rubrik}\n\n{forst}{hopfalld(handlingar, traffar, bas)}\n"


def ar_handlingar(dokument: str) -> bool:
    return dokument.rsplit("/", 1)[-1].startswith("handlingar")


def hopfalld(dokumenten: list[str], traffar: list[Traff], bas: str) -> str:
    if not dokumenten:
        return ""
    rubrik = f"<summary>Handlingar, {len(dokumenten)} dokument</summary>"
    return f"\n<details>{rubrik}\n\n{rader(dokumenten, traffar, bas)}\n</details>\n"


def rader(dokumenten: list[str], traffar: list[Traff], bas: str) -> str:
    return "".join(rad([t for t in traffar if t.dokument == d], bas) for d in dokumenten)


def rad(sidorna: list[Traff], bas: str) -> str:
    forsta = sidorna[0]
    adress = f"{bas}/{forsta.dokument.removesuffix('.md')}.html#sida-{forsta.sida}"
    nummer = ", ".join(str(t.sida) for t in sidorna)
    termer = ", ".join(dict.fromkeys(term for t in sidorna for term in t.termer))
    namn = forsta.dokument.rsplit("/", 1)[-1]
    return f"- {forsta.datum} · {forsta.organ} · [{namn}]({adress}), sida {nummer} · {termer}\n"
