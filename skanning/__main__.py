"""Krav: K11 och K13 i KRAV.md. Test: tests/test_skanning.py.

python3 -m skanning [--kommande] <kommunhandlingars data/<kommun>> <dokumentbas> [dag]

Körs från repots rot och skriver rapporten till stdout; `dag` är i dag om
den utelämnas. Med --kommande söks bara sammanträden efter dagen (K13).
"""

import sys
from datetime import date, datetime, timezone
from pathlib import Path

from skanning.skanna import kommande, skanna

argument = sys.argv[1:]
vecka = argument[:1] == ["--kommande"]
argument = argument[vecka:]
if len(argument) not in (2, 3):
    raise SystemExit(__doc__)
dag = date.fromisoformat(argument[2]) if len(argument) == 3 else datetime.now(timezone.utc).date()
korning = kommande if vecka else skanna
print(korning(Path.cwd(), Path(argument[0]), argument[1].rstrip("/"), dag), end="")
