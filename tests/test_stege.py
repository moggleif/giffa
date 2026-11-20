"""K33: processtegen för planerna, med läget för varje steg och bara det händelserna säger."""

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
    return re.findall(r'<li class="(\w+)"><span aria-hidden="true">(.)</span> <strong>(\w+)</strong> <small>(.*?)</small>', html)


class Processtegen(unittest.TestCase):
    def test_detaljplan_gjort_nu_och_kommande_med_datum(self):
        self.assertEqual(
            steg(stege(byggt("Detaljplan för bostäder"), IDAG)),
            [
                ("gjord", "✓", "Uppdrag", 'klart, <time datetime="2025-01-16">16 januari 2025</time>'),
                ("gjord", "✓", "Samråd", 'klart, <time datetime="2026-02-19">19 februari 2026</time>'),
                ("nu", "●", "Granskning", 'nu, <time datetime="2026-05-26">26 maj 2026</time>'),
                ("nasta", "→", "Antagande", 'nästa, <time datetime="2026-11-17">17 november 2026</time>'),
            ],
        )
        html = stege(byggt("Detaljplan för bostäder"), IDAG)
        self.assertIn("<p>Var planen står</p>", html)
        self.assertIn("Stegen i plan- och bygglagen</a>", html)

    def test_nasta_steg_och_senare_steg(self):
        bara = "## Händelser\n\n- 2025-08-26 · forslag · Kommunstyrelsen godkände projektbeställning gällande planprogrammet. · [P](https://example.org/p)\n\n"
        self.assertEqual(
            [(s[0], s[1], s[3]) for s in steg(stege(byggt("Detaljplan för N", bara), IDAG))],
            [
                ("nu", "●", 'nu, <time datetime="2025-08-26">26 augusti 2025</time>'),
                ("nasta", "→", "nästa, inget datum än"),
                ("kommande", "○", "inget datum än"),
                ("kommande", "○", "inget datum än"),
            ],
        )

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
            self.assertRegex(html, r'<li class="nu">.+?<strong>Granskning</strong>')
        antog = med("- 2026-10-20 · beslut · Kommunfullmäktige antog detaljplanen. · [P](https://example.org/a)")
        self.assertRegex(stege(byggt("Detaljplan för P", antog), IDAG), r'<li class="gjord">.+?<strong>Antagande</strong>')

    def test_ett_annat_tillfalle_ar_inte_antagandet(self):
        html = stege(byggt("Detaljplan för P", HANDELSER.replace("föreslås anta detaljplanen", "ska besluta om principavtalet")), IDAG)
        self.assertIn("<strong>Antagande</strong> <small>nästa, inget datum än</small>", html)
        foreslag = HANDELSER.replace("Nämnden föreslås anta", "Utskottet föreslås föreslå att nämnden antar")
        html = stege(byggt("Detaljplan för P", foreslag), IDAG)
        self.assertIn("<strong>Antagande</strong> <small>nästa, inget datum än</small>", html)

    def test_ett_steg_utan_egen_handelse_sags_inte_vara_gjort(self):
        utan = HANDELSER.replace("- 2026-02-19 · samrad · Samråd. · [P](https://example.org/s)\n", "")
        html = stege(byggt("Detaljplan för T", utan), IDAG)
        self.assertIn('<li class="tidigare"><span aria-hidden="true">✓</span> <strong>Samråd</strong> <small>passerat</small>', html)
        kallat = utan.replace("## Tycka till\n\n", "## Tycka till\n\n- 2026-12-01 · samrad · Samråd. · [K](https://example.org/k)\n")
        self.assertIn("<strong>Samråd</strong> <small>passerat</small>", stege(byggt("Detaljplan för T", kallat), IDAG))

    def test_okant_lage_star_som_okant(self):
        bara = "## Händelser\n\n- 2023-10-26 · forslag · Nämnden ger uppdrag att genomföra granskning. · [P](https://example.org/p)\n\n"
        bara += "## Tycka till\n\n- 2026-11-19 · beslut · Nämnden ska besluta om uppdraget att upprätta planen. · [K](https://example.org/k)\n\n"
        html = stege(byggt("Detaljplan för V", bara), IDAG)
        self.assertIn("<p>Var planen står: okänt</p>", html)
        self.assertEqual(
            [(s[0], s[1], s[2], s[3]) for s in steg(html)][:2],
            [("okand", "○", "Uppdrag", 'kommer, <time datetime="2026-11-19">19 november 2026</time>'), ("okand", "○", "Samråd", "")],
        )

    def test_en_antagen_plan_ar_klar_och_visar_vad_som_hant_sedan(self):
        antog = med(
            "- 2026-10-01 · forslag · KSAU föreslog ny part i exploateringsavtalet. · [E](https://example.org/e)\n"
            "- 2026-09-15 · info · Detaljplanen fick laga kraft. · [L](https://example.org/l)\n"
            "- 2026-08-01 · beslut · Byggnadsnämnden antog detaljplanen. · [A](https://example.org/a)",
            HANDELSER.split("## Tycka till")[0],
        )
        html = stege(byggt("Detaljplan för K", antog), IDAG)
        self.assertEqual(steg(html)[-1], ("gjord", "✓", "Antagande", 'klart, <time datetime="2026-08-01">1 augusti 2026</time>'))
        self.assertIn('<p>Var planen står: antagen, laga kraft <time datetime="2026-09-15">15 september 2026</time></p>', html)
        self.assertIn('<strong>Senast, <time datetime="2026-10-01">1 oktober 2026</time>:</strong> KSAU föreslog ny part i exploateringsavtalet.', html)
        html = stege(byggt("Detaljplan för K", antog + "## Tycka till\n\n- 2026-11-24 · vantas · KS väntas besluta om partsbytet. · [K](https://example.org/k)\n\n"), IDAG)
        self.assertIn('<strong>Härnäst, <time datetime="2026-11-24">24 november 2026</time>:</strong> KS väntas besluta om partsbytet.', html)

    def test_ett_upphavt_antagande(self):
        upphavt = med(
            "- 2026-09-01 · info · Domen överklagades; den upphävde planen. · [O](https://example.org/o)\n"
            "- 2026-08-15 · info · Länsstyrelsen upphävde antagandet. · [L](https://example.org/l)\n"
            "- 2026-08-01 · beslut · KF antog detaljplanen. · [P](https://example.org/a)"
        )
        html = stege(byggt("Detaljplan för U", upphavt), IDAG)
        self.assertIn('<time datetime="2026-08-15">15 augusti 2026</time>: Länsstyrelsen upphävde antagandet.', html)
        self.assertIn("Stegen visar planen fram till upphävandet.", html)
        self.assertNotIn("Var planen står: antagen", html)
        self.assertRegex(html, r'<li class="nu">.+?<strong>Antagande</strong>')
        omstart = med("- 2026-10-01 · granskning · Ny granskning. · [G](https://example.org/n)", upphavt)
        html = stege(byggt("Detaljplan för U", omstart), IDAG)
        self.assertIn("Stegen visar det som hänt sedan dess.", html)
        self.assertRegex(html, r'<li class="nu">.+?<strong>Granskning</strong>')

    def test_bara_pagaende(self):
        self.assertEqual(stege(byggt("Detaljplan för B", status="beslutat"), IDAG), "")


if __name__ == "__main__":
    unittest.main()
