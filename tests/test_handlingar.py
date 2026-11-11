"""K25: handlingarna intill steget och förslaget i korthet på ärendets sida."""

import unittest

from tests.test_arende import ARENDE, FORSLAGET, HANDLINGAR
from tests.test_sidor import SAJT, arende
from webbplats.arende import tolka
from webbplats.arendesida import arendesida


class HandlingarnaPaSidan(unittest.TestCase):
    def test_handlingarna_intill_steget_och_forslaget_overst(self):
        text = ARENDE.replace("(https://example.org/a)", "(https://example.org/a)" + HANDLINGAR)
        text = text.replace("## Händelser", FORSLAGET + "## Händelser")
        html = arendesida(SAJT, tolka("bevakning/ks/h.md", text))
        steget = html.split("Ett förslag. ")[1].split("</li>")[0]
        self.assertIn('<strong>Handlingarna:</strong> <a href="https://example.org/b#sida-5">', steget)
        self.assertIn('<a href="https://example.org/k.pdf#page=9">Karta</a>', steget)
        self.assertLess(html.index("Förslaget i korthet"), html.index("<h2>Händelser"))
        self.assertIn('Omkring 40 bostäder. <a href="https://example.org/p">', html)

    def test_utan_handlingar_ingen_rad(self):
        html = arendesida(SAJT, arende("pågår"))
        self.assertNotIn("Handlingarna:", html)
        self.assertNotIn("Förslaget i korthet", html)
