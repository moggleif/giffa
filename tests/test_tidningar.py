"""K37: tidningarnas flöden."""

import unittest
from datetime import date

from tidningar.flode import Artikel, artiklar
from tidningar.matcha import termer, traffar
from tidningar.rapport import INGA, rapport

FLODE = """<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel><title>t</title>
<item><title>Ny skola i &#197;sa</title>
<link>https://tidning.example/skola/1</link>
<pubDate>Mon, 16 Nov 2026 00:30:00  +0200</pubDate>
<description><![CDATA[<p>Kommunen vill bygga <b>Åsaskolan</b> större.</p>]]></description></item>
<item><title>Onsalabons roman</title><link>https://tidning.example/kultur/2</link>
<pubDate>Sun, 15 Nov 2026 20:15:00 +0100</pubDate></item>
</channel></rss>"""


def artikel(rubrik: str, lank: str = "https://t.example/a") -> Artikel:
    return Artikel("Tidningen", rubrik, lank, date(2026, 11, 16), "")


class Flode(unittest.TestCase):
    def test_rubrik_lank_datum_och_ingress_utan_html(self):
        forsta, andra = artiklar("Tidningen", FLODE)
        self.assertEqual(forsta.rubrik, "Ny skola i Åsa")
        self.assertEqual(forsta.lank, "https://tidning.example/skola/1")
        self.assertEqual(forsta.datum, date(2026, 11, 16))
        self.assertEqual(forsta.ingress, "Kommunen vill bygga Åsaskolan större.")
        self.assertEqual(andra.ingress, "")


class Matcha(unittest.TestCase):
    SOKTA = ("Åsa", "Onsala", "Åsaskolan", "Restaurangstråket i Åsa")

    def test_termerna_ar_orter_platser_och_namn_en_gang_var(self):
        omrade = "# Område\n\n## Förening Åsa\n\n- Åsa\n- Fjärås\n\n## Platser\n"
        platser = "namn,typ,ort,anteckning,handlingar,exempel\nÅsaskolan,grundskola,Åsa,,1,x\n"
        namn = "namn,arende,kalla\nBanvallen,a,b\nBanvallen,c,d\nÅsaskolan,e,f\n"
        self.assertEqual(termer(omrade, platser, namn), ["Åsa", "Fjärås", "Åsaskolan", "Banvallen"])

    def test_ort_och_amne_ger_traff(self):
        traff = traffar([artikel("Nya bostäder i Åsa")], list(self.SOKTA), "")
        self.assertEqual(traff[0][1], ["Åsa"])

    def test_ort_utan_amne_ger_ingen_traff(self):
        rubriker = ["Bilbrand i Åsa i norra Halland", "Kommunen varnar för halka i Åsa"]
        artiklar = [artikel(r) for r in rubriker]
        self.assertEqual(traffar(artiklar, list(self.SOKTA), ""), [])

    def test_hela_ord(self):
        self.assertEqual(traffar([artikel("Onsalabon bygger")], list(self.SOKTA), ""), [])

    def test_lankar_som_redan_finns_hoppas_over(self):
        kanda = "- 2026-11-16 · [x](https://t.example/a) · Tidningen"
        self.assertEqual(traffar([artikel("Ny skola i Åsa")], list(self.SOKTA), kanda), [])


class Rapport(unittest.TestCase):
    def test_rad_i_arendenas_format_med_termerna_efter(self):
        text = rapport([(artikel("Ny skola i Åsa"), ["Åsa"])], {"Tidningen": 2}, [])
        self.assertIn(
            "- 2026-11-16 · [Ny skola i Åsa](https://t.example/a) · Tidningen\n"
            "  - Träffade: Åsa\n", text
        )
        self.assertIn("Lästa flöden: Tidningen (2 artiklar).", text)

    def test_inga_traffar_och_floden_som_inte_gick_att_lasa(self):
        self.assertTrue(rapport([], {"Tidningen": 2}, []).startswith(INGA + "\n"))
        text = rapport([], {}, ["SVT Halland (HTTP Error 503)"])
        self.assertFalse(text.startswith(INGA + "\n"))
        self.assertIn("Gick inte att läsa: SVT Halland (HTTP Error 503).", text)
