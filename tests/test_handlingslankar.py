"""K26: handlingarna intill protokollet."""

import tempfile
import unittest
from pathlib import Path

from handlingslankar.lanka import Pool, lanka_fil
from handlingslankar.matcha import handling, punkt
from handlingslankar.sidor import Paragraf, paragraf, som_ordbok

BAS = "https://kh.example"
PROT = BAS + "/kungsbacka/ks/2026/2026-05-05/protokoll.html#sida-2"
RAD = f"- 2026-05-05 · beslut · Beviljat. · [KS protokoll § 12]({PROT})"
PROTOKOLL = """<!-- sida 1 -->
Innehåll
<!-- sida 2 -->
§ 12                      Dnr KS-2026-00123
Godkännande av projektbeställning för Exempel 1:2

Beslut
Kommunstyrelsen godkänner.
"""
FORTECKNING = "".join(f"| {i}. | Ärende | 2026-0012{i} | x |\n" for i in range(1, 5))
KALLELSELISTA = "Ärende Beteckning Förslag\n5. Exempel 2026-00123 Godkänns.\n"
UTDRAG = "SAMMANTRÄDESPROTOKOLL\n§ 50 Dnr KS-2026-00123\nEnligt förvaltningens tjänsteskrivelse.\n"
ANNAN = "TJÄNSTESKRIVELSE\nDiarienummer\nKS 2026-00999\nGodkännande av projektbeställning för Annat 3:4\n"
EGEN = "TJÄNSTESKRIVELSE\nDiarienummer\nKS 2026-00123\nGodkännande av projektbeställning för Exempel 1:2\n"
ARENDE = Paragraf("12", "KS-2026-00123", "Godkännande av projektbeställning för Exempel 1:2")


def handlingar(*sidor: str) -> str:
    return "---\nkvalitet: full\n---\n" + "".join(f"<!-- sida {i} -->\n{s}" for i, s in enumerate(sidor, 1))


def pool(handlingstext: str | None, kallelse: str = "| 5. | Exempel | 2026-00123 | x |\n") -> Pool:
    rot = Path(tempfile.mkdtemp()) / "kungsbacka"
    mote = rot / "ks/2026/2026-05-05"
    mote.mkdir(parents=True)
    (mote / "protokoll.md").write_text(PROTOKOLL, encoding="utf-8")
    (mote / "kallelse.md").write_text(kallelse, encoding="utf-8")
    if handlingstext is not None:
        (mote / "handlingar.md").write_text(handlingstext, encoding="utf-8")
    return Pool(rot, BAS)


def sidorna(*sidor: str) -> dict[int, str]:
    return som_ordbok(handlingar(*sidor))


class Paragrafen(unittest.TestCase):
    def test_paragraf_ur_protokollets_sida(self):
        self.assertEqual(paragraf(som_ordbok(PROTOKOLL), 2), ARENDE)

    def test_paragrafen_som_borjade_pa_sidan_fore(self):
        self.assertEqual(paragraf(som_ordbok(PROTOKOLL + "<!-- sida 3 -->\nFortsättning\n"), 3), ARENDE)


class Handlingen(unittest.TestCase):
    def test_diarienumret_vinner_over_en_rubrik_som_borjar_likadant(self):
        self.assertEqual(handling(sidorna(ANNAN, EGEN), ARENDE), (2, "Tjänsteskrivelse"))

    def test_utdrag_som_namner_tjansteskrivelsen_ar_ingen_tjansteskrivelse(self):
        self.assertEqual(handling(sidorna(UTDRAG, EGEN), ARENDE), (2, "Tjänsteskrivelse"))
        self.assertEqual(handling(sidorna(UTDRAG), ARENDE), (1, "Handlingarna i ärendet"))

    def test_forteckning_over_manga_arenden_lankas_inte(self):
        self.assertIsNone(handling(sidorna(FORTECKNING), ARENDE))
        self.assertIsNone(handling(sidorna(KALLELSELISTA), ARENDE))

    def test_hela_rubriken_racker_nar_huvudet_saknar_diarienummer(self):
        utan = "TJÄNSTESKRIVELSE\nGodkännande av projektbeställning för Exempel 1:2\n"
        borjan = "TJÄNSTESKRIVELSE\nGodkännande av projektbeställning för\n"
        self.assertEqual(handling(sidorna(utan), ARENDE), (1, "Tjänsteskrivelse"))
        self.assertIsNone(handling(sidorna(borjan), ARENDE))

    def test_allmant_arende_far_bara_en_tjansteskrivelse(self):
        allman = Paragraf("3", "KS-2026-00123", "Anmälan av delegeringsbeslut")
        self.assertIsNone(handling(sidorna(UTDRAG), allman))

    def test_arsspann_i_huvudet_ar_inget_diarienummer(self):
        rapport = "TJÄNSTESKRIVELSE\nDiarienummer\n«Diarienr»\nIntraprenadrapport för utbildningsår 2024–2025\n"
        arende = Paragraf("9", "FG-2025-00853", "Intraprenadrapport för utbildningsår 2024–2025")
        self.assertEqual(handling(sidorna(rapport), arende), (1, "Tjänsteskrivelse"))

    def test_punkt_ur_kallelsen(self):
        self.assertEqual(punkt("| 12. | Ärende | KS 2026-00123 | x |", ARENDE), "12")
        self.assertIsNone(punkt("| 12. | Ärende | 2026-00999 | x |", ARENDE))


class Lankningen(unittest.TestCase):
    def test_tjansteskrivelsen_lanks_intill_protokollet(self):
        text, antal = lanka_fil(pool(handlingar(ANNAN, EGEN)), RAD)
        self.assertEqual(antal, 1)
        lank = f"{BAS}/kungsbacka/ks/2026/2026-05-05/handlingar.html#sida-2"
        self.assertEqual(text, f"{RAD} · Handlingar: [Tjänsteskrivelse]({lank})")

    def test_aldre_beslut_befintliga_handlingar_och_saknade_filer_lamnas(self):
        aldre = f"- 2020-01-01 · beslut · Återgivet. · [KS protokoll]({PROT})"
        befintlig = f"{RAD} · Handlingar: [X](https://x.example)"
        self.assertEqual(lanka_fil(pool(handlingar(EGEN)), aldre), (aldre, 0))
        self.assertEqual(lanka_fil(pool(handlingar(EGEN)), befintlig), (befintlig, 0))
        self.assertEqual(lanka_fil(pool(None), RAD), (RAD, 0))

    def test_ej_hamtade_handlingar_ger_pdf_med_punkt(self):
        ej = "---\nkvalitet: ej-hamtad\nkalla_url: https://kommun.example/h.pdf\n---\n"
        text, _ = lanka_fil(pool(ej), RAD)
        self.assertTrue(text.endswith("[Handlingar till sammanträdet, punkt 5 (PDF)](https://kommun.example/h.pdf)"))

    def test_allmant_arende_far_ingen_pdf(self):
        ej = "---\nkvalitet: ej-hamtad\nkalla_url: https://kommun.example/h.pdf\n---\n"
        allman = PROTOKOLL.replace("Godkännande av projektbeställning för Exempel 1:2", "Information från ledamöter")
        test = pool(ej)
        (test.data / "ks/2026/2026-05-05/protokoll.md").write_text(allman, encoding="utf-8")
        self.assertEqual(lanka_fil(test, RAD), (RAD, 0))


if __name__ == "__main__":
    unittest.main()
