"""Krav: K18, K23, K24, K25 och K27 i KRAV.md. Test: tests/test_sidor.py och tests/test_handlingar.py.

Ett ärendes egen sida med en adress som inte ändras när status ändras:
allt om ärendet, med alla händelser och källor utfällda.
"""

from html import escape

from webbplats.arende import Arende
from webbplats.handlingar import forslaget
from webbplats.kort import kallas, markor, media, organ, post
from webbplats.mall import Sajt, sida
from webbplats.paverka import markering


def arendesida(sajt: Sajt, arende: Arende) -> str:
    innehall = (
        f'{markor(arende)}{kallas(arende)}<p class="organ">{escape(organ(arende))} · status: {arende.falt["status"]}</p>'
        + (f"<p>{sajt.karta.lanka(arende.ingress)}</p>" if arende.ingress else "")
        + forslaget(arende, sajt.karta)
        + markering(arende, sajt)
        + f"<h2>Händelser</h2><ol class=\"handelser\">{''.join(post(h, sajt.karta) for h in arende.handelser)}</ol>"
        + media(arende)
        + f'<p><a href="{escape(sajt.repo)}/blob/main/{escape(arende.fil)}">Ärendet i repot</a></p>'
    )
    return sida(sajt, arende.sida, arende.falt["rubrik"], innehall)
