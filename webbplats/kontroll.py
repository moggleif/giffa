"""Krav: K10 och K12 i KRAV.md. Test: tests/test_arende.py.

Det i ett ärende som bara går att pröva mot repots andra filer: orterna i
OMRADE.md, statusen, händelsernas ordning och stegen för att tycka till.
"""

from webbplats.arende import STATUS, Arende
from webbplats.paverka import TILLFALLE


def kontrollera(arende: Arende, orter: list[str]) -> None:
    if arende.falt["status"] not in STATUS:
        raise ValueError(f"okänd status {arende.falt['status']!r}")
    if okanda := [o for o in arende.orter if o not in orter]:
        raise ValueError(f"orten finns inte i OMRADE.md: {', '.join(okanda)}")
    if not arende.handelser:
        raise ValueError("ärendet har inga händelser")
    datumen = [h.datum for h in arende.handelser]
    if datumen != sorted(datumen, reverse=True):
        raise ValueError("händelserna står inte nyast först")
    if fel := [t.steg for t in arende.tillfallen if t.steg not in TILLFALLE]:
        raise ValueError(f"steget går inte att tycka till om: {fel[0]}")
