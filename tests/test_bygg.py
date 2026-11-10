"""K3 och K10: bygget av hela repot ger sidorna, och ett felaktigt ärende stoppar."""

import shutil
import tempfile
import unittest
from pathlib import Path

from webbplats.__main__ import bygg

ROT = Path(__file__).resolve().parent.parent


class Bygg(unittest.TestCase):
    def setUp(self):
        self.ut = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.ut)

    def test_repots_arenden_ger_sidorna_och_det_statiska(self):
        bygg(ROT, self.ut, "https://github.com/agare/giffa")
        for namn in (
            "index.html",
            "historik.html",
            "bevakar.html",
            "stil.css",
            "urval.js",
            ".nojekyll",
        ):
            self.assertTrue((self.ut / namn).exists(), namn)
        arenden = list(ROT.glob("bevakning/*/*.md"))
        self.assertEqual(len(list(self.ut.glob("arende/*.html"))), len(arenden))

    def test_felaktigt_arende_stoppar_med_filens_namn(self):
        rot = self.ut / "repo"
        shutil.copytree(ROT, rot, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        fil = next(rot.glob("bevakning/*/*.md"))
        fil.write_text(
            fil.read_text(encoding="utf-8").replace("status: ", "status: x"), encoding="utf-8"
        )
        with self.assertRaises(SystemExit) as fel:
            bygg(rot, self.ut / "sajt", "https://github.com/agare/giffa")
        self.assertIn(fil.name, str(fel.exception))

    def test_samma_filnamn_i_tva_kataloger_stoppar(self):
        rot = self.ut / "repo"
        shutil.copytree(ROT, rot, ignore=shutil.ignore_patterns(".git", "__pycache__"))
        fil = next(rot.glob("bevakning/ks/*.md"))
        shutil.copy(fil, rot / "bevakning/namnder" / fil.name)
        with self.assertRaises(SystemExit) as fel:
            bygg(rot, self.ut / "sajt", "https://github.com/agare/giffa")
        self.assertIn(fil.name.removesuffix(".md"), str(fel.exception))


if __name__ == "__main__":
    unittest.main()
