"""K4–K9, K12, K14 och K16–K20: tabellen, korten, startsidan, historiken, sidan om
bevakningen, tillfällena att tycka till och läsbarheten."""

import re
import unittest
from datetime import date, datetime, timezone
from pathlib import Path

from tests.test_arende import ARENDE
from webbplats.arende import tolka
from webbplats.arendesida import arendesida
from webbplats.bevakar import bevakar
from webbplats.ikoner import BETYDER
from webbplats.mall import Sajt
from webbplats.paverka import SA_GOR
from webbplats.sidor import LISTOR, lista, startsida
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


def pagar(arenden: list) -> str:
    return lista(SAJT, arenden, LISTOR[0])


def historik(arenden: list) -> str:
    return lista(SAJT, arenden, LISTOR[2])


class Startsidan(unittest.TestCase):
    def test_raknar_listorna_och_visar_inga_kort(self):
        alla = [arende("pågår", "p"), arende("beslutat", "b"), arende("klart", "k")]
        html = startsida(SAJT, alla, RUNDA)
        self.assertIn('<li><a href="pagar.html">Pågår</a>: 1 ärende</li>', html)
        self.assertIn('<li><a href="historik.html">Historik</a>: 1 ärende</li>', html)
        self.assertNotIn("<article id=", html)
        self.assertNotIn("tidslinje", html)
        self.assertIn('<a href="beslutat.html">Beslutat</a></li>', html)

    def test_varje_lista_har_sina_statusar(self):
        alla = [arende("pågår", "p"), arende("beslutat", "b"), arende("klart", "k")]
        html = lista(SAJT, alla, LISTOR[1])
        self.assertIn("<h1>Beslutat</h1>", html)
        self.assertIn('id="b"', html)
        self.assertNotIn('id="p"', html)

    def test_tabellens_ar_ikoner_och_lank_till_kortet(self):
        html = pagar([arende("pågår", "p")])
        for ar in ("2025", "2026"):
            self.assertIn(f'<th scope="col">{ar}</th>', html)
        self.assertIn('<a href="arende/p.html">Ny förskola</a>', html)
        self.assertIn('class="steg beslut" href="https://example.org/b#sida-2"', html)
        self.assertIn('class="band start"', html)

    def test_kortet_lankar_till_arendets_sida(self):
        html = pagar([arende("pågår", "p")])
        self.assertIn('<a href="arende/p.html">Läs mer: alla 2 händelser med källor</a>', html)
        self.assertNotIn("Norra Halland", html)

    def test_nytt_ar_handelserna_i_rundans_period(self):
        html = startsida(SAJT, [arende("klart", "k")], RUNDA)
        nytt = html[html.index('id="nytt"') :]
        self.assertIn("1 ny händelse", nytt)
        self.assertIn('<a href="arende/k.html">Hela ärendet</a>', nytt)
        self.assertNotIn("Ett förslag.", nytt)
        self.assertIn("1 mars 2026</time> till <time datetime=\"2026-03-31\">31 mars 2026</time>. Startärenden.", nytt)

    def test_urval_per_ort_ur_omrade(self):
        html = pagar([arende("pågår", "p")])
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
        self.assertIn('<a class="arende" href="arende/s.html">Ny förskola</a>', nu)
        self.assertNotIn("2026-11-09", html)
        self.assertIn("1 december 2026</time>, om 21 dagar", nu)
        self.assertIn("Så kan du påverka, steg för steg", nu)

    def test_markering_pa_kort_och_rad(self):
        html = pagar([paverkbart("s")])
        self.assertIn('<small class="paverka">Tycka till <time datetime="2026-11-10">10 november 2026</time></small>', html)
        kortet = html[html.index('<article id="s"') :]
        self.assertIn('<div class="paverka"><p>Tycka till</p>', kortet)
        self.assertIn("Granskning – synpunkter senast <time datetime=\"2026-12-01\">tisdag 1 december 2026", kortet)
        self.assertIn("Beslut väntas, preliminärt <time datetime=\"2026-11-24\">tisdag 24 november 2026", kortet)

    def test_vantat_beslut_markeras_preliminart_i_tabellen(self):
        rader = "## Tycka till\n\n- 2026-11-24 · vantas · X. · [K](https://example.org/c)\n\n"
        text = ARENDE.replace("## I media", rader + "## I media")
        html = pagar([tolka("bevakning/ks/v.md", text)])
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
        self.assertIn("<h1>Pågår</h1>\n<p>Ärenden som inte är avgjorda.</p>", pagar([]))
        self.assertIn("<p>Inga ärenden ännu.</p>", pagar([]))
        self.assertIn('Sidan byggdes <time datetime="2026-11-10">10 november 2026</time>', html)


class Lasbarhet(unittest.TestCase):
    def test_forsta_lanken_hoppar_till_innehallet(self):
        for html in (startsida(SAJT, [], RUNDA), historik([])):
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
        spalt = float(re.search(r"ol\.handelser \{ max-width: ([0-9.]+)rem", stil).group(1))
        self.assertLessEqual(spalt * bas / 8.4, 70)


class Klarsprak(unittest.TestCase):
    def test_ikoner_kort_och_teckenforklaring_i_klartext(self):
        html = pagar([arende("pågår", "p")])
        self.assertIn("<strong>Samråd</strong> – samråd eller remiss: öppet för synpunkter.", html)
        self.assertIn("Senaste steget: beslut, <time", html)
        self.assertIn("<span>Pågått 2025–2026</span>", html)
        self.assertIn('aria-label="Beslut 2 mars 2026: Nämnden beslutade.', html)
        self.assertLess(html.index("Vad ikonerna betyder"), html.index("tidslinje"))


    def test_teckenforklaringen_ar_densamma_som_formatets(self):
        readme = (Path(__file__).resolve().parent.parent / "bevakning/README.md").read_text()
        efter = readme.split("Stegen ger ikonen")[1]
        tabellen = next(b for b in efter.split("\n\n") if b.startswith("|"))
        rader = re.findall(r"^\| `(\w+)` +\| (.+?) +\|$", tabellen, re.M)
        self.assertEqual(dict(rader), BETYDER)


class SaGorDu(unittest.TestCase):
    def test_varje_tillfalle_sager_vad_man_gor(self):
        html = startsida(SAJT, [paverkbart("s")], RUNDA)
        nu = html[html.index('id="tycka-till"') : html.index('id="nytt"')]
        rader = nu.split("<li data-ort=")[1:]
        self.assertEqual(len(rader), 3)
        for rad in rader:
            self.assertRegex(rad, r'^"[^"]+"><a class="arende" [^>]+>Ny förskola</a> <small>Åsa')
        self.assertIn("Så gör du:</strong> Före sammanträdet går ledamöterna", rader[0])
        self.assertIn("står i arbetsutskottets protokoll", rader[1])
        self.assertIn("Lämna skriftliga synpunkter senast sista dagen", rader[2])
        self.assertIn("<details open><summary>Så kan du påverka", nu)
        self.assertEqual(pagar([paverkbart("s")]).count("Så gör du:"), 3)

    def test_ett_steg_en_rad(self):
        self.assertEqual(len(set(SA_GOR.values())), len(SA_GOR) - 1)
        self.assertEqual(SA_GOR["yttrande"], SA_GOR["beslut"])


class Arendesidan(unittest.TestCase):
    def test_allt_om_arendet_med_fast_adress(self):
        html = arendesida(SAJT, paverkbart("s"))
        self.assertIn("<title>Ny förskola – Giffå</title>", html)
        self.assertIn('href="../stil.css"', html)
        self.assertIn('<a href="../index.html">Start</a>', html)
        self.assertIn("status: pågår", html)
        self.assertIn("Så gör du:", html)
        self.assertIn("Ett förslag. <a", html)
        self.assertIn('<a href="https://example.org/m">Rubrik</a> – Norra Halland', html)
        self.assertIn('href="https://github.com/agare/giffa/blob/main/bevakning/ks/s.md"', html)


def stillat(senast: str) -> str:
    return ARENDE.replace("2026-03-02", senast).replace("2025-01-05 ·", "2024-01-05 ·")


class StillaArenden(unittest.TestCase):
    def test_pagar_skiljer_rorliga_fran_stilla(self):
        gammalt = tolka("bevakning/ks/g.md", stillat("2024-11-09"))
        pa_gransen = tolka("bevakning/ks/n.md", stillat("2024-11-10"))
        html = pagar([arende("pågår", "p"), gammalt, pa_gransen])
        stilla = html.index('<h2 id="stilla">Ingen händelse sedan <time datetime="2024-11-10">')
        self.assertLess(html.index('id="p"'), stilla)
        self.assertLess(stilla, html.index('id="g"'))
        self.assertLess(html.index('id="n"'), stilla)
        self.assertEqual(html.count("Vad ikonerna betyder"), 1)


class Mobilen(unittest.TestCase):
    def test_tidslinjen_doljs_pa_smal_skarm(self):
        self.assertIn('<table class="tidslinje">', pagar([arende("pågår", "p")]))
        stil = (Path(__file__).resolve().parent.parent / "docs/stil.css").read_text(encoding="utf-8")
        smal = stil.split("@media (max-width: 40rem) {")[1].split("\n}")[0]
        self.assertIn("table.tidslinje { display: none; }", smal)
        self.assertNotIn("teckenforklaring", smal)


class Historiken(unittest.TestCase):
    def test_bara_klart_och_avbrutet(self):
        html = historik([arende("klart", "k"), arende("avbrutet", "x"), arende("pågår", "p")])
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
