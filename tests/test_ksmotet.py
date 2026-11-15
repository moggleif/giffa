"""K34: sidan om kommunstyrelsens kommande sammanträde, punkt för punkt."""

import unittest
from dataclasses import replace
from datetime import date
from pathlib import Path

from tests.test_arende import ARENDE
from tests.test_sidor import SAJT
from webbplats.arende import tolka
from webbplats.kallelsen import kommande
from webbplats.ksmotet import ks_motet
from webbplats.punktkoppling import foljda, traffar
from webbplats.sokord import sokord

POOL = Path(__file__).resolve().parent / "fixtures" / "pool"
TOM = Path(__file__).resolve().parent / "fixtures" / "tom_pool"
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

    def test_foregaende_i_vantan_pa_nasta_kallelse(self):
        motet = kommande(POOL, date(2026, 12, 2))
        self.assertEqual((motet.datum, motet.foregaende), (date(2026, 12, 1), True))
        self.assertEqual(motet.nasta, date(2026, 12, 15))
        self.assertIsNone(kommande(POOL, date(2026, 12, 16)).nasta)
        self.assertFalse(kommande(POOL, date(2026, 11, 1)).foregaende)

    def test_utan_tidigare_kallelse_nasta_utan_punkter_och_utan_mote_inget(self):
        motet = kommande(POOL, date(2026, 10, 1))
        self.assertEqual(motet.datum, date(2026, 10, 20))
        self.assertIsNone(motet.punkter)
        self.assertIsNone(kommande(TOM, date(2026, 10, 1)))

    def test_orten_i_kallelsen_och_den_som_bara_star_i_handlingen(self):
        forsta = kommande(POOL, date(2026, 11, 1)).punkter[0]
        funna = {(t.ort, t.i_handlingen) for t in traffar(forsta, SAJT.orter, PLATSER)}
        self.assertEqual(funna, {("Åsa", False), ("Fjärås", True)})

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


class Sokorden(unittest.TestCase):
    def test_ord_ur_rubriken_och_platser_i_kallelsen_hogst_fyra(self):
        punkter = kommande(POOL, date(2026, 11, 1)).punkter
        self.assertEqual(sokord(punkter[2], PLATSER), ["Planbesked"])
        platser = [{"namn": n, "ort": "Åsa"} for n in ("Ekan", "Boken", "Lönnen")]
        punkt = replace(punkter[0].punkt, rubrik="Taxa, remiss och planbesked")
        forsta = replace(punkter[0], punkt=punkt, kallelsen="Ekan, Boken och Lönnen")
        self.assertEqual(sokord(forsta, platser), ["Planbesked", "Remiss", "Ekan", "Boken"])


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

    def test_orterna_pa_punkten_utan_oversikt_per_forening(self):
        html = self.html(date(2026, 11, 1))
        self.assertNotIn("<table", html)
        kortet = html.split('<article id="punkt-1">')[1].split("</article>")[0]
        self.assertIn(
            '<p class="markor"><span class="nummer">Punkt 1</span><span>Åsa</span>'
            '<span class="sokord">Åsaskolan</span>'
            '<small>i handlingen:</small><span class="svag">Fjärås</span></p>',
            kortet,
        )
        tredje = html.split('<article id="punkt-3">')[1]
        self.assertIn('<span>Fjärås</span><span class="sokord">Planbesked</span>', tredje)

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

    def test_foregaende_markt_overst(self):
        html = self.html(date(2026, 12, 2))
        self.assertIn("<h1>Kommunstyrelsen 1 december 2026</h1>", html)
        self.assertIn(
            '<div class="varning" role="note"><p><strong>Det här är föregående sammanträde, '
            "inte nästa.</strong></p>"
            "<p>Kallelsen till nästa, 15 december 2026, finns inte i datapoolen än.</p></div>",
            html,
        )
        utan_nasta = self.html(date(2026, 12, 16))
        self.assertIn("Nästa sammanträde finns inte i kalendern än.", utan_nasta)
        self.assertNotIn("föregående", self.html(date(2026, 11, 1)))

    def test_utan_kallelse_och_utan_mote(self):
        self.assertIn("Kallelsen finns inte i datapoolen än.", self.html(date(2026, 10, 1)))
        html = ks_motet(SAJT, kommande(TOM, date(2026, 10, 1)), [], PLATSER)
        self.assertIn("Inget kommande sammanträde", html)


if __name__ == "__main__":
    unittest.main()
