"""K4–K9, K12 och K14: tabellen, korten, startsidan, historiken, sidan om
bevakningen, tillfällena att tycka till och läsbarheten."""

import re
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from tests.test_arende import ARENDE
from webbplats.arende import tolka
from webbplats.bevakar import bevakar
from webbplats.ikoner import BETYDER
from webbplats.mall import Sajt
from webbplats.sidor import historik, startsida
from webbplats.underlag import Runda

SAJT = Sajt(
    "https://github.com/agare/giffa",
    datetime(2026, 11, 10, 6, 0, tzinfo=timezone.utc),
    ["Åsa", "Fjärås"],
)
RUNDA = Runda(date(2026, 3, 1), date(2026, 3, 31), "Startärenden.")


def arende(status: str, namn: str = "a") -> object:
    return tolka(f"bevakning/ks/{namn}.md", ARENDE.replace("status: pågår", f"status: {status}"))


def paverkbart(namn: str) -> object:
    tillfallen = (
        "## Tycka till\n\n"
        "- 2026-12-01 · granskning · Granskningen. · [Underrättelse](https://example.org/g)\n"
        "- 2026-11-10 · beslut · Nämnden beslutar. · [Kallelse](https://example.org/k)\n"
        "- 2026-11-24 · vantas · KS väntas besluta. · [Kalendern](https://example.org/c)\n"
        "- 2026-11-09 · beslut · Passerat. · [Kallelse](https://example.org/p)\n\n"
    )
    text = ARENDE.replace("## I media och debatt", tillfallen + "## I media och debatt")
    return tolka(f"bevakning/ks/{namn}.md", text)


class Startsidan(unittest.TestCase):
    def test_pagar_och_beslutat_men_inte_historiken(self):
        html = startsida(
            SAJT, [arende("pågår", "p"), arende("beslutat", "b"), arende("klart", "k")], RUNDA
        )
        self.assertLess(html.index("<h2>Pågår</h2>"), html.index('id="p"'))
        self.assertLess(html.index("<h2>Beslutat</h2>"), html.index('id="b"'))
        self.assertNotIn('id="k"', html)

    def test_tabellens_ar_ikoner_och_lank_till_kortet(self):
        html = startsida(SAJT, [arende("pågår", "p")], RUNDA)
        for ar in ("2025", "2026"):
            self.assertIn(f'<th scope="col">{ar}</th>', html)
        self.assertIn('<a href="#p">Ny förskola</a>', html)
        self.assertIn('class="steg beslut" href="https://example.org/b#sida-2"', html)
        self.assertIn('class="band start"', html)

    def test_kortet_har_historik_media_och_lank_till_repot(self):
        html = startsida(SAJT, [arende("pågår", "p")], RUNDA)
        self.assertIn("Läs mer: alla 2 händelser med källor", html)
        self.assertIn('<a href="https://example.org/m">Rubrik</a> – Norra Halland', html)
        self.assertIn('href="https://github.com/agare/giffa/blob/main/bevakning/ks/p.md"', html)

    def test_nytt_ar_handelserna_i_rundans_period(self):
        html = startsida(SAJT, [arende("klart", "k")], RUNDA)
        nytt = html[html.index('id="nytt"') :]
        self.assertIn("1 ny händelse", nytt)
        self.assertIn('href="historik.html#k"', nytt)
        self.assertNotIn("Ett förslag.", nytt)
        self.assertIn("1 mars 2026</time> till <time datetime=\"2026-03-31\">31 mars 2026</time>. Startärenden.", nytt)

    def test_urval_per_ort_ur_omrade(self):
        html = startsida(SAJT, [arende("pågår", "p")], RUNDA)
        self.assertIn('<button type="button" data-urval="Fjärås">Fjärås</button>', html)
        self.assertIn('<tr data-ort="Åsa|Fjärås">', html)
        self.assertIn('<article id="p" data-ort="Åsa|Fjärås">', html)

    def test_inget_nytt_sags(self):
        html = startsida(SAJT, [arende("pågår")], Runda(date(2027, 1, 1), date(2027, 1, 31), ""))
        self.assertIn("Inga nya händelser.", html)

    def test_tycka_till_nu_i_tur_och_ordning(self):
        html = startsida(SAJT, [paverkbart("s"), arende("pågår", "p")], RUNDA)
        nu = html[html.index('id="tycka-till"') : html.index('id="nytt"')]
        self.assertLess(nu.index("Beslut <time datetime=\"2026-11-10\">tisdag 10 november 2026</time>, i dag"), nu.index("synpunkter senast"))
        self.assertIn('<a href="#s">Ny förskola</a>', nu)
        self.assertNotIn("2026-11-09", html)
        self.assertIn("1 december 2026</time>, om 21 dagar", nu)
        self.assertIn("Så kan du påverka, steg för steg", nu)

    def test_markering_pa_kort_och_rad(self):
        html = startsida(SAJT, [paverkbart("s")], RUNDA)
        self.assertIn('<small class="paverka">Tycka till <time datetime="2026-11-10">10 november 2026</time></small>', html)
        kortet = html[html.index('<article id="s"') :]
        self.assertIn('<div class="paverka"><p>Tycka till</p>', kortet)
        self.assertIn("Granskning – synpunkter senast <time datetime=\"2026-12-01\">tisdag 1 december 2026", kortet)
        self.assertIn("Beslut väntas, preliminärt <time datetime=\"2026-11-24\">tisdag 24 november 2026", kortet)

    def test_vantat_beslut_markeras_preliminart_i_tabellen(self):
        rader = "## Tycka till\n\n- 2026-11-24 · vantas · X. · [K](https://example.org/c)\n\n"
        text = ARENDE.replace("## I media", rader + "## I media")
        html = startsida(SAJT, [tolka("bevakning/ks/v.md", text)], RUNDA)
        self.assertIn("24 november 2026</time> (preliminärt)</small>", html)

    def test_inga_tillfallen_sags(self):
        html = startsida(SAJT, [arende("pågår")], RUNDA)
        self.assertIn("Inga kända tillfällen.", html)
        self.assertNotIn('class="paverka"', html)

    def test_sidfoten_lankar_till_repot(self):
        html = startsida(SAJT, [], RUNDA)
        self.assertIn(
            '<footer><p>Källkod, ärenden och källor: <a href="https://github.com/agare/giffa">',
            html,
        )
        self.assertIn("<h2>Pågår</h2><p>Inga ärenden ännu.</p>", html)
        self.assertIn('Sidan byggdes <time datetime="2026-11-10">10 november 2026</time>', html)


class Lasbarhet(unittest.TestCase):
    def test_forsta_lanken_hoppar_till_innehallet(self):
        for html in (startsida(SAJT, [], RUNDA), historik(SAJT, [])):
            efter_body = html.split("<body>\n", 1)[1]
            self.assertTrue(efter_body.startswith('<a class="hoppa" href="#innehall">'))
            self.assertIn('<main id="innehall" tabindex="-1">', html)

    def test_text_minst_15_punkter_och_spalt_hogst_70_tecken(self):
        stil = (Path(__file__).resolve().parent.parent / "docs/stil.css").read_text()
        bas = 16 * float(re.search(r"html \{ font-size: ([0-9.]+)%", stil).group(1)) / 100
        self.assertEqual(bas, 18)
        storlekar = re.findall(r"font-size: ([0-9.]+)(\w+|%)", stil)
        self.assertEqual({enhet for _, enhet in storlekar}, {"%", "rem"})
        self.assertGreaterEqual(min(float(s) for s, e in storlekar if e == "rem") * bas, 15)
        spalt = float(re.search(r"ol\.tillfallen \{ max-width: ([0-9.]+)rem", stil).group(1))
        self.assertLessEqual(spalt * bas / 8.4, 70)


class Klarsprak(unittest.TestCase):
    def test_ikoner_kort_och_teckenforklaring_i_klartext(self):
        html = startsida(SAJT, [arende("pågår", "p")], RUNDA)
        self.assertIn("<strong>Samråd</strong> – samråd eller remiss: öppet för synpunkter.", html)
        self.assertIn("Senaste steget: beslut, <time", html)
        self.assertIn("<span>Pågått 2025–2026</span>", html)
        self.assertIn('aria-label="Beslut 2 mars 2026: Nämnden beslutade.', html)
        self.assertLess(html.index("<h2>Pågår</h2>"), html.index("Vad ikonerna betyder"))


    def test_teckenforklaringen_ar_densamma_som_formatets(self):
        readme = (Path(__file__).resolve().parent.parent / "bevakning/README.md").read_text()
        efter = readme.split("Stegen ger ikonen")[1]
        tabellen = next(b for b in efter.split("\n\n") if b.startswith("|"))
        rader = re.findall(r"^\| `(\w+)` +\| (.+?) +\|$", tabellen, re.M)
        self.assertEqual(dict(rader), BETYDER)


class Historiken(unittest.TestCase):
    def test_bara_klart_och_avbrutet(self):
        html = historik(SAJT, [arende("klart", "k"), arende("avbrutet", "x"), arende("pågår", "p")])
        self.assertIn('id="k"', html)
        self.assertIn('id="x"', html)
        self.assertNotIn('id="p"', html)


class Bevakar(unittest.TestCase):
    def test_orter_kallor_och_platser_ur_filerna(self):
        plats = {
            "namn": "Åsaskolan",
            "typ": "grundskola",
            "ort": "Åsa",
            "anteckning": "",
            "handlingar": "3",
            "exempel": "https://e/x",
        }
        html = bevakar(SAJT, [plats], [["Kommunen", "nyheter", "https://k.se"]])
        self.assertIn("<li>Fjärås</li>", html)
        self.assertIn('<a href="https://e/x">Åsaskolan</a>', html)
        self.assertIn('<a href="https://k.se">https://k.se</a>', html)
        self.assertIn("https://github.com/agare/giffa/blob/main/KALLOR.md", html)


if __name__ == "__main__":
    unittest.main()
