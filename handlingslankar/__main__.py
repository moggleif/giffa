"""Krav: K26 i KRAV.md. Test: tests/test_handlingslankar.py.

python3 -m handlingslankar <kommunhandlingars data/<kommun>> <dokumentbas>

Körs från repots rot, skriver om ärendena i bevakning/ och skriver ut hur
många händelser som fick handlingar.
"""

import sys
from pathlib import Path

from handlingslankar.lanka import Pool, lanka_fil

if len(sys.argv) != 3:
    raise SystemExit(__doc__)
pool, totalt = Pool(Path(sys.argv[1]), sys.argv[2].rstrip("/")), 0
for fil in sorted(Path("bevakning").glob("*/*.md")):
    if fil.name == "README.md":
        continue
    text, antal = lanka_fil(pool, fil.read_text(encoding="utf-8"))
    if antal:
        fil.write_text(text, encoding="utf-8")
        print(f"{fil}: {antal}")
    totalt += antal
print(f"Händelser som fick handlingar: {totalt}")
