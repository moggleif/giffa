"""K6 och K8: orterna, platserna, källorna och förra rundan ur repots filer."""

import unittest
from datetime import date

from webbplats import underlag


class Underlag(unittest.TestCase):
    def test_orterna_ur_listan_fore_platserna(self):
        omrade = "# Område\n\n- Åsa\n- Fjärås\n\nText.\n\n## Platser\n\n- Inte en ort\n"
        self.assertEqual(underlag.orter(omrade), ["Åsa", "Fjärås"])

    def test_kallorna_ur_tabellen(self):
        kallor = "| Källa | Vad | Adress |\n| -- | -- | -- |\n| A | ger | https://a |\n\nText.\n"
        self.assertEqual(underlag.kallor(kallor), [["A", "ger", "https://a"]])

    def test_senaste_rundan_ar_sista_raden(self):
        rundor = "fran,till\n2026-09-01,2026-09-30\n2026-10-01,2026-10-31\n"
        self.assertEqual(underlag.senaste_runda(rundor), (date(2026, 10, 1), date(2026, 10, 31)))


if __name__ == "__main__":
    unittest.main()
