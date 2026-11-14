"""Krav: K30 i KRAV.md. Test: tests/test_spar.py.

De två spåren för att påverka: partierna, som kan ta upp ett ärende innan
det beslutas, och alla, som kan lämna synpunkter i samråd och granskning.
Varje spår har ett eget tecken och en egen färg, överallt på sidan.
"""

ALLA = ("samrad", "granskning")
NAMN = {"partiet": "Diskutera i partiet", "alla": "Tycka till för alla"}
FORM = {
    "alla": '<path d="M2 3h12v8H7l-3 3v-3H2z" fill="currentColor"/>',
    "partiet": (
        '<circle cx="5" cy="5" r="2.5" fill="currentColor"/>'
        '<circle cx="11" cy="5" r="2.5" fill="currentColor"/>'
        '<path d="M1 14c0-3 2-5 4-5s4 2 4 5zM7 14c0-3 2-5 4-5s4 2 4 5z" fill="currentColor"/>'
    ),
}


def spar(steg: str) -> str:
    return "alla" if steg in ALLA else "partiet"


def tecken(namn: str) -> str:
    return (
        f'<span class="tecken {namn}"><svg viewBox="0 0 16 16" width="1.3em" height="1.3em" '
        f'aria-hidden="true">{FORM[namn]}</svg><span class="dold">{NAMN[namn]}: </span></span>'
    )
