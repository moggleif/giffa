"""K25: handlingarna intill steget och förslaget i korthet på ärendets sida."""

import unittest

from tests.test_arende import ARENDE, FORSLAGET, HANDLINGAR
from tests.test_sidor import RUNDA, SAJT, arende
from webbplats.arende import tolka
from webbplats.arendesida import arendesida
from webbplats.sidor import startsida


class HandlingarnaPaSidan(unittest.TestCase):
    def test_handlingarna_intill_steget_och_forslaget_overst(self):
        text = ARENDE.replace("(https://example.org/a)", "(https://example.org/a)" + HANDLINGAR)
        text = text.replace("## Händelser", FORSLAGET + "## Händelser")
        html = arendesida(SAJT, tolka("bevakning/ks/h.md", text))
        steget = html.split("Ett förslag. ")[1].split("</li>")[0]
        self.assertIn('<strong>Handlingar:</strong> <a href="https://example.org/b#sida-5">', steget)
        self.assertIn('<a href="https://example.org/k.pdf#page=9">Karta</a>', steget)
        self.assertLess(html.index("Förslaget i korthet"), html.index("<h2>Händelser"))
        self.assertIn('Omkring 40 bostäder. <a href="https://example.org/p">', html)

    def test_utan_handlingar_ingen_rad(self):
        html = arendesida(SAJT, arende("pågår"))
        self.assertNotIn("Handlingar:", html)
        self.assertNotIn("Förslaget i korthet", html)

    def test_handlingarna_ocksa_under_tycka_till_nu_och_nytt(self):
        tillfalle = "- 2026-12-01 · beslut · Nämnden beslutar. · [Kallelse](https://example.org/k)" + HANDLINGAR
        text = ARENDE.replace("## I media", f"## Tycka till\n\n{tillfalle}\n\n## I media")
        text = text.replace("(https://example.org/b#sida-2)", "(https://example.org/b#sida-2)" + HANDLINGAR)
        html = startsida(SAJT, [tolka("bevakning/ks/h.md", text)], RUNDA)
        self.assertEqual(html.count("<strong>Handlingar:</strong>"), 2)
