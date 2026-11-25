"""K40: varje byggd sida är lika med facit, byggd ur en fryst rot, pool och klocka.

Är en ändring av sidan avsedd skrivs facit om, och diffen följer med:
python3 -m tests.test_facit --skriv-om
"""

import shutil
import sys
import unittest
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from webbplats.__main__ import sidor

TESTER = Path(__file__).resolve().parent
FACIT = TESTER / "facit"
BYGGD = datetime(2026, 11, 20, 10, 0, tzinfo=ZoneInfo("Europe/Stockholm"))
SKRIV_OM = "Var ändringen avsedd: python3 -m tests.test_facit --skriv-om"


def byggda() -> dict[str, str]:
    fixturer = TESTER / "fixtures"
    return sidor(fixturer / "sajt", "https://github.com/agare/giffa", fixturer / "pool", BYGGD)


def skriv_om() -> None:
    if FACIT.exists():
        shutil.rmtree(FACIT)
    for namn, text in byggda().items():
        (FACIT / namn).parent.mkdir(parents=True, exist_ok=True)
        (FACIT / namn).write_text(text, encoding="utf-8")


class Facit(unittest.TestCase):
    def test_samma_sidor_som_facit(self):
        facit = sorted(f.relative_to(FACIT).as_posix() for f in FACIT.rglob("*") if f.is_file())
        self.assertEqual(sorted(byggda()), facit, SKRIV_OM)

    def test_varje_sida_lika_med_facit(self):
        for namn, text in byggda().items():
            with self.subTest(namn):
                self.assertEqual(text, (FACIT / namn).read_text(encoding="utf-8"), SKRIV_OM)


if __name__ == "__main__":
    if sys.argv[1:] == ["--skriv-om"]:
        skriv_om()
    else:
        unittest.main()
