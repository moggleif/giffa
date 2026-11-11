"""Krav: K18 och K23 i KRAV.md. Test: tests/test_sidor.py.

Ett ärendes egen sida med en adress som inte ändras när status ändras:
allt om ärendet, med alla händelser och källor utfällda.
"""

from html import escape

from webbplats.arende import Arende
from webbplats.fastighet import med_kartlankar
from webbplats.kort import markor, media, organ, post
from webbplats.mall import Sajt, sida
from webbplats.paverka import markering


def arendesida(sajt: Sajt, arende: Arende) -> str:
    innehall = (
        f'{markor(arende)}<p class="organ">{escape(organ(arende))} · status: {arende.falt["status"]}</p>'
        + (f"<p>{med_kartlankar(arende.ingress)}</p>" if arende.ingress else "")
        + markering(arende, sajt.byggd.date())
        + f"<h2>Händelser</h2><ol class=\"handelser\">{''.join(post(h) for h in arende.handelser)}</ol>"
        + media(arende)
        + f'<p><a href="{escape(sajt.repo)}/blob/main/{escape(arende.fil)}">Ärendet i repot</a></p>'
    )
    return sida(sajt, arende.sida, arende.falt["rubrik"], innehall)
