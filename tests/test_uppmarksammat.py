"""K27: listan över uppmärksammade ärenden och namnen de kallas läses, stoppar
vid fel och syns på startsidan, i korten, på ärendets sida och i tidslinjen."""

import unittest
from dataclasses import replace

from tests.test_sidor import RUNDA, SAJT, arende
from webbplats.arendesida import arendesida
from webbplats.sidor import LISTOR, lista, startsida
from webbplats.uppmarksammat import Namn, las, namn_per_arende

LANKEN = "[Artikeln](https://example.org/a)"
LISTAN = (
    "namn,arende,kalla\n"
    f"Lagret,b,{LANKEN}\n"
    "Stråket,a,projektägaren\n"
    "Stråket,b,projektägaren\n"
)


class Las(unittest.TestCase):
    def test_namnen_i_filens_ordning_med_sina_arenden_och_kallor(self):
        self.assertEqual(
            las(LISTAN, {"a", "b"}),
            [Namn("Lagret", ("b",), (LANKEN,)), Namn("Stråket", ("a", "b"), ("projektägaren",))],
        )

    def test_varje_arende_far_sina_namn(self):
        self.assertEqual(namn_per_arende(las(LISTAN, {"a", "b"})), {"b": ("Lagret", "Stråket"), "a": ("Stråket",)})

    def test_okant_arende_stoppar(self):
        with self.assertRaisesRegex(ValueError, "ärendet finns inte: b"):
            las(LISTAN, {"a"})

    def test_tomt_falt_stoppar(self):
        with self.assertRaisesRegex(ValueError, "tomt fält kalla"):
            las("namn,arende,kalla\nLagret,a,\n", {"a"})

    def test_lank_som_inte_ar_https_stoppar(self):
        with self.assertRaisesRegex(ValueError, "ingen https-länk"):
            las("namn,arende,kalla\nLagret,a,[Art](http://example.org)\n", {"a"})

    def test_samma_namn_och_arende_tva_ganger_stoppar(self):
        with self.assertRaisesRegex(ValueError, "två gånger: Lagret, a"):
            las("namn,arende,kalla\nLagret,a,x\n Lagret ,a,y\n", {"a"})

    def test_fel_kolumner_stoppar(self):
        with self.assertRaisesRegex(ValueError, "kolumnerna"):
            las("namn,fil\nLagret,a\n", {"a"})


class Sidorna(unittest.TestCase):
    def setUp(self):
        self.namnen = las(LISTAN, {"a", "b"})
        per = namn_per_arende(self.namnen)
        self.arenden = [replace(arende("pågår", i), kallas=per[i]) for i in ("a", "b")]

    def test_startsidan_har_rutan_i_listans_ordning_med_kallan(self):
        html = startsida(SAJT, self.arenden, RUNDA, self.namnen)
        self.assertIn('<h2 id="uppmarksammat">Uppmärksammat</h2>', html)
        self.assertLess(html.index("<strong>Lagret</strong>"), html.index("<strong>Stråket</strong>"))
        self.assertIn('Namnet: <a href="https://example.org/a">Artikeln</a>', html)
        self.assertIn('<li data-ort="Fjärås|Åsa"><strong>Stråket</strong>', html)
        self.assertIn('<li data-ort="Åsa|Fjärås"><a href="arende/b.html">Ny förskola</a>', html)

    def test_utan_namn_ingen_ruta(self):
        self.assertNotIn("Uppmärksammat", startsida(SAJT, self.arenden, RUNDA))

    def test_namnen_star_i_kortet_tidslinjen_och_pa_arendets_sida(self):
        html = lista(SAJT, self.arenden, LISTOR[0])
        self.assertIn('<p class="kallas">Uppmärksammat som Lagret, Stråket</p>', html)
        self.assertIn('<small class="kallas">Uppmärksammat som Lagret, Stråket</small>', html)
        self.assertIn('<p class="kallas">Uppmärksammat som Stråket</p>', arendesida(SAJT, self.arenden[0]))


if __name__ == "__main__":
    unittest.main()
