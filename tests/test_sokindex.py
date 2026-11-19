"""K28: Giffås sökindex, i det format som alla sajterna skriver sitt i."""

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
        grupp = index([a])["grupper"][0]
        self.assertEqual(grupp["rubrik"], "Ärenden")
        self.assertEqual(grupp["poster"][0], {
            "rubrik": "Ny förskola",
            "adress": "arende/a.html",
            "om": ["Åsa, Fjärås", "pågår"],
            "orter": ["Åsa", "Fjärås"],
            "kallas": ["Stråket i Åsa"],
            "traff": "ny förskola åsa fjärås nämnden ks-2026-00001 stråket i åsa",
            "text": "två meningar om ärendet. nämnden beslutade. ett förslag.",
        })

    def test_foreningarnas_orter_for_urvalet(self):
        self.assertEqual(
            index([])["foreningar"], {"Förening Åsa": ["Åsa", "Fjärås"], "Förening Särö": ["Särö"]}
        )


class Motet(unittest.TestCase):
    def test_punkterna_med_adress_pa_sidan_och_motets_datum(self):
        grupp = index([], kommande(POOL, date(2026, 10, 21)))["grupper"][1]
        self.assertEqual(grupp["rubrik"], "KS-mötet 24 november 2026")
        forsta = grupp["poster"][0]
        self.assertEqual(forsta["rubrik"], "Utbyggnad av Åsaskolan")
        self.assertEqual(forsta["adress"], "ks-motet.html#punkt-1")
        self.assertEqual(forsta["om"], ["Punkt 1", "Dnr KS-2026-00001"])
        self.assertEqual(forsta["traff"], "utbyggnad av åsaskolan ks-2026-00001")
        self.assertIn("skolan ska byggas ut för fler elever.", forsta["text"])

    def test_utan_mote_eller_kallelse_bara_arendena(self):
        self.assertEqual(len(index([])["grupper"]), 1)
        self.assertEqual(len(index([], kommande(POOL, date(2026, 10, 1)))["grupper"]), 1)


if __name__ == "__main__":
    unittest.main()
