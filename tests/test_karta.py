"""K23 och K24: fastighetsbeteckningar, platser, gator och detaljplaner blir länkar till kartan."""

import unittest

from webbplats.kartlankar import Kartlankar, ur_platser

KARTA = Kartlankar(("Åsaskolan", "Åsa idrottsplats"))
med_kartlankar = KARTA.lanka

OLMANAS = (
    '<a href="https://karta.kungsbacka.se/publik/#m=publik&amp;q='
    '%C3%96lman%C3%A4s+1%3A17">Ölmanäs 1:17</a>'
)


class Kartlankar(unittest.TestCase):
    def test_adressen_ur_kartan(self):
        self.assertEqual(
            med_kartlankar("Planbesked för Ölmanäs 1:17 i Åsa."),
            f"Planbesked för {OLMANAS} i Åsa.",
        )

    def test_trakt_med_bindestreck(self):
        self.assertIn(">Frillesås-Rya 3:77</a>", med_kartlankar("inom Frillesås-Rya 3:77"))

    def test_flera_beteckningar(self):
        text = med_kartlankar("Varla 2:198 och Tölö 5:39")
        self.assertEqual(text.count("<a "), 2)

    def test_upprakning_och_intervall_far_trakten_fran_den_forsta(self):
        text = med_kartlankar("Åsa 5:153 och 5:89, Bäcken 1:31–1:34")
        self.assertEqual(text.count("<a "), 4)
        self.assertIn("q=%C3%85sa+5%3A89\">5:89</a>", text)
        self.assertIn("q=B%C3%A4cken+1%3A34\">1:34</a>", text)

    def test_trakt_med_tva_ord(self):
        text = med_kartlankar("planläggning för fastigheten Ölmevalla Hallen 1:17")
        self.assertIn("q=%C3%96lmevalla+Hallen+1%3A17\">Ölmevalla Hallen 1:17</a>", text)

    def test_ord_som_inleder_meningen_hor_inte_till_trakten(self):
        for text in ("På Särö 1:493 bedrivs golf.", "Ja. Fastigheten Rya 4:17 överläts."):
            lankat = med_kartlankar(text)
            self.assertNotIn(">På ", lankat)
            self.assertNotIn(">Fastigheten ", lankat)
            self.assertEqual(lankat.count("<a "), 1)

    def test_bolagsnamn_lankas_inte(self):
        for text in ("med Castellum Varla 3:34 AB.", "till Fjärås Äskatorp 4:19B AB."):
            self.assertEqual(med_kartlankar(text), text)

    def test_inte_klockslag_eller_ord_med_liten_bokstav(self):
        for text in ("kl. 10:30", "och 1:105", "Sida 3", "Åsa 5:246:1"):
            self.assertNotIn("<a", med_kartlankar(text), text)

    def test_resten_av_texten_escapas(self):
        self.assertEqual(med_kartlankar("A & <b>"), "A &amp; &lt;b&gt;")


def lank(sok: str, text: str) -> str:
    return f'<a href="https://karta.kungsbacka.se/publik/#m=publik&amp;q={sok}">{text}</a>'


class Platser(unittest.TestCase):
    def test_plats_ur_platser(self):
        self.assertEqual(
            med_kartlankar("Ny idrottshall vid Åsaskolan."),
            f"Ny idrottshall vid {lank('%C3%85saskolan', 'Åsaskolan')}.",
        )

    def test_langsta_namnet_vinner(self):
        self.assertIn(">Åsa idrottsplats</a>", med_kartlankar("på Åsa idrottsplats"))

    def test_inte_inuti_ett_annat_ord(self):
        self.assertNotIn("<a", med_kartlankar("Åsaskolans elever"))

    def test_foreningar_och_planer_lankas_inte(self):
        rader = [{"namn": "Åsa IF", "typ": "förening"}, {"namn": "Åsaskolan", "typ": "grundskola"}]
        self.assertEqual(ur_platser(rader).platser, ("Åsaskolan",))


class Gator(unittest.TestCase):
    def test_gatunamn_utan_husnummer(self):
        self.assertEqual(
            med_kartlankar("vid Pölagårdsvägen 11"),
            f"vid {lank('P%C3%B6lag%C3%A5rdsv%C3%A4gen', 'Pölagårdsvägen')} 11",
        )

    def test_leden_och_gatan(self):
        text = med_kartlankar("Säröleden och Kungsgatan")
        self.assertEqual(text.count("<a "), 2)


class Detaljplaner(unittest.TestCase):
    def test_plannummer_efter_detaljplan(self):
        self.assertEqual(
            med_kartlankar("i detaljplan S88 från 1981"),
            f"i detaljplan {lank('S88', 'S88')} från 1981",
        )

    def test_flera_plannummer(self):
        text = med_kartlankar("ersätter planerna T13 och T15")
        self.assertEqual(text.count("<a "), 2)

    def test_plannummer_utan_ordet_plan_lankas_inte(self):
        self.assertNotIn("<a", med_kartlankar("väg E6 och K35"))
