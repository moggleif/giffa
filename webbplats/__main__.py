"""Krav: K3–K10 i KRAV.md. Test: tests/test_bygg.py.

python3 -m webbplats <utkatalog> <repoadress>

Läser ärendena och underlaget i repots rot, kontrollerar dem och skriver
sidorna och det som ligger i docs/ till utkatalogen.
"""

import shutil
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from webbplats import underlag
from webbplats.arende import Arende, tolka
from webbplats.bevakar import bevakar
from webbplats.kontroll import kontrollera
from webbplats.mall import Sajt
from webbplats.sidor import historik, startsida


def las_arenden(rot: Path, orter: list[str]) -> list[Arende]:
    arenden = [las_arende(rot, fil, orter) for fil in sorted(rot.glob("bevakning/*/*.md"))]
    return sorted(arenden, key=lambda a: a.handelser[0].datum, reverse=True)


def las_arende(rot: Path, fil: Path, orter: list[str]) -> Arende:
    namn = fil.relative_to(rot).as_posix()
    try:
        arende = tolka(namn, fil.read_text(encoding="utf-8"))
        kontrollera(arende, orter)
    except ValueError as fel:
        raise SystemExit(f"{namn}: {fel}") from fel
    return arende


def las(rot: Path, namn: str) -> str:
    return (rot / namn).read_text(encoding="utf-8")


def bygg(rot: Path, ut: Path, repo: str) -> None:
    byggd = datetime.now(ZoneInfo("Europe/Stockholm"))
    sajt = Sajt(repo, byggd, underlag.orter(las(rot, "OMRADE.md")))
    arenden = las_arenden(rot, sajt.orter)
    runda = underlag.senaste_runda(las(rot, "bevakning/rundor.csv"))
    platser = underlag.platser(las(rot, "platser.csv"))
    kallor = underlag.kallor(las(rot, "KALLOR.md"))
    shutil.copytree(rot / "docs", ut, dirs_exist_ok=True)
    sidor = {
        "index.html": startsida(sajt, arenden, runda),
        "historik.html": historik(sajt, arenden),
        "bevakar.html": bevakar(sajt, platser, kallor),
    }
    for namn, html in sidor.items():
        (ut / namn).write_text(html, encoding="utf-8")


if __name__ == "__main__":
    bygg(Path.cwd(), Path(sys.argv[1]), sys.argv[2].rstrip("/"))
