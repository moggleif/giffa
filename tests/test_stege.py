"""K33: processtegen för planerna, med spåret för varje steg och bara det händelserna säger."""

import re
import unittest
from datetime import date

from tests.test_arende import ARENDE
from webbplats.arende import tolka
from webbplats.stege import stege

IDAG = date(2026, 11, 10)
HANDELSER = """## Händelser

- 2026-05-26 · granskning · Granskningen pågick. · [T](https://example.org/g)
- 2026-02-19 · samrad · Samråd. · [P](https://example.org/s)
- 2025-01-16 · forslag · Uppdrag att upprätta planen. · [P](https://example.org/u)

## Tycka till

- 2026-11-17 · beslut · Nämnden föreslås anta detaljplanen. · [Kallelse](https://example.org/k)

"""


def byggt(rubrik: str, handelser: str = HANDELSER, status: str = "pågår") -> object:
    text = ARENDE.replace("rubrik: Ny förskola", f"rubrik: {rubrik}").replace("status: pågår", f"status: {status}")
    text = text.split("## Händelser")[0] + handelser + "## I media" + text.split("## I media")[1]
    return tolka("bevakning/detaljplaner/d.md", text)


def med(rad: str, handelser: str = HANDELSER) -> str:
    return handelser.replace("## Händelser\n\n", f"## Händelser\n\n{rad}\n")


def steg(html: str) -> list[tuple[str, str, str, str]]:
    return re.findall(r'<li class="(\w+) (\w+)">.*?<strong>(\w+)</strong> <small>(.*?)</small>', html)


class Processtegen(unittest.TestCase):
    def test_detaljplan_gjort_nu_och_kommande_med_datum(self):
        self.assertEqual(
            steg(stege(byggt("Detaljplan för bostäder"), IDAG)),
            [
                ("gjord", "partiet", "Uppdrag", 'gjort, <time datetime="2025-01-16">16 januari 2025</time>'),
                ("gjord", "alla", "Samråd", 'gjort, <time datetime="2026-02-19">19 februari 2026</time>'),
                ("nu", "alla", "Granskning", 'nu, <time datetime="2026-05-26">26 maj 2026</time>'),
                ("kommande", "partiet", "Antagande", 'kommer, <time datetime="2026-11-17">17 november 2026</time>'),
            ],
        )
        self.assertIn("standardförfarande", stege(byggt("Detaljplan för bostäder"), IDAG))

    def test_planprogram_andring_och_ovrigt(self):
        program = steg(stege(byggt("Planprogram för X"), IDAG))
        self.assertEqual([s[2] for s in program], ["Uppdrag", "Samråd", "Godkännande"])
        andring = steg(stege(byggt("Ändring av detaljplan för Z"), IDAG))
        self.assertEqual([s[2] for s in andring], ["Uppdrag", "Samråd", "Granskning", "Antagande"])
        self.assertEqual(stege(byggt("Planbesked för Y"), IDAG), "")
        self.assertEqual(stege(byggt("Ny förskola"), IDAG), "")

    def test_andra_beslut_med_ordet_anta_ar_inte_antagandet(self):
        for text in (
            "KS godkände exploateringsavtalet som krävs innan nämnden kan anta planen.",
            "Nämnden överlämnade planen till fullmäktige för antagande.",
        ):
            html = stege(byggt("Detaljplan för P", med(f"- 2026-10-20 · beslut · {text} · [P](https://example.org/e)")), IDAG)
            self.assertRegex(html, r'<li class="nu alla">.+?<strong>Granskning</strong>')
        antog = med("- 2026-10-20 · beslut · Kommunfullmäktige antog detaljplanen. · [P](https://example.org/a)")
        self.assertRegex(stege(byggt("Detaljplan för P", antog), IDAG), r'<li class="nu partiet">.+?<strong>Antagande</strong>')

    def test_ett_annat_tillfalle_ar_inte_antagandet(self):
        html = stege(byggt("Detaljplan för P", HANDELSER.replace("föreslås anta detaljplanen", "ska besluta om principavtalet")), IDAG)
        self.assertIn("<strong>Antagande</strong> <small>inget i källorna än</small>", html)
        foreslag = HANDELSER.replace("Nämnden föreslås anta", "Utskottet föreslås föreslå att nämnden antar")
        html = stege(byggt("Detaljplan för P", foreslag), IDAG)
        self.assertIn("<strong>Antagande</strong> <small>inget i källorna än</small>", html)

    def test_ett_steg_utan_egen_handelse_sags_inte_vara_gjort(self):
        utan = HANDELSER.replace("- 2026-02-19 · samrad · Samråd. · [P](https://example.org/s)\n", "")
        html = stege(byggt("Detaljplan för T", utan), IDAG)
        self.assertIn('<li class="tidigare alla">', html)
        self.assertIn("<strong>Samråd</strong> <small>ingen händelse i källorna</small>", html)

    def test_okant_lage_star_som_okant(self):
        bara = "## Händelser\n\n- 2023-10-26 · forslag · Nämnden ger uppdrag att genomföra granskning. · [P](https://example.org/p)\n\n"
        bara += "## Tycka till\n\n- 2026-11-19 · beslut · Nämnden ska besluta om uppdraget att upprätta planen. · [K](https://example.org/k)\n\n"
        html = stege(byggt("Detaljplan för V", bara), IDAG)
        self.assertIn("Var planen står går inte att läsa ut ur händelserna.", html)
        self.assertEqual(
            [(s[0], s[2], s[3]) for s in steg(html)][:2],
            [("okand", "Uppdrag", 'kommer, <time datetime="2026-11-19">19 november 2026</time>'), ("okand", "Samråd", "")],
        )

    def test_ett_upphavt_antagande(self):
        upphavt = med(
            "- 2026-09-01 · info · Domen överklagades; den upphävde planen. · [O](https://example.org/o)\n"
            "- 2026-08-15 · info · Länsstyrelsen upphävde antagandet. · [L](https://example.org/l)\n"
            "- 2026-08-01 · beslut · KF antog detaljplanen. · [P](https://example.org/a)"
        )
        html = stege(byggt("Detaljplan för U", upphavt), IDAG)
        self.assertIn('<time datetime="2026-08-15">15 augusti 2026</time>: Länsstyrelsen upphävde antagandet.', html)
        self.assertIn("Stegen visar planen fram till upphävandet.", html)
        self.assertRegex(html, r'<li class="nu partiet">.+?<strong>Antagande</strong>')
        omstart = med("- 2026-10-01 · granskning · Ny granskning. · [G](https://example.org/n)", upphavt)
        html = stege(byggt("Detaljplan för U", omstart), IDAG)
        self.assertIn("Stegen visar det som hänt sedan dess.", html)
        self.assertRegex(html, r'<li class="nu alla">.+?<strong>Granskning</strong>')

    def test_bara_pagaende(self):
        self.assertEqual(stege(byggt("Detaljplan för B", status="beslutat"), IDAG), "")


if __name__ == "__main__":
    unittest.main()
