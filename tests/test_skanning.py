"""K11: månadens skanning av kommunhandlingar."""

import unittest
from datetime import date
from pathlib import Path

from skanning.__main__ import skanna

FIXTURER = Path(__file__).resolve().parent / "fixtures"
BAS = "https://kh.example"


def rapport() -> str:
    return skanna(FIXTURER / "rot", FIXTURER / "kh/data/kungsbacka", BAS, date(2026, 11, 30))


class Skanning(unittest.TestCase):
    def test_period_och_vad_som_soktes(self):
        text = rapport()
        self.assertIn("## Träffar i kommunhandlingar 2026-11-01 – 2026-11-30", text)
        self.assertIn("Sökte i 2 dokument från och med 2026-11-01 efter 2 orter, 1 platser", text)
        self.assertIn("Inte sökt automatiskt:", text)

    def test_hela_ord_och_oppna_arendens_diarienummer(self):
        rad = (
            "- 2026-11-20 · ks · [protokoll.md](https://kh.example/kungsbacka/ks/2026/"
            "2026-11-20/protokoll.html#sida-2), sida 2 · Åsa, Åsaskolan, KS-2026-1\n"
        )
        self.assertIn(rad, rapport())
        self.assertNotIn("KS-2026-2", rapport())

    def test_kommande_sammantraden_for_sig_och_aldre_inte_alls(self):
        text = rapport()
        kommande = text[text.index("### Kommande sammanträden, efter 2026-11-30") :]
        self.assertIn("2026-12-03 · fg · [kallelse.md]", kommande)
        self.assertIn("sida 4 · Fjärås", kommande)
        self.assertNotIn("2026-10-01", text)

    def test_ingen_text_ur_handlingarna(self):
        self.assertNotIn("Beslut om", rapport())


if __name__ == "__main__":
    unittest.main()
