"""K1, K4, K10, K22 och K25: ett ärende och OMRADE.md läses enligt formatet eller stoppar bygget."""

import unittest
from datetime import date

from webbplats.arende import tolka
from webbplats.kontroll import kontrollera, kontrollera_omrade

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


FEL_STEG = "- 2026-12-01 · forslag · X. · [K](https://example.org/k)"


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
            andrat("## I media och debatt", "## I media"),
            andrat("## I media", f"## Tycka till\n\n{FEL_STEG}\n\n## I media"),
        ]
        for text in fel:
            with self.subTest(text=text), self.assertRaises(ValueError):
                tolka("x.md", text)


HANDLINGAR = (
    " · Handlingar: [Tjänsteskrivelse, förslag](https://example.org/b#sida-5), "
    "[Karta](https://example.org/k.pdf#page=9)"
)
FORSLAGET = "## Förslaget i korthet\n\n- Omkring 40 bostäder. · [Planprogrammet s. 2](https://example.org/p)\n\n"


class Handlingarna(unittest.TestCase):
    def test_handlingarna_efter_kallan_och_forslaget_i_korthet(self):
        text = andrat("(https://example.org/b#sida-2)", "(https://example.org/b#sida-2)" + HANDLINGAR)
        arende = tolka("x.md", text.replace("## Händelser", FORSLAGET + "## Händelser"))
        self.assertEqual(
            arende.handelser[0].handlingar,
            (
                ("Tjänsteskrivelse, förslag", "https://example.org/b#sida-5"),
                ("Karta", "https://example.org/k.pdf#page=9"),
            ),
        )
        self.assertEqual(arende.handelser[1].handlingar, ())
        punkt = arende.forslaget[0]
        self.assertEqual((punkt.text, punkt.kalla), ("Omkring 40 bostäder.", "Planprogrammet s. 2"))

    def test_handlingar_som_inte_ar_lankar_stoppar(self):
        for svans in (" · [K](https://example.org/k)", " · Handlingar: Karta", " · Handlingar: [K](http://x.org)"):
            with self.subTest(svans=svans), self.assertRaises(ValueError):
                tolka("x.md", andrat("(https://example.org/a)", "(https://example.org/a)" + svans))


class Kontrollera(unittest.TestCase):
    def test_fel_mot_repots_filer_stoppar(self):
        fel = [
            andrat("status: pågår", "status: oklart"),
            andrat("ort: Åsa, Fjärås", "ort: Åsa, Onsala"),
            andrat("- 2026-03-02", "- 2024-03-02"),
            ARENDE.split("## Händelser")[0],
        ]
        for text in fel:
            with self.subTest(text=text), self.assertRaises(ValueError):
                kontrollera(tolka("x.md", text), ORTER)

    def test_ort_under_tva_foreningar_eller_forening_utan_orter_stoppar(self):
        for foreningar in (
            {"Förening A": ["Åsa"], "Förening B": ["Åsa", "Särö"]},
            {"Förening A": ["Åsa"], "Förening B": []},
            {},
        ):
            with self.subTest(foreningar=foreningar), self.assertRaises(ValueError):
                kontrollera_omrade(foreningar)

    def test_varje_ort_under_en_forening_gar_igenom(self):
        kontrollera_omrade({"Förening A": ["Åsa"], "Förening B": ["Särö"]})


if __name__ == "__main__":
    unittest.main()
