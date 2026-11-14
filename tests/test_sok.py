"""K28: sidan Sök listar alla ärenden med det som går att söka på."""

import unittest
from dataclasses import replace

from tests.test_sidor import SAJT, arende
from webbplats.sok import soksida


class Soksidan(unittest.TestCase):
    def test_alla_arenden_med_rubrik_namn_orter_och_organ_i_sma_bokstaver(self):
        arenden = [replace(arende("pågår", "a"), kallas=("Stråket i Åsa",)), arende("klart", "b")]
        html = soksida(SAJT, arenden)
        self.assertIn('data-sok="ny förskola stråket i åsa åsa fjärås nämnden"', html)
        self.assertIn('data-sok="ny förskola åsa fjärås nämnden"', html)
        self.assertIn('<a href="arende/b.html">Ny förskola</a>', html)
        self.assertIn('<p class="kallas">Kallas Stråket i Åsa</p>', html)

    def test_rutan_ar_dold_tills_skriptet_visar_den(self):
        html = soksida(SAJT, [arende("pågår")])
        self.assertIn('<p class="sok" hidden><label for="sok">Sök</label>', html)
        self.assertIn('<script src="sok.js"></script>', html)
        self.assertIn('<a href="sok.html" aria-current="page">Sök</a>', html)


if __name__ == "__main__":
    unittest.main()
