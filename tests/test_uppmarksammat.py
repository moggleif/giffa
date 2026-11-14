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
        lagret, straket = '<span class="etikett">Lagret</span>', '<span class="etikett">Stråket</span>'
        self.assertIn(f'<p class="kallas">Uppmärksammat som {lagret} {straket}</p>', html)
        dold = '<span class="dold">Uppmärksammat som </span>'
        self.assertIn(f'<small class="kallas">{dold}{lagret} {straket}</small>', html)
        self.assertIn(f'<p class="kallas">Uppmärksammat som {straket}</p>', arendesida(SAJT, self.arenden[0]))


class Overst(unittest.TestCase):
    """K29: de uppmärksammade står först i listorna, i listans ordning."""

    def setUp(self):
        self.namnen = las(LISTAN, {"a", "b"})
        self.arenden = [arende("beslutat", i) for i in ("a", "c", "b")]

    def test_uppmarksammade_forst_i_listans_ordning_och_resten_under(self):
        html = lista(SAJT, self.arenden, LISTOR[1], self.namnen)
        b, a, c = (html.index(f'<article id="{i}"') for i in "bac")
        self.assertLess(html.index('<h2 id="uppmarksammat">'), b)
        self.assertLess(b, a)
        self.assertLess(a, html.index('<h2 id="ovriga">Övriga ärenden</h2>'))
        self.assertLess(html.index('<h2 id="ovriga">'), c)

    def test_pagar_behaller_sina_rubriker_under(self):
        pagar = [arende("pågår", i) for i in ("a", "c")]
        html = lista(SAJT, pagar, LISTOR[0], self.namnen)
        self.assertLess(html.index('<article id="a"'), html.index('<h2 id="rorliga">'))
        self.assertNotIn('id="ovriga"', html)

    def test_bara_uppmarksammade_ger_ingen_tom_ovrigt_rubrik(self):
        html = lista(SAJT, [arende("beslutat", "a")], LISTOR[1], self.namnen)
        self.assertIn('<article id="a"', html)
        self.assertNotIn('id="ovriga"', html)
        self.assertNotIn("Inga ärenden ännu.", html)

    def test_utan_uppmarksammade_i_listan_ingen_rubrik(self):
        html = lista(SAJT, [arende("beslutat", "c")], LISTOR[1], self.namnen)
        self.assertNotIn("Uppmärksammat", html)


if __name__ == "__main__":
    unittest.main()
