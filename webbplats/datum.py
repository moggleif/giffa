"""Krav: K15 i KRAV.md. Test: tests/test_datum.py.

Datum som man säger dem, och hur länge det är kvar till ett tillfälle att
tycka till. Maskinläsbart ISO-datum följer med i `datetime`.
"""

from datetime import date

MANADER = (
    "januari", "februari", "mars", "april", "maj", "juni",
    "juli", "augusti", "september", "oktober", "november", "december",
)
VECKODAGAR = ("måndag", "tisdag", "onsdag", "torsdag", "fredag", "lördag", "söndag")


def klartext(dag: date) -> str:
    return f"{dag.day} {MANADER[dag.month - 1]} {dag.year}"


def tid(dag: date) -> str:
    return f'<time datetime="{dag}">{klartext(dag)}</time>'


def med_veckodag(dag: date) -> str:
    return f'<time datetime="{dag}">{VECKODAGAR[dag.weekday()]} {klartext(dag)}</time>'


def kvar(dag: date, idag: date) -> str:
    dagar = (dag - idag).days
    return {0: "i dag", 1: "i morgon"}.get(dagar, f"om {dagar} dagar")
