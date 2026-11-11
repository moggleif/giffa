"""Krav: K23 och K24 i KRAV.md. Test: tests/test_karta.py.

Länken till en sökning i Kungsbackas karta (KALLOR.md). Kartan hämtas
aldrig; bara adressen byggs, i formatet som kartans egen sökning ger.
Länken öppnas i en ny flik, så att läsaren har kvar ärendet.
"""

from html import escape
from urllib.parse import quote_plus

KARTA = "https://karta.kungsbacka.se/publik/#m=publik&q={}"


def lank(sok: str, text: str) -> str:
    adress = escape(KARTA.format(quote_plus(sok)))
    return f'<a href="{adress}" target="_blank" rel="noopener">{text}</a>'
