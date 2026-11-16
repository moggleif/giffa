"""Krav: K37 i KRAV.md. Test: tests/test_tidningar.py.

Läser ett RSS-flöde till artiklar: tidning, rubrik, länk, datum och
ingress. Ingressen rensas från HTML.
"""

import html
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import date
from email.utils import parsedate_to_datetime

TAGG = re.compile(r"<[^>]+>")


@dataclass(frozen=True)
class Artikel:
    tidning: str
    rubrik: str
    lank: str
    datum: date
    ingress: str

    @property
    def text(self) -> str:
        return f"{self.rubrik} {self.ingress}"


def artiklar(tidning: str, xml: str) -> list[Artikel]:
    return [artikel(tidning, post) for post in ET.fromstring(xml).iter("item")]


def artikel(tidning: str, post: ET.Element) -> Artikel:
    ingress = html.unescape(TAGG.sub(" ", falt(post, "description")))
    return Artikel(
        tidning,
        html.unescape(falt(post, "title")),
        falt(post, "link"),
        parsedate_to_datetime(falt(post, "pubDate")).date(),
        " ".join(ingress.split()),
    )


def falt(post: ET.Element, namn: str) -> str:
    return " ".join((post.findtext(namn) or "").split())
