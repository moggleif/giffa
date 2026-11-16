"""K27: listan över uppmärksammade ärenden och namnen de kallas läses, stoppar
vid fel och syns i korten, på ärendets sida och i tidslinjen, länkade till
källan när den är en länk."""

import unittest
from dataclasses import replace

from tests.test_sidor import SAJT, arende
from webbplats.arende import Namn
from webbplats.arendesida import arendesida
from webbplats.sidor import LISTOR, lista
from webbplats.uppmarksammat import las

LANKEN = "[Artikeln](https://example.org/a)"
LISTAN = (
    "namn,arende,kalla\n"
    f"Lagret,b,{LANKEN}\n"
    "Stråket,a,projektägaren\n"
    "Stråket,b,projektägaren\n"
)


class Las(unittest.TestCase):
    def test_varje_arende_far_sina_namn_i_filens_ordning_med_kallan(self):
        self.assertEqual(
            las(LISTAN, {"a", "b"}),
            {
                "b": (Namn("Lagret", LANKEN), Namn("Stråket", "projektägaren")),
                "a": (Namn("Stråket", "projektägaren"),),
            },
        )

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
        per = las(LISTAN, {"a", "b"})
        self.arenden = [replace(arende("pågår", i), kallas=per[i]) for i in ("a", "b")]

    def test_namnen_star_i_kortet_tidslinjen_och_pa_arendets_sida(self):
        html = lista(SAJT, self.arenden, LISTOR[0])
        lagret = '<a class="etikett" href="https://example.org/a" title="Namnet: Artikeln">Lagret</a>'
        straket = '<span class="etikett" title="Namnet: projektägaren">Stråket</span>'
        self.assertIn(f'<p class="kallas">Uppmärksammat som {lagret} {straket}</p>', html)
        dold = '<span class="dold">Uppmärksammat som </span>'
        self.assertIn(f'<small class="kallas">{dold}{lagret} {straket}</small>', html)
        self.assertIn(f'<p class="kallas">Uppmärksammat som {straket}</p>', arendesida(SAJT, self.arenden[0]))


if __name__ == "__main__":
    unittest.main()
