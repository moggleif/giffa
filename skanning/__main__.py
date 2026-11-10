"""Krav: K11 i KRAV.md. Test: tests/test_skanning.py.

python3 -m skanning <kommunhandlingars data/<kommun>> <dokumentbas> [till]

Söker från dagen efter förra rundan i bevakning/rundor.csv till och med
`till` (i dag om den utelämnas) och skriver rapporten till stdout.
Dokument från senare sammanträden, som kallelser, tas med för sig.
"""

import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

from skanning.rapport import rapport
from skanning.sok import dokument, traffar
from skanning.termer import termer
from webbplats import underlag


def skanna(rot: Path, data: Path, bas: str, till: date) -> str:
    runda = underlag.senaste_runda((rot / "bevakning/rundor.csv").read_text(encoding="utf-8"))
    fran = runda.till + timedelta(days=1)
    grupper = termer(rot)
    alla = [t for lista in grupper.values() for t in lista]
    filer = dokument(data, fran)
    funna = [t for fil in filer for t in traffar(data, fil, alla)]
    funna.sort(key=lambda t: (t.datum, t.organ, t.dokument))
    antal = ", ".join(f"{len(lista)} {namn}" for namn, lista in grupper.items())
    sokt = f"Sökte i {len(filer)} dokument från och med {fran} efter {antal}."
    return rapport(funna, (fran, till), sokt, bas)


if __name__ == "__main__":
    till = (
        date.fromisoformat(sys.argv[3]) if len(sys.argv) > 3 else datetime.now(timezone.utc).date()
    )
    print(skanna(Path.cwd(), Path(sys.argv[1]), sys.argv[2].rstrip("/"), till), end="")
