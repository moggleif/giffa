"""Krav: K3–K10, K18, K27, K28 och K34 i KRAV.md. Test: tests/test_bygg.py.

python3 -m webbplats <utkatalog> <repoadress> <kommunhandlingar>

Läser ärendena och underlaget i repots rot, kontrollerar dem och skriver
sidorna och det som ligger i docs/ till utkatalogen. Sidan om
kommunstyrelsens kommande sammanträde (K34) läses ur en utcheckning av
kommunhandlingar, vars `src/` ska finnas i `PYTHONPATH`.
"""

import shutil
import sys
from dataclasses import replace
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from webbplats import underlag
from webbplats.arende import Arende, tolka
from webbplats.arendesida import arendesida
from webbplats.bevakar import bevakar
from webbplats.kallelsen import kommande
from webbplats.kartlankar import ur_platser
from webbplats.kontroll import kontrollera, kontrollera_omrade
from webbplats.ksmotet import SIDA as KS_MOTET
from webbplats.ksmotet import ks_motet
from webbplats.mall import Sajt
from webbplats.sidor import LISTOR, lista, startsida
from webbplats.sok import soksida
from webbplats.uppmarksammat import las as las_namnen

UPPMARKSAMMADE = "bevakning/uppmarksammade.csv"


def las_arenden(rot: Path, orter: list[str]) -> list[Arende]:
    arenden = [las_arende(rot, fil, orter) for fil in sorted(rot.glob("bevakning/*/*.md"))]
    if dubbletter := sorted({a.id for a in arenden if [b.id for b in arenden].count(a.id) > 1}):
        raise SystemExit(f"samma filnamn i flera kataloger: {', '.join(dubbletter)}")
    return sorted(arenden, key=lambda a: a.handelser[0].datum, reverse=True)


def las_arende(rot: Path, fil: Path, orter: list[str]) -> Arende:
    namn = fil.relative_to(rot).as_posix()
    try:
        arende = tolka(namn, fil.read_text(encoding="utf-8"))
        kontrollera(arende, orter)
    except ValueError as fel:
        raise SystemExit(f"{namn}: {fel}") from fel
    return arende


def las_foreningar(rot: Path) -> dict[str, list[str]]:
    foreningar = underlag.foreningar(las(rot, "OMRADE.md"))
    try:
        kontrollera_omrade(foreningar)
    except ValueError as fel:
        raise SystemExit(f"OMRADE.md: {fel}") from fel
    return foreningar


def med_namn(rot: Path, arenden: list[Arende]) -> list[Arende]:
    try:
        per_arende = las_namnen(las(rot, UPPMARKSAMMADE), {a.id for a in arenden})
    except ValueError as fel:
        raise SystemExit(f"{UPPMARKSAMMADE}: {fel}") from fel
    return [replace(a, kallas=per_arende.get(a.id, ())) for a in arenden]


def las(rot: Path, namn: str) -> str:
    return (rot / namn).read_text(encoding="utf-8")


def bygg(rot: Path, ut: Path, repo: str, pool: Path) -> None:
    byggd = datetime.now(ZoneInfo("Europe/Stockholm"))
    platser = underlag.platser(las(rot, "platser.csv"))
    sajt = Sajt(repo, byggd, las_foreningar(rot), ur_platser(platser))
    arenden = med_namn(rot, las_arenden(rot, sajt.orter))
    runda = underlag.senaste_runda(las(rot, "bevakning/rundor.csv"))
    kallor = underlag.kallor(las(rot, "KALLOR.md"))
    shutil.copytree(rot / "docs", ut, dirs_exist_ok=True)
    sidor = {
        "index.html": startsida(sajt, arenden, runda),
        "sok.html": soksida(sajt, arenden),
        "bevakar.html": bevakar(sajt, platser, kallor),
        KS_MOTET: ks_motet(sajt, kommande(pool, byggd.date()), arenden, platser),
    }
    sidor |= {listan[0]: lista(sajt, arenden, listan) for listan in LISTOR}
    sidor |= {a.sida: arendesida(sajt, a) for a in arenden}
    (ut / "arende").mkdir(exist_ok=True)
    for namn, html in sidor.items():
        (ut / namn).write_text(html, encoding="utf-8")


if __name__ == "__main__":
    bygg(Path.cwd(), Path(sys.argv[1]), sys.argv[2].rstrip("/"), Path(sys.argv[3]))
