"""K1, K4 och K10: ett ärende läses enligt formatet eller stoppar bygget."""

import unittest
from datetime import date

from webbplats.arende import tolka
from webbplats.kontroll import kontrollera

ORTER = ["Åsa", "Fjärås"]
ARENDE = """---
rubrik: Ny förskola
ort: Åsa, Fjärås
organ: Nämnden
status: pågår
---

Två meningar
om ärendet.

## Händelser

- 2026-03-02 · beslut · Nämnden beslutade. · [Protokoll § 2](https://example.org/b#sida-2)
- 2025-01-05 · forslag · Ett förslag. · [Handling](https://example.org/a)

## I media och debatt

- 2026-03-03 · [Rubrik](https://example.org/m) · Norra Halland
"""


def andrat(gammalt: str, nytt: str) -> str:
    return ARENDE.replace(gammalt, nytt)


class Tolka(unittest.TestCase):
    def test_falt_ingress_handelser_och_media(self):
        arende = tolka("bevakning/ks/2025-01-05-ny-forskola.md", ARENDE)
        self.assertEqual(arende.id, "2025-01-05-ny-forskola")
        self.assertEqual(arende.orter, ["Åsa", "Fjärås"])
        self.assertEqual(arende.ingress, "Två meningar om ärendet.")
        forsta = arende.handelser[0]
        self.assertEqual((forsta.datum, forsta.steg), (date(2026, 3, 2), "beslut"))
        self.assertEqual(forsta.kalla, "Protokoll § 2")
        self.assertEqual(forsta.lank, "https://example.org/b#sida-2")
        self.assertEqual(arende.media[0].var, "Norra Halland")
        kontrollera(arende, ORTER)

    def test_formatfel_stoppar(self):
        fel = [
            andrat("status: pågår\n", "status: pågår\nfarg: blå\n"),
            andrat("organ: Nämnden\n", ""),
            andrat("organ: Nämnden", "organ Nämnden"),
            andrat("· beslut ·", "· besluten ·"),
            andrat("(https://example.org/a)", "(http://example.org/a)"),
            andrat("2026-03-02 ·", "2026-13-02 ·"),
            andrat(" · Norra Halland", ""),
            ARENDE.removeprefix("---\n"),
        ]
        for text in fel:
            with self.subTest(text=text), self.assertRaises(ValueError):
                tolka("x.md", text)


class Kontrollera(unittest.TestCase):
    def test_fel_mot_repots_filer_stoppar(self):
        fel = [
            andrat("status: pågår", "status: oklart"),
            andrat("ort: Åsa, Fjärås", "ort: Åsa, Onsala"),
            andrat("- 2026-03-02", "- 2024-03-02"),
            andrat("status: pågår", "status: pågår\nsynpunkter_senast: snart"),
            ARENDE.split("## Händelser")[0],
        ]
        for text in fel:
            with self.subTest(text=text), self.assertRaises(ValueError):
                kontrollera(tolka("x.md", text), ORTER)


if __name__ == "__main__":
    unittest.main()
