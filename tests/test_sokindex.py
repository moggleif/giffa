"""K28: sökindexet som knappen Sök söker i."""

import json
import unittest
from dataclasses import replace
from datetime import date

from tests.test_ksmotet import POOL
from tests.test_sidor import SAJT, arende
from webbplats.kallelsen import kommande
from webbplats.sokindex import sokindex


def index(arenden: list, motet: object = None) -> dict:
    return json.loads(sokindex(SAJT, arenden, motet))


class Arendena(unittest.TestCase):
    def test_det_som_visas_och_det_som_soks_i_sma_bokstaver(self):
        a = replace(arende("pågår", "a"), kallas=("Stråket i Åsa",))
        a.falt["diarienummer"] = "KS-2026-00001"
        post = index([a])["arenden"][0]
        self.assertEqual(post["rubrik"], "Ny förskola")
        self.assertEqual(post["adress"], "arende/a.html")
        self.assertEqual(post["orter"], ["Åsa", "Fjärås"])
        self.assertEqual(post["status"], "pågår")
        self.assertEqual(post["kallas"], ["Stråket i Åsa"])
        self.assertEqual(post["traff"], "ny förskola åsa fjärås nämnden ks-2026-00001 stråket i åsa")
        self.assertEqual(post["text"], "två meningar om ärendet. nämnden beslutade. ett förslag.")

    def test_foreningarnas_orter_for_urvalet(self):
        self.assertEqual(
            index([])["foreningar"], {"Förening Åsa": ["Åsa", "Fjärås"], "Förening Särö": ["Särö"]}
        )


class Motet(unittest.TestCase):
    def test_punkterna_med_adress_pa_sidan_och_motets_datum(self):
        motet = index([], kommande(POOL, date(2026, 10, 21)))["motet"]
        self.assertEqual(motet["rubrik"], "KS-mötet 24 november 2026")
        forsta = motet["punkter"][0]
        self.assertEqual(forsta["rubrik"], "Utbyggnad av Åsaskolan")
        self.assertEqual(forsta["adress"], "ks-motet.html#punkt-1")
        self.assertEqual(forsta["nummer"], 1)
        self.assertEqual(forsta["dnr"], "KS-2026-00001")
        self.assertEqual(forsta["traff"], "utbyggnad av åsaskolan ks-2026-00001")
        self.assertIn("skolan ska byggas ut för fler elever.", forsta["text"])

    def test_utan_mote_eller_kallelse_inga_punkter(self):
        self.assertIsNone(index([])["motet"])
        self.assertIsNone(index([], kommande(POOL, date(2026, 10, 1)))["motet"])


if __name__ == "__main__":
    unittest.main()
