"""K33: processtegen för pågående ärenden, med spåret för varje steg."""

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
- 2025-01-16 · forslag · Uppdrag. · [P](https://example.org/u)

## Tycka till

- 2026-11-17 · beslut · Antagandet. · [Kallelse](https://example.org/k)

"""


def plan(rubrik: str = "Detaljplan för bostäder", status: str = "pågår") -> object:
    text = ARENDE.replace("rubrik: Ny förskola", f"rubrik: {rubrik}").replace("pågår", status)
    text = text.split("## Händelser")[0] + HANDELSER + "## I media" + text.split("## I media")[1]
    return tolka("bevakning/detaljplaner/d.md", text)


def byggt(rubrik: str, handelser: str) -> str:
    text = ARENDE.replace("rubrik: Ny förskola", f"rubrik: {rubrik}")
    return text.split("## Händelser")[0] + handelser + "## I media" + text.split("## I media")[1]


def steg(html: str) -> list[tuple[str, str, str, str]]:
    return re.findall(r'<li class="(\w+) (\w+)">.*?<strong>(\w+)</strong> <small>(.*?)</small>', html)


class Processtegen(unittest.TestCase):
    def test_detaljplan_gjort_nu_och_kommande_med_datum(self):
        self.assertEqual(
            steg(stege(plan(), IDAG)),
            [
                ("gjord", "partiet", "Uppdrag", 'gjort, <time datetime="2025-01-16">16 januari 2025</time>'),
                ("gjord", "alla", "Samråd", 'gjort, <time datetime="2026-02-19">19 februari 2026</time>'),
                ("nu", "alla", "Granskning", 'nu, <time datetime="2026-05-26">26 maj 2026</time>'),
                ("kommande", "partiet", "Antagande", 'kommer, <time datetime="2026-11-17">17 november 2026</time>'),
            ],
        )
        self.assertIn("standardförfarande", stege(plan(), IDAG))

    def test_planprogram_och_ovrigt(self):
        program = steg(stege(plan("Planprogram för X"), IDAG))
        self.assertEqual([s[2] for s in program], ["Uppdrag", "Samråd", "Godkännande"])
        ovrigt = stege(plan("Ny förskola"), IDAG)
        self.assertEqual([s[2] for s in steg(ovrigt)], ["Beredning", "Beslut"])
        andring = steg(stege(plan("Ändring av detaljplan för Z"), IDAG))
        self.assertEqual([s[2] for s in andring], ["Uppdrag", "Samråd", "Granskning", "Antagande"])
        self.assertNotIn("standardförfarande", ovrigt)

    def test_kommande_utan_tillfalle_ar_inte_kant(self):
        text = ARENDE.replace("rubrik: Ny förskola", "rubrik: Detaljplan för Y")
        html = stege(tolka("bevakning/detaljplaner/y.md", text), IDAG)
        self.assertIn("<strong>Samråd</strong> <small>kommer, datum inte känt än</small>", html)

    def test_antagandet_ar_ett_beslut_om_att_planen_antogs(self):
        avtal = "- 2026-10-20 · beslut · KS godkände exploateringsavtalet. · [P](https://example.org/e)\n"
        text = ARENDE.replace("rubrik: Ny förskola", "rubrik: Detaljplan för Z")
        text = text.split("## Händelser")[0] + HANDELSER.replace("## Händelser\n\n", "## Händelser\n\n" + avtal)
        html = stege(tolka("bevakning/detaljplaner/z.md", text + "## I media" + ARENDE.split("## I media")[1]), IDAG)
        self.assertIn('<li class="kommande partiet">', html)
        antog = text.replace("KS godkände exploateringsavtalet.", "Kommunfullmäktige antog detaljplanen.")
        html = stege(tolka("bevakning/detaljplaner/z.md", antog + "## I media" + ARENDE.split("## I media")[1]), IDAG)
        self.assertRegex(html, r'<li class="nu partiet">.+?<strong>Antagande</strong> <small>nu,')

    def test_en_plan_som_borjat_om_star_pa_sitt_nya_steg(self):
        gammalt = "- 2022-10-18 · beslut · KF antog detaljplanen. · [P](https://example.org/a)\n"
        text = ARENDE.replace("rubrik: Ny förskola", "rubrik: Detaljplan för Z")
        text = text.split("## Händelser")[0] + HANDELSER.replace("(https://example.org/u)\n", "(https://example.org/u)\n" + gammalt)
        html = stege(tolka("bevakning/detaljplaner/z.md", text + "## I media" + ARENDE.split("## I media")[1]), IDAG)
        self.assertRegex(html, r'<li class="nu alla">.+?<strong>Granskning</strong>')
        self.assertRegex(html, r'<li class="kommande partiet">.+?<strong>Antagande</strong>')

    def test_ett_annat_beslut_ar_inte_antagandet(self):
        text = HANDELSER.replace("Antagandet.", "Principavtalet.")
        html = stege(tolka("bevakning/detaljplaner/p.md", byggt("Detaljplan för P", text)), IDAG)
        self.assertIn("<strong>Antagande</strong> <small>kommer, datum inte känt än</small>", html)

    def test_uppdraget_som_tillfalle_och_utan_datum(self):
        bara = "## Händelser\n\n- 2022-12-13 · forslag · Planbesked. · [P](https://example.org/p)\n\n"
        bara += "## Tycka till\n\n- 2026-11-19 · beslut · Nämnden ska besluta om uppdraget. · [K](https://example.org/k)\n\n"
        html = stege(tolka("bevakning/ks/v.md", byggt("Detaljplan för V", bara)), IDAG)
        self.assertIn('<strong>Uppdrag</strong> <small>nu, <time datetime="2026-11-19">', html)
        uppdrag = bara.split("## Tycka till")[0]
        html = stege(tolka("bevakning/ks/v.md", byggt("Detaljplan för V", uppdrag)), IDAG)
        self.assertIn("<strong>Uppdrag</strong> <small>nu, inget datum i källorna</small>", html)

    def test_ett_upphavt_antagande_raknas_inte(self):
        text = HANDELSER.replace(
            "## Händelser\n\n",
            "## Händelser\n\n- 2026-09-01 · info · Länsstyrelsen upphävde antagandet. · [L](https://example.org/l)\n"
            "- 2026-08-01 · beslut · KF antog detaljplanen. · [P](https://example.org/a)\n",
        )
        html = stege(tolka("bevakning/detaljplaner/u.md", byggt("Detaljplan för U", text)), IDAG)
        self.assertIn("Länsstyrelsen upphävde antagandet.", html)
        self.assertIn("Stegen visar planen fram till upphävandet.", html)
        self.assertRegex(html, r'<li class="nu partiet">.+?<strong>Antagande</strong>')
        omstart = text.replace(
            "## Händelser\n\n", "## Händelser\n\n- 2026-10-01 · forslag · Uppdrag att återuppta. · [P](https://example.org/o)\n"
        )
        html = stege(tolka("bevakning/detaljplaner/u.md", byggt("Detaljplan för U", omstart)), IDAG)
        self.assertIn("Stegen visar det som hänt sedan dess.", html)
        self.assertRegex(html, r'<li class="nu partiet">.+?<strong>Uppdrag</strong>')

    def test_bara_pagaende(self):
        self.assertEqual(stege(plan(status="beslutat"), IDAG), "")


if __name__ == "__main__":
    unittest.main()
