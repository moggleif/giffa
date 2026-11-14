"""K32: det som organen har informerats om, utan förslag eller tillfälle efter."""

import unittest

from tests.test_arende import ARENDE
from tests.test_sidor import RUNDA, SAJT
from webbplats.arende import tolka
from webbplats.sidor import startsida

INFO = "- {} · info · Arbetsutskottet informerades. · [Protokoll § 9](https://example.org/i)\n"


def informerat(namn: str, datum: str, status: str = "pågår", extra: str = "") -> object:
    text = ARENDE.replace("## Händelser\n\n", "## Händelser\n\n" + INFO.format(datum))
    text = text.replace("status: pågår", f"status: {status}")
    return tolka(f"bevakning/ksau/{namn}.md", text.replace("## I media", extra + "## I media"))


def pa_vag(arenden: list) -> str:
    html = startsida(SAJT, arenden, RUNDA)
    return html[html.index('id="pa-vag-upp"') : html.index('id="nytt"')]


class PaVagUpp(unittest.TestCase):
    def test_informerat_senaste_aret_nyast_forst(self):
        html = pa_vag([informerat("aldre", "2026-01-10"), informerat("nyare", "2026-10-01")])
        self.assertLess(html.index("arende/nyare.html"), html.index("arende/aldre.html"))
        self.assertIn('<small>Information <time datetime="2026-10-01">1 oktober 2026</time> · <a href="https://example.org/i" title="Arbetsutskottet informerades.">Protokoll § 9</a>', html)
        self.assertIn('<li data-ort="Åsa|Fjärås"><span class="tecken partiet">', html)

    def test_inte_aldre_an_ett_ar_avgjort_eller_med_tillfalle(self):
        tillfalle = "## Tycka till\n\n- 2026-12-01 · beslut · X. · [K](https://example.org/k)\n\n"
        html = pa_vag(
            [
                informerat("gammal", "2025-11-09"),
                informerat("beslutad", "2026-10-01", "beslutat"),
                informerat("kallad", "2026-10-01", extra=tillfalle),
            ]
        )
        self.assertIn("Inget just nu.", html)

    def test_ett_forslag_efter_informationen_tar_bort_arendet(self):
        self.assertIn("Inget just nu.", pa_vag([tolka("bevakning/ks/f.md", ARENDE)]))


if __name__ == "__main__":
    unittest.main()
