"""K23: fastighetsbeteckningar blir länkar till kartan."""

import unittest

from webbplats.fastighet import med_kartlankar

OLMANAS = (
    '<a href="https://karta.kungsbacka.se/publik/#m=publik&amp;q='
    '%C3%96lman%C3%A4s+1%3A17">Ölmanäs 1:17</a>'
)


class Kartlankar(unittest.TestCase):
    def test_adressen_ur_kartan(self):
        self.assertEqual(
            med_kartlankar("Planbesked för Ölmanäs 1:17 i Åsa."),
            f"Planbesked för {OLMANAS} i Åsa.",
        )

    def test_trakt_med_bindestreck(self):
        self.assertIn(">Frillesås-Rya 3:77</a>", med_kartlankar("inom Frillesås-Rya 3:77"))

    def test_flera_beteckningar(self):
        text = med_kartlankar("Varla 2:198 och Tölö 5:39")
        self.assertEqual(text.count("<a "), 2)

    def test_upprakning_och_intervall_far_trakten_fran_den_forsta(self):
        text = med_kartlankar("Åsa 5:153 och 5:89, Bäcken 1:31–1:34")
        self.assertEqual(text.count("<a "), 4)
        self.assertIn("q=%C3%85sa+5%3A89\">5:89</a>", text)
        self.assertIn("q=B%C3%A4cken+1%3A34\">1:34</a>", text)

    def test_trakt_som_kan_ha_tva_ord_lankas_inte(self):
        for text in ("Ölmevalla Berg 1:2", "Nedre Ögärdet 2:13", "Fastigheten Rya 4:17"):
            self.assertEqual(med_kartlankar(text), text)

    def test_inte_klockslag_eller_ord_med_liten_bokstav(self):
        for text in ("kl. 10:30", "och 1:105", "Sida 3", "Åsa 5:246:1"):
            self.assertNotIn("<a", med_kartlankar(text), text)

    def test_resten_av_texten_escapas(self):
        self.assertEqual(med_kartlankar("A & <b>"), "A &amp; &lt;b&gt;")
