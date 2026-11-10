"""Krav: K11 i KRAV.md. Test: tests/test_skanning.py.

Söker från början av förra rundans period, eftersom ett protokoll ofta
publiceras veckor efter sammanträdet, och beskriver vad som söktes, vad som
inte gick att läsa och vilka källor i KALLOR.md som rundan söker för hand.
"""

from datetime import date
from pathlib import Path

from skanning.rapport import korta, rapport
from skanning.sok import dokument, sidor, traffar
from skanning.termer import termer
from webbplats import underlag

KOMMUNHANDLINGAR = "kommunhandlingar"


def skanna(rot: Path, data: Path, bas: str, till: date) -> str:
    fran = underlag.senaste_runda(las(rot, "bevakning/rundor.csv")).fran
    grupper = termer(rot)
    filer = dokument(data, fran)
    tomma = [f for f in filer if not sidor(f.read_text(encoding="utf-8"))]
    alla = [t for lista in grupper.values() for t in lista]
    funna = [t for fil in filer if fil not in tomma for t in traffar(data, fil, alla)]
    funna.sort(key=lambda t: (t.datum, t.organ, t.dokument))
    text = omfattning(rot, grupper, (fran, len(filer)), [f.relative_to(data) for f in tomma])
    return korta(rapport(funna, (fran, till), text, bas))


def las(rot: Path, namn: str) -> str:
    return (rot / namn).read_text(encoding="utf-8")


def omfattning(rot: Path, grupper: dict, sokta: tuple[date, int], tomma: list[Path]) -> str:
    fran, antal = sokta
    termerna = ", ".join(f"{len(lista)} {namn}" for namn, lista in grupper.items())
    for_hand = [
        k[0] for k in underlag.kallor(las(rot, "KALLOR.md")) if KOMMUNHANDLINGAR not in k[2]
    ]
    text = (
        f"Sökte i {antal} dokument med sammanträdesdatum från och med {fran}, början på "
        f"förra rundans period, efter {termerna}.\n\n"
        f"Inte sökt automatiskt: {', '.join(for_hand)} och tabellerna i kommunhandlingar. "
        "Det görs i rundan (`.claude/skills/runda-1-insamla/SKILL.md`)."
    )
    if tomma:
        text += f"\n\nUtan text, inte sökta: {', '.join(p.as_posix() for p in tomma)}."
    return text
