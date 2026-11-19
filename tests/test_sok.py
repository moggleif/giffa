"""K28: sidan Sök listar alla ärenden, med sökfältet utfällt överst."""

import unittest
from dataclasses import replace

from tests.test_sidor import SAJT, arende
from webbplats.sok import soksida


class Soksidan(unittest.TestCase):
    def test_alla_arenden_med_orter_status_och_namn(self):
        arenden = [replace(arende("pågår", "a"), kallas=("Stråket i Åsa",)), arende("klart", "b")]
        html = soksida(SAJT, arenden)
        self.assertIn('<li><a href="arende/b.html">Ny förskola</a> <small>Åsa, Fjärås · klart</small>', html)
        self.assertIn('<p class="kallas">Uppmärksammat som <span class="etikett">Stråket i Åsa</span></p>', html)

    def test_faltet_falls_ut_av_skriptet(self):
        html = soksida(SAJT, [arende("pågår")])
        self.assertIn('<ul class="sokning" data-sok-oppen>', html)
        self.assertIn('<script src="sokruta.js" defer></script>', html)
        self.assertIn('<a href="sok.html" aria-current="page">Sök</a>', html)


if __name__ == "__main__":
    unittest.main()
