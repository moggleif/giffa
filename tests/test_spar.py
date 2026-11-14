"""K30: två spår med var sitt tecken och var sin färg."""

import re
import unittest
from pathlib import Path

from webbplats.spar import spar, tecken

STIL = (Path(__file__).resolve().parent.parent / "docs/stil.css").read_text(encoding="utf-8")


def farg(valjare: str) -> str:
    return re.search(rf"{re.escape(valjare)} \{{ color: var\(--(\w+)\)", STIL).group(1)


class Spar(unittest.TestCase):
    def test_samrad_och_granskning_for_alla_resten_for_partierna(self):
        self.assertEqual([spar(s) for s in ("samrad", "granskning")], ["alla", "alla"])
        for steg in ("forslag", "yttrande", "beslut", "vantas", "info"):
            self.assertEqual(spar(steg), "partiet")

    def test_tecknet_har_text_for_skarmlasare(self):
        self.assertIn('<span class="dold">Tycka till för alla: </span>', tecken("alla"))
        self.assertIn('<span class="dold">Diskutera i partiet: </span>', tecken("partiet"))
        self.assertNotEqual(tecken("alla").split("<svg")[1], tecken("partiet").split("<svg")[1])

    def test_samma_farg_for_spaaret_overallt_och_egen_for_uppmarksammat(self):
        self.assertEqual(farg(".tecken.alla"), "alla")
        self.assertEqual(farg(".tecken.partiet"), "partiet")
        self.assertEqual(farg(".steg.samrad, .steg.granskning"), "alla")
        self.assertEqual(farg(".steg.forslag, .steg.yttrande, .steg.info"), "partiet")
        varden = dict(re.findall(r"--(alla|partiet|lyft): (#[0-9a-f]{6})", STIL))
        self.assertEqual(len(set(varden.values())), 3)


if __name__ == "__main__":
    unittest.main()
