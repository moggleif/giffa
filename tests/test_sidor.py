"""K4–K9: tabellen, korten, startsidan, historiken och sidan om bevakningen."""

import unittest
from datetime import date, datetime, timezone

from tests.test_arende import ARENDE
from webbplats.arende import tolka
from webbplats.bevakar import bevakar
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
        self.assertIn("Läs mer: händelserna och källorna, 2 st", html)
        self.assertIn('<a href="https://example.org/m">Rubrik</a> – Norra Halland', html)
        self.assertIn('href="https://github.com/agare/giffa/blob/main/bevakning/ks/p.md"', html)

    def test_nytt_ar_handelserna_i_rundans_period(self):
        html = startsida(SAJT, [arende("klart", "k")], RUNDA)
        nytt = html[html.index('id="nytt"') :]
        self.assertIn("1 ny händelse", nytt)
        self.assertIn('href="historik.html#k"', nytt)
        self.assertNotIn("Ett förslag.", nytt)
        self.assertIn("2026-03-01 till 2026-03-31. Startärenden.", nytt)

    def test_urval_per_ort_ur_omrade(self):
        html = startsida(SAJT, [arende("pågår", "p")], RUNDA)
        self.assertIn('<button type="button" data-urval="Fjärås">Fjärås</button>', html)
        self.assertIn('<tr data-ort="Åsa|Fjärås">', html)
        self.assertIn('<article id="p" data-ort="Åsa|Fjärås">', html)

    def test_inget_nytt_sags(self):
        html = startsida(SAJT, [arende("pågår")], Runda(date(2027, 1, 1), date(2027, 1, 31), ""))
        self.assertIn("Inga nya händelser.", html)

    def test_synpunkter_visas(self):
        text = ARENDE.replace(
            "status: pågår",
            "status: pågår\nsynpunkter: https://x.se/s\nsynpunkter_senast: 2026-04-01",
        )
        html = startsida(SAJT, [tolka("bevakning/ks/s.md", text)], RUNDA)
        self.assertIn('Lämna synpunkter senast 2026-04-01: <a href="https://x.se/s">', html)

    def test_sidfoten_lankar_till_repot(self):
        html = startsida(SAJT, [], RUNDA)
        self.assertIn(
            '<footer><p>Källkod, ärenden och källor: <a href="https://github.com/agare/giffa">',
            html,
        )
        self.assertIn("<h2>Pågår</h2><p>Inga ärenden ännu.</p>", html)


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
