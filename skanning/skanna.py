"""Krav: K11, K13 och K39 i KRAV.md. Test: tests/test_skanning.py.

Söker i en källa – kommunens eller regionens handlingar, med samma format –
från början av förra rundans period, eftersom ett protokoll ofta
publiceras veckor efter sammanträdet, och beskriver vad som söktes, vad som
inte gick att läsa och vilka källor i KALLOR.md som rundan söker för hand.
Veckans kontroll söker bara kallelser och handlingar till kommande
sammanträden, så att tillfällen att tycka till hinner föras in före mötet.
"""

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from skanning.rapport import avsnitt, korta, rapport
from skanning.sok import Traff, dokument, sidor, traffar
from skanning.termer import termer
from webbplats import underlag


@dataclass(frozen=True)
class Kalla:
    data: Path
    bas: str
    kommunnamn: tuple[str, ...] = ()

    @property
    def namn(self) -> str:
        return self.bas.rsplit("/", 1)[-1]


def skanna(rot: Path, kalla: Kalla, till: date) -> str:
    fran = underlag.senaste_runda(las(rot, "bevakning/rundor.csv")).fran
    grupper = termer(rot, kalla.kommunnamn)
    filer = dokument(kalla.data, fran)
    tomma = [f for f in filer if not sidor(f.read_text(encoding="utf-8"))]
    funna = sok(kalla.data, [f for f in filer if f not in tomma], grupper)
    sokta = (fran, len(filer))
    text = omfattning(ej_sokta(rot, kalla.namn), grupper, sokta, utan_text(kalla.data, tomma))
    return korta(rapport(funna, (fran, till), text, kalla.bas))


def kommande(rot: Path, kalla: Kalla, dag: date) -> str:
    filer = dokument(kalla.data, dag + timedelta(days=1))
    tomma = [f for f in filer if not sidor(f.read_text(encoding="utf-8"))]
    funna = sok(kalla.data, [f for f in filer if f not in tomma], termer(rot, kalla.kommunnamn))
    text = (
        f"## Kallelser i {kalla.namn} till sammanträden efter {dag}\n\n"
        f"Sökte i {len(filer)} dokument. "
        "Det som rör ett bevakat ärende förs in under *Tycka till* "
        "(`bevakning/README.md`).\n\n"
    )
    if tomma:
        text += f"Utan text, inte sökta: {', '.join(utan_text(kalla.data, tomma))}.\n\n"
    return korta(text + avsnitt("Träffar", funna, kalla.bas))


def utan_text(data: Path, tomma: list[Path]) -> list[str]:
    return [f.relative_to(data).as_posix() for f in tomma]


def sok(data: Path, filer: list[Path], grupper: dict) -> list[Traff]:
    alla = [t for lista in grupper.values() for t in lista]
    funna = [t for fil in filer for t in traffar(data, fil, alla)]
    return sorted(funna, key=lambda t: (t.datum, t.organ, t.dokument))


def las(rot: Path, namn: str) -> str:
    return (rot / namn).read_text(encoding="utf-8")


def ej_sokta(rot: Path, namn: str) -> str:
    for_hand = [k[0] for k in underlag.kallor(las(rot, "KALLOR.md")) if namn not in k[2]]
    return (
        f"Inte sökt automatiskt: {', '.join(for_hand)} och tabellerna i {namn}. "
        "Det görs i rundan (`.claude/skills/runda-1-insamla/SKILL.md`)."
    )


def omfattning(for_hand: str, grupper: dict, sokta: tuple[date, int], tomma: list[str]) -> str:
    fran, antal = sokta
    termerna = ", ".join(f"{len(lista)} {namn}" for namn, lista in grupper.items())
    text = (
        f"Sökte i {antal} dokument med sammanträdesdatum från och med {fran}, början på "
        f"förra rundans period, efter {termerna}.\n\n{for_hand}"
    )
    if tomma:
        text += f"\n\nUtan text, inte sökta: {', '.join(tomma)}."
    return text
