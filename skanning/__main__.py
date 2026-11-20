"""Krav: K11, K13 och K39 i KRAV.md. Test: tests/test_skanning.py.

python3 -m skanning [--kommande] [--kommunnamn NAMN] <data/<kommun>> <dokumentbas> [dag]

Körs från repots rot och skriver rapporten till stdout; `dag` är i dag om
den utelämnas. Med --kommande söks bara sammanträden efter dagen (K13).
Med --kommunnamn söks också på kommunens namn, i regionens handlingar (K39).
"""

import argparse
from datetime import date, datetime, timezone
from pathlib import Path

from skanning.skanna import Kalla, kommande, skanna

tolkare = argparse.ArgumentParser(prog="python3 -m skanning")
tolkare.add_argument("--kommande", action="store_true")
tolkare.add_argument("--kommunnamn", action="append", default=[])
tolkare.add_argument("data", type=Path)
tolkare.add_argument("bas")
tolkare.add_argument("dag", nargs="?", type=date.fromisoformat)
argument = tolkare.parse_args()
kalla = Kalla(argument.data, argument.bas.rstrip("/"), tuple(argument.kommunnamn))
dag = argument.dag or datetime.now(timezone.utc).date()
korning = kommande if argument.kommande else skanna
print(korning(Path.cwd(), kalla, dag), end="")
