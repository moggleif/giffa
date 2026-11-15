"""K34: sidan om kommunstyrelsens kommande sammanträde, punkt för punkt."""

import unittest
from datetime import date
from pathlib import Path

from tests.test_arende import ARENDE
from tests.test_sidor import SAJT
from webbplats.arende import tolka
from webbplats.kallelsen import kommande
from webbplats.ksmotet import ks_motet
from webbplats.punktkoppling import foljda, traffar

POOL = Path(__file__).resolve().parent / "fixtures" / "pool"
PLATSER = [{"namn": "Åsaskolan", "ort": "Åsa"}]


def arende(namn: str, diarienummer: str) -> object:
    text = ARENDE.replace("organ: Nämnden", f"organ: KS\ndiarienummer: {diarienummer}")
    return tolka(f"bevakning/ks/{namn}.md", text.replace("Ny förskola", namn.capitalize()))


class KommandeMotet(unittest.TestCase):
    def test_forsta_datumet_fran_byggdagen_med_kallelsens_punkter(self):
        motet = kommande(POOL, date(2026, 10, 21))
        self.assertEqual(motet.datum, date(2026, 11, 24))
        self.assertEqual(motet.katalog, "ks/2026/2026-11-24")
        self.assertEqual([p.punkt.nummer for p in motet.punkter], [1, 2, 3, 4, 5])
        forsta = motet.punkter[0]
        self.assertEqual(forsta.punkt.rubrik, "Utbyggnad av Åsaskolan")
        self.assertEqual(forsta.numren, ("KS-2026-1", "BN-2025-7"))
        self.assertEqual(forsta.handling, range(2, 4))
        self.assertEqual(forsta.sammanfattning, ("Skolan ska byggas ut för fler elever.",))

    def test_motesdagen_raknas_som_kommande(self):
        self.assertEqual(kommande(POOL, date(2026, 10, 20)).datum, date(2026, 10, 20))

    def test_utan_kallelse_inga_punkter_och_utan_mote_inget(self):
        motet = kommande(POOL, date(2026, 12, 2))
        self.assertEqual(motet.datum, date(2026, 12, 15))
        self.assertIsNone(motet.punkter)
        self.assertIsNone(kommande(POOL, date(2026, 12, 16)))

    def test_orten_i_kallelsen_och_den_som_bara_star_i_handlingen(self):
        forsta = kommande(POOL, date(2026, 11, 1)).punkter[0]
        funna = {(t.namn, t.i_handlingen) for t in traffar(forsta, SAJT.orter, PLATSER)}
        self.assertEqual(funna, {("Åsaskolan", False), ("Fjärås", True)})

    def test_arendena_med_punktens_nummer_utan_forled_och_ur_handlingen(self):
        forsta = kommande(POOL, date(2026, 11, 1)).punkter[0]
        arenden = [
            arende("ks", "KS-2026-1"),
            arende("utan", "2026-1"),
            arende("bn", "BN-2026-1"),
            arende("bygglov", "BN 2025-7"),
            arende("annat", "2025-7"),
        ]
        egna, osakra, namnda = foljda(forsta, arenden)
        self.assertEqual([a.id for a in egna], ["ks"])
        self.assertEqual([a.id for a in osakra], ["utan"])
        self.assertEqual([a.id for a in namnda], ["bygglov"])


class Sidan(unittest.TestCase):
    def html(self, dag: date) -> str:
        arenden = [arende("skolan", "KS-2026-1"), arende("bygglovet", "BN 2025-7")]
        return ks_motet(SAJT, kommande(POOL, dag), arenden, PLATSER)

    def test_alla_punkter_i_kallelsens_ordning_med_det_som_saknas_sagt(self):
        html = self.html(date(2026, 11, 1))
        self.assertIn("<h1>Kommunstyrelsen 24 november 2026</h1>", html)
        self.assertIn("<h2>Dagordningen, 5 punkter</h2>", html)
        punkter = [html.index(f'<article id="punkt-{n}">') for n in (1, 2, 3, 4, 5)]
        self.assertEqual(punkter, sorted(punkter))
        self.assertIn("<blockquote>Kommunstyrelsen godkänner utbyggnaden.</blockquote>", html)
        self.assertIn("Inget förslag till beslut i kallelsen.", html)
        self.assertIn("Förslaget gick inte att läsa ur kallelsen.", html)
        self.assertIn("Rubriken gick inte att läsa ur kallelsen", html)
        self.assertIn("Ingen sammanfattning av ärendet i handlingen.", html)
        self.assertIn("Ingen egen handling hittad för punkten", html)
        self.assertIn("Dnr saknas i kallelsen", html)
        self.assertIn("Dnr KS-2026-00015", html)

    def test_handlingen_och_historiken_lankar_till_datapoolen(self):
        html = self.html(date(2026, 11, 1))
        bas = "https://moggleif.github.io/kommunhandlingar/kungsbacka/ks/2026/2026-11-24"
        self.assertIn(f'<a href="{bas}/handlingar.html#sida-2">Handlingen, sidorna 2–3</a>', html)
        self.assertIn(f'<a href="{bas}.html#punkt-1">Historik i alla organ</a>', html)

    def test_foreningarna_i_oversikten_och_orterna_pa_punkten(self):
        html = self.html(date(2026, 11, 1))
        rad = html.split('<a href="#punkt-1">1</a>')[1].split("</tr>")[0]
        self.assertIn('<td data-forening="Åsa" title="Åsa, Fjärås">●', rad)
        self.assertTrue(rad.endswith("<td></td>"))
        kortet = html.split('<article id="punkt-1">')[1].split("</article>")[0]
        self.assertIn("<span>Åsaskolan (Åsa)</span>", kortet)
        self.assertIn("I handlingen: Fjärås", kortet)

    def test_arendet_med_punktens_nummer_och_det_som_handlingen_namner(self):
        kortet = self.html(date(2026, 11, 1)).split('<article id="punkt-1">')[1]
        kortet = kortet.split("</article>")[0]
        self.assertIn('Följs i Giffå: <a href="arende/skolan.html">Skolan</a>', kortet)
        self.assertIn("Historik i Giffå, 2 händelser", kortet)
        self.assertIn('nämner ett nummer i <a href="arende/bygglovet.html">', kortet)

    def test_utan_handlingar_ingen_lank_och_olaslig_dagordning_sagd(self):
        html = self.html(date(2026, 11, 25))
        self.assertIn("Dagordningen gick inte att läsa ur kallelsen.", html)
        self.assertNotIn("Handlingarna</a>", html)
        self.assertIn("Handlingarna</a>", self.html(date(2026, 11, 1)))

    def test_utan_kallelse_och_utan_mote(self):
        self.assertIn("Kallelsen finns inte i datapoolen än.", self.html(date(2026, 12, 2)))
        self.assertIn("Inget kommande sammanträde", self.html(date(2026, 12, 16)))


if __name__ == "__main__":
    unittest.main()
