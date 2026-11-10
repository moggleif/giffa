"""K15: datum i klartext och dagar kvar."""

import unittest
from datetime import date

from webbplats.datum import kvar, med_veckodag, tid


class Datum(unittest.TestCase):
    def test_som_man_sager_det_med_iso_i_datetime(self):
        self.assertEqual(tid(date(2026, 3, 1)), '<time datetime="2026-03-01">1 mars 2026</time>')

    def test_med_veckodag(self):
        self.assertIn(">tisdag 24 november 2026<", med_veckodag(date(2026, 11, 24)))

    def test_dagar_kvar(self):
        idag = date(2026, 11, 10)
        self.assertEqual(kvar(date(2026, 11, 10), idag), "i dag")
        self.assertEqual(kvar(date(2026, 11, 11), idag), "i morgon")
        self.assertEqual(kvar(date(2026, 11, 24), idag), "om 14 dagar")
