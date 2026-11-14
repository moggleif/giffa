"""K26: handlingarna intill protokollet."""

import tempfile
import unittest
from pathlib import Path

from handlingslankar.lanka import Pool, lanka_fil
from handlingslankar.matcha import forteckning, punkt
from handlingslankar.sidor import Paragraf, paragraf, sidor

BAS = "https://kh.example"
PROT = BAS + "/kungsbacka/ks/2026/2026-05-05/protokoll.html#sida-2"
PROTOKOLL = """<!-- sida 1 -->
Innehåll
<!-- sida 2 -->
§ 12                      Dnr KS-2026-00123
Planbesked för Exempel 1:2
i Exempelby

Beslut
Kommunstyrelsen lämnar besked.
"""
HANDLINGAR = """---
kvalitet: full
---
<!-- sida 4 -->
| 1. | Planbesked för Exempel 1:2 | 2026-00123 | Förslag |
| 2. | Annat | 2026-00001 | Förslag |
| 3. | Annat | 2026-00002 | Förslag |
| 4. | Annat | 2026-00003 | Förslag |
<!-- sida 7 -->
TJÄNSTESKRIVELSE
Diarienummer
KS 2026-00123
Planbesked för Exempel 1:2 i Exempelby
"""


def pool(handlingar: str = HANDLINGAR) -> Pool:
    rot = Path(tempfile.mkdtemp()) / "kungsbacka"
    mote = rot / "ks/2026/2026-05-05"
    mote.mkdir(parents=True)
    (mote / "protokoll.md").write_text(PROTOKOLL, encoding="utf-8")
    (mote / "handlingar.md").write_text(handlingar, encoding="utf-8")
    (mote / "kallelse.md").write_text("| 5. | Planbesked | 2026-00123 | Förslag |\n", encoding="utf-8")
    return Pool(rot, BAS)


class Handlingslankar(unittest.TestCase):
    def test_paragraf_ur_protokollets_sida(self):
        funnen = paragraf(sidor(PROTOKOLL), 2)
        self.assertEqual(funnen, Paragraf("12", "KS-2026-00123", "Planbesked för Exempel 1:2 i Exempelby"))

    def test_tjansteskrivelsen_lanks_intill_protokollet(self):
        rad = f"- 2026-05-05 · beslut · Beviljat. · [KS protokoll § 12]({PROT})"
        text, antal = lanka_fil(pool(), rad)
        self.assertEqual(antal, 1)
        self.assertEqual(
            text,
            rad + f" · Handlingar: [Tjänsteskrivelse]({BAS}/kungsbacka/ks/2026/2026-05-05/handlingar.html#sida-7)",
        )

    def test_forteckningen_hoppas_over(self):
        self.assertTrue(forteckning(sidor(HANDLINGAR)[4]))
        self.assertFalse(forteckning(sidor(HANDLINGAR)[7]))

    def test_aldre_beslut_och_befintliga_handlingar_lamnas(self):
        aldre = f"- 2020-01-01 · beslut · Återgivet. · [KS protokoll]({PROT})"
        befintlig = f"- 2026-05-05 · beslut · Beviljat. · [KS]({PROT}) · Handlingar: [X](https://x.example)"
        self.assertEqual(lanka_fil(pool(), aldre), (aldre, 0))
        self.assertEqual(lanka_fil(pool(), befintlig), (befintlig, 0))

    def test_ej_hamtade_handlingar_ger_pdf_med_punkt(self):
        ej = "---\nkvalitet: ej-hamtad\nkalla_url: https://kommun.example/h.pdf\n---\n"
        rad = f"- 2026-05-05 · beslut · Beviljat. · [KS protokoll § 12]({PROT})"
        text, _ = lanka_fil(pool(ej), rad)
        self.assertTrue(text.endswith("[Handlingar till sammanträdet, punkt 5 (PDF)](https://kommun.example/h.pdf)"))

    def test_punkt_ur_kallelsen(self):
        self.assertEqual(punkt("| 12. | Ärende | KS 2026-00123 | x |", Paragraf("1", "KS-2026-00123", "")), "12")
        self.assertIsNone(punkt("| 12. | Ärende | 2026-00999 | x |", Paragraf("1", "KS-2026-00123", "")))


if __name__ == "__main__":
    unittest.main()
