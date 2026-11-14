"""Krav: K26 i KRAV.md. Test: tests/test_handlingslankar.py.

Lägger handlingarna intill protokollet på de händelser i bevakningen som
bara länkar ett protokoll. Bara när händelsens datum är sammanträdets, så
att ett protokoll som återger ett äldre beslut inte ger fel handling.
"""

import re
from pathlib import Path

from handlingslankar import matcha
from handlingslankar.sidor import paragraf, sidor

HANDELSE = re.compile(r"^- (\d{4}-\d\d-\d\d) · ")
PROTOKOLL = r"/([^/]+/\d{{4}}/(\d{{4}}-\d\d-\d\d))/(protokoll[^)#]*)\.html#sida-(\d+)"
KVALITET = re.compile(r"^kvalitet: (\S+)", re.M)
KALLA = re.compile(r"^kalla_url: (\S+)", re.M)


class Pool:
    def __init__(self, data: Path, bas: str):
        self.data, self.cache = data, {}
        self.bas = f"{bas}/{data.name}"
        self.protokoll = re.compile(re.escape(self.bas) + PROTOKOLL.format())

    def text(self, del_: str) -> str | None:
        if del_ not in self.cache:
            fil = self.data / f"{del_}.md"
            self.cache[del_] = fil.read_text(encoding="utf-8") if fil.exists() else None
        return self.cache[del_]


def lank(pool: Pool, rad: str) -> str | None:
    handelse, traff = HANDELSE.match(rad), pool.protokoll.search(rad)
    if not handelse or not traff or " · Handlingar: " in rad or traff[2] != handelse[1]:
        return None
    protokoll, handlingar = pool.text(f"{traff[1]}/{traff[3]}"), pool.text(f"{traff[1]}/handlingar")
    if not protokoll or not handlingar:
        return None
    funnen = paragraf(sidor(protokoll), int(traff[4]))
    return funnen and (sida(pool, traff[1], handlingar, funnen) or pdf(pool, traff[1], handlingar, funnen))


def sida(pool: Pool, mote: str, handlingar: str, funnen) -> str | None:
    traff = matcha.handling(sidor(handlingar), funnen)
    return traff and f"[{traff[1]}]({pool.bas}/{mote}/handlingar.html#sida-{traff[0]})"


def pdf(pool: Pool, mote: str, handlingar: str, funnen) -> str | None:
    kvalitet, kalla, kallelse = KVALITET.search(handlingar), KALLA.search(handlingar), pool.text(f"{mote}/kallelse")
    if not kvalitet or kvalitet[1] != "ej-hamtad" or not kalla or not kallelse:
        return None
    nummer = matcha.punkt(kallelse, funnen)
    return nummer and f"[Handlingar till sammanträdet, punkt {nummer} (PDF)]({kalla[1]})"


def lanka_fil(pool: Pool, text: str) -> tuple[str, int]:
    rader, antal = text.split("\n"), 0
    for i, rad in enumerate(rader):
        ny = lank(pool, rad)
        if ny:
            rader[i], antal = f"{rad} · Handlingar: {ny}", antal + 1
    return "\n".join(rader), antal
