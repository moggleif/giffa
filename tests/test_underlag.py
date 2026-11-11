"""K6, K8 och K22: föreningarna, orterna, platserna, källorna och förra rundan ur repots filer."""

import unittest
from datetime import date

from webbplats import underlag


class Underlag(unittest.TestCase):
    def test_foreningarna_och_orterna_fore_platserna(self):
        omrade = (
            "# Område\n\nText.\n\n## Förening A\n\n- Åsa\n- Fjärås\n\n"
            "## Förening B\n\n- Särö\n\nText.\n\n## Platser\n\n- Inte en ort\n"
        )
        self.assertEqual(
            underlag.foreningar(omrade), {"Förening A": ["Åsa", "Fjärås"], "Förening B": ["Särö"]}
        )
        self.assertEqual(underlag.orter(omrade), ["Åsa", "Fjärås", "Särö"])

    def test_kallorna_ur_tabellen(self):
        kallor = "| Källa | Vad | Adress |\n| -- | -- | -- |\n| A | ger | https://a |\n\nText.\n"
        self.assertEqual(underlag.kallor(kallor), [["A", "ger", "https://a"]])

    def test_senaste_rundan_ar_sista_raden(self):
        rundor = "fran,till,anteckning\n2026-09-01,2026-09-30,\n2026-10-01,2026-10-31,Delvis\n"
        self.assertEqual(
            underlag.senaste_runda(rundor),
            underlag.Runda(date(2026, 10, 1), date(2026, 10, 31), "Delvis"),
        )

    def test_utan_runda_stoppar(self):
        with self.assertRaises(ValueError):
            underlag.senaste_runda("fran,till,anteckning\n")


if __name__ == "__main__":
    unittest.main()
