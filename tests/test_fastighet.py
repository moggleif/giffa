"""K23: fastighetsbeteckningar blir länkar till kartan."""

import unittest
from urllib.parse import quote

from webbplats.fastighet import KARTA, med_kartlankar


def lank(beteckning: str) -> str:
    adress = KARTA.format(quote(beteckning))
    return f'<a class="fastighet" href="{adress}">{beteckning}</a>'


class Kartlankar(unittest.TestCase):
    def test_en_beteckning_blir_en_lank(self):
        self.assertEqual(
            med_kartlankar("Planbesked för Ölmanäs 1:17 i Åsa."),
            f"Planbesked för {lank('Ölmanäs 1:17')} i Åsa.",
        )

    def test_trakt_med_bindestreck(self):
        self.assertIn(lank("Frillesås-Rya 3:77"), med_kartlankar("inom Frillesås-Rya 3:77"))

    def test_flera_beteckningar(self):
        text = med_kartlankar("Varla 2:198 och Tölö 5:39")
        self.assertEqual(text, f"{lank('Varla 2:198')} och {lank('Tölö 5:39')}")

    def test_inte_klockslag_eller_ord_med_liten_bokstav(self):
        for text in ("kl. 10:30", "och 1:105", "Sida 3", "Åsa 5:246:1"):
            self.assertNotIn("<a", med_kartlankar(text), text)

    def test_resten_av_texten_escapas(self):
        self.assertEqual(med_kartlankar("A & <b>"), "A &amp; &lt;b&gt;")
