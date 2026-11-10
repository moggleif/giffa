"""Krav: K4 och K16 i KRAV.md. Test: tests/test_sidor.py.

Ett stegs ikon. Stegen skiljs åt med form, inte bara färg, och varje ikon i
tabellen länkar till händelsens källa.
"""

from html import escape

from webbplats.arende import STEG, Handelse
from webbplats.datum import klartext

LINJE = 'fill="none" stroke="currentColor" stroke-width="2"'
FORM = {
    "forslag": f'<circle cx="8" cy="8" r="5" {LINJE}/>',
    "samrad": '<path d="M2 3h12v8H7l-3 3v-3H2z" fill="currentColor"/>',
    "granskning": f'<circle cx="7" cy="7" r="4" {LINJE}/><path d="M10 10l4 4" {LINJE}/>',
    "yttrande": f'<path d="M4 2h6l3 3v9H4z" {LINJE}/>',
    "beslut": '<path d="M8 1l7 7-7 7-7-7z" fill="currentColor"/>',
    "bygge": '<path d="M8 2l7 12H1z" fill="currentColor"/>',
    "klart": f'<path d="M2 8l4 4 8-9" {LINJE} stroke-width="3"/>',
    "avbrutet": f'<path d="M3 3l10 10M13 3L3 13" {LINJE} stroke-width="3"/>',
    "info": '<circle cx="8" cy="8" r="3" fill="currentColor"/>',
}

BETYDER = {
    "forslag": "förslag, uppdrag eller initiativ",
    "samrad": "samråd eller remiss: öppet för synpunkter",
    "granskning": "granskning av ett planförslag",
    "yttrande": "en nämnd eller myndighet yttrar sig",
    "beslut": "beslut eller antagande",
    "bygge": "byggstart eller genomförande",
    "klart": "klart, på plats",
    "avbrutet": "avbrutet eller upphävt",
    "info": "information, avstämning eller överprövning av en högre instans",
}


def bild(steg: str) -> str:
    return (
        '<svg viewBox="0 0 16 16" width="1.3em" height="1.3em" aria-hidden="true">'
        f"{FORM[steg]}</svg>"
    )


def ikon(handelse: Handelse) -> str:
    namn = STEG[handelse.steg].capitalize()
    text = f"{namn} {klartext(handelse.datum)}: {handelse.text} – {handelse.kalla}"
    return (
        f'<a class="steg {handelse.steg}" href="{escape(handelse.lank)}" '
        f'title="{escape(text)}" aria-label="{escape(text)}">{bild(handelse.steg)}</a>'
    )


def teckenforklaring() -> str:
    poster = "".join(
        f'<li><span class="steg {steg}">{bild(steg)}</span> '
        f"<span><strong>{namn.capitalize()}</strong> – {BETYDER[steg]}.</span></li>"
        for steg, namn in STEG.items()
    )
    return (
        '<details class="teckenforklaring" open><summary>Vad ikonerna betyder</summary>'
        f"<ul>{poster}</ul></details>"
    )
