"""K11: månadens skanning av kommunhandlingar."""

import unittest
from datetime import date
from pathlib import Path

from skanning.rapport import GRANS, korta
from skanning.skanna import kommande, skanna
from skanning.termer import monster

FIXTURER = Path(__file__).resolve().parent / "fixtures"
BAS = "https://kh.example"


def rapport() -> str:
    return skanna(FIXTURER / "rot", FIXTURER / "kh/data/kungsbacka", BAS, date(2026, 11, 30))


class Skanning(unittest.TestCase):
    def test_fran_borjan_av_forra_rundan(self):
        text = rapport()
        self.assertIn("## Träffar i kommunhandlingar 2026-11-01 – 2026-11-30", text)
        self.assertIn("Sökte i 4 dokument med sammanträdesdatum från och med 2026-11-01", text)
        self.assertIn("efter 2 orter, 1 platsnamn, 1 diarienummer.", text)
        self.assertNotIn("2026-10-01", text)

    def test_kallor_for_hand_ur_kallor_md(self):
        self.assertIn(
            "Inte sökt automatiskt: Lokaltidningen och tabellerna i kommunhandlingar.", rapport()
        )

    def test_dokument_utan_text_listas(self):
        self.assertIn("Utan text, inte sökta: vo/2026/2026-11-05/protokoll.md.", rapport())

    def test_hela_ord_och_oppna_arendens_diarienummer(self):
        rad = (
            "- 2026-11-20 · ks · [protokoll.md](https://kh.example/kungsbacka/ks/2026/"
            "2026-11-20/protokoll.html#sida-2), sida 2 · Åsa, Åsaskolan, KS-2026-1\n"
        )
        self.assertIn(rad, rapport())
        self.assertNotIn("KS-2026-2", rapport())

    def test_kommande_sammantraden_for_sig(self):
        text = rapport()
        kommande = text[text.index("### Kommande sammanträden, efter 2026-11-30") :]
        self.assertIn("2026-12-03 · fg · [kallelse.md]", kommande)
        self.assertIn("sida 4 · Fjärås", kommande)

    def test_handlingarna_hopfallda_efter_protokollen(self):
        text = rapport()
        protokoll = text.index("[protokoll.md](https://kh.example/kungsbacka/ks/2026/2026-11-20/")
        hopfalld = text.index("<details><summary>Handlingar, 1 dokument")
        handlingar = text.index("[handlingar.md](https://kh.example/kungsbacka/ks/2026/")
        self.assertLess(protokoll, hopfalld)
        self.assertLess(hopfalld, handlingar)
        self.assertLess(handlingar, text.index("</details>"))

    def test_ingen_text_ur_handlingarna(self):
        self.assertNotIn("Beslut om", rapport())

    def test_lang_rapport_kortas_vid_radslut(self):
        text = korta("rad\n" * GRANS)
        self.assertLessEqual(len(text), GRANS)
        self.assertTrue(text.endswith("Hela finns som artefakt i körningen.\n"))
        self.assertEqual(korta("kort\n"), "kort\n")

    def test_kortad_rapport_stanger_hopfalld_del(self):
        text = korta("<details>\n" + "rad\n" * GRANS)
        self.assertLessEqual(len(text), GRANS)
        self.assertEqual(text.count("</details>"), 1)


class Kommande(unittest.TestCase):
    def test_bara_sammantraden_efter_dagen(self):
        text = kommande(FIXTURER / "rot", FIXTURER / "kh/data/kungsbacka", BAS, date(2026, 11, 30))
        self.assertIn("## Kallelser till sammanträden efter 2026-11-30", text)
        self.assertIn("Sökte i 1 dokument.", text)
        self.assertIn("2026-12-03 · fg · [kallelse.md]", text)
        self.assertNotIn("2026-11-20", text)

    def test_inga_traffar(self):
        text = kommande(FIXTURER / "rot", FIXTURER / "kh/data/kungsbacka", BAS, date(2026, 12, 3))
        self.assertIn("Inga träffar.", text)


class Termer(unittest.TestCase):
    def test_monster(self):
        fall = [
            ("BN-2024-00196", "i BN 2024-00196 och", True),
            ("Fjärås Bräckaskolan", "Fjärås\nBräckaskolan", True),
            ("Åsa 3:14", "Åsa 3:140", False),
            ("Åsa", "Kåsa", False),
        ]
        for term, text, traff in fall:
            with self.subTest(term=term, text=text):
                self.assertEqual(bool(monster(term).search(text)), traff)


if __name__ == "__main__":
    unittest.main()
