"""Krav: K11 i KRAV.md. Test: tests/test_skanning.py.

python3 -m skanning <kommunhandlingars data/<kommun>> <dokumentbas> [till]

Körs från repots rot och skriver rapporten till stdout; `till` är i dag om
den utelämnas.
"""

import sys
from datetime import date, datetime, timezone
from pathlib import Path

from skanning.skanna import skanna

if len(sys.argv) not in (3, 4):
    raise SystemExit(__doc__)
till = date.fromisoformat(sys.argv[3]) if len(sys.argv) == 4 else datetime.now(timezone.utc).date()
print(skanna(Path.cwd(), Path(sys.argv[1]), sys.argv[2].rstrip("/"), till), end="")
