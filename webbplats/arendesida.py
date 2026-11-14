"""Krav: K18, K23, K24, K25, K27 och K33 i KRAV.md. Test: tests/test_sidor.py och tests/test_handlingar.py.

Ett ärendes egen sida med en adress som inte ändras när status ändras:
allt om ärendet, med alla händelser och källor utfällda.
"""

from html import escape

from webbplats.arende import Arende
from webbplats.handlingar import forslaget
from webbplats.kort import markor, media, namn_rad, organ, post
from webbplats.mall import Sajt, sida
from webbplats.paverka import markering
from webbplats.stege import stege


def arendesida(sajt: Sajt, arende: Arende) -> str:
    innehall = (
        f'{markor(arende)}{namn_rad(arende)}<p class="organ">{escape(organ(arende))} · status: {arende.falt["status"]}</p>'
        + (f"<p>{sajt.karta.lanka(arende.ingress)}</p>" if arende.ingress else "")
        + stege(arende, sajt.byggd.date())
        + markering(arende, sajt)
        + forslaget(arende, sajt.karta)
        + f"<h2>Händelser</h2><ol class=\"handelser\">{''.join(post(h, sajt.karta) for h in arende.handelser)}</ol>"
        + media(arende)
        + f'<p><a href="{escape(sajt.repo)}/blob/main/{escape(arende.fil)}">Ärendet i repot</a></p>'
    )
    return sida(sajt, arende.sida, arende.falt["rubrik"], innehall)
