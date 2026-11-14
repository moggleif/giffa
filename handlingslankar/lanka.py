"""Krav: K26 i KRAV.md. Test: tests/test_handlingslankar.py.

Lägger handlingarna intill protokollet på de händelser i bevakningen som
bara länkar ett protokoll. Bara när händelsens datum är sammanträdets, så
att ett protokoll som återger ett äldre beslut inte ger fel handling.
"""

import re
from pathlib import Path

from handlingslankar import matcha
from handlingslankar.sidor import Paragraf, paragraf, som_ordbok

HANDELSE = re.compile(r"^- (\d{4}-\d\d-\d\d) · ")
PROTOKOLL = r"/([^/]+/\d{4}/(\d{4}-\d\d-\d\d))/(protokoll[^)#]*)\.html#sida-(\d+)"
KVALITET = re.compile(r"^kvalitet: (\S+)", re.M)
KALLA = re.compile(r"^kalla_url: (\S+)", re.M)


class Pool:
    def __init__(self, data: Path, bas: str):
        self.data, self.lasta = data, {}
        self.bas = f"{bas}/{data.name}"
        self.protokoll = re.compile(re.escape(self.bas) + PROTOKOLL)

    def text(self, del_: str) -> str | None:
        if del_ not in self.lasta:
            fil = self.data / f"{del_}.md"
            self.lasta[del_] = fil.read_text(encoding="utf-8") if fil.exists() else None
        return self.lasta[del_]


def protokollet(pool: Pool, rad: str) -> re.Match | None:
    handelse, traff = HANDELSE.match(rad), pool.protokoll.search(rad)
    if handelse and traff and " · Handlingar: " not in rad and traff[2] == handelse[1]:
        return traff
    return None


def lank(pool: Pool, rad: str) -> str | None:
    traff = protokollet(pool, rad)
    if not traff:
        return None
    mote, protokoll = traff[1], pool.text(f"{traff[1]}/{traff[3]}")
    handlingar = pool.text(f"{mote}/handlingar")
    funnen = protokoll and handlingar and paragraf(som_ordbok(protokoll), int(traff[4]))
    if not funnen:
        return None
    return sida(pool, mote, funnen) or pdf(pool, mote, funnen)


def sida(pool: Pool, mote: str, funnen: Paragraf) -> str | None:
    traff = matcha.handling(som_ordbok(pool.text(f"{mote}/handlingar")), funnen)
    return traff and f"[{traff[1]}]({pool.bas}/{mote}/handlingar.html#sida-{traff[0]})"


def pdf(pool: Pool, mote: str, funnen: Paragraf) -> str | None:
    handlingar, kallelse = pool.text(f"{mote}/handlingar"), pool.text(f"{mote}/kallelse")
    kvalitet = KVALITET.search(handlingar)
    if not kallelse or kvalitet[1] != "ej-hamtad" or matcha.allman(funnen):
        return None
    nummer = matcha.punkt(kallelse, funnen)
    kalla = KALLA.search(handlingar)
    # Sidan i PDF:en är okänd när handlingarna inte gick att hämta; punkten
    # i kallelsen visar var ärendet står.
    return nummer and kalla and f"[Handlingar till sammanträdet, punkt {nummer} (PDF)]({kalla[1]})"


def lanka_fil(pool: Pool, text: str) -> tuple[str, int]:
    rader, antal = text.split("\n"), 0
    for i, rad in enumerate(rader):
        ny = lank(pool, rad)
        if ny:
            rader[i], antal = f"{rad} · Handlingar: {ny}", antal + 1
    return "\n".join(rader), antal
