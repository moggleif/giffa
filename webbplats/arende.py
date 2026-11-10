"""Krav: K1, K4, K10 och K12 i KRAV.md. Test: tests/test_arende.py.

Läser ett ärende enligt formatet i bevakning/README.md och stoppar med
felet när något inte följer det.
"""

import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

STATUS = ("pågår", "beslutat", "klart", "avbrutet")
STEG = {
    "forslag": "förslag eller uppdrag",
    "samrad": "samråd",
    "granskning": "granskning",
    "yttrande": "yttrande",
    "beslut": "beslut",
    "bygge": "byggs",
    "klart": "klart",
    "avbrutet": "avbrutet",
    "info": "information",
}
TILLFALLEN = ("samrad", "granskning", "yttrande", "beslut", "vantas")
KRAVS = ("rubrik", "ort", "organ", "status")
VALFRIA = ("diarienummer",)
AVSNITT = ("Händelser", "Tycka till", "I media och debatt")
LANK = re.compile(r"\[([^\]]+)\]\((https://\S+)\)")


@dataclass(frozen=True)
class Handelse:
    datum: date
    steg: str
    text: str
    kalla: str
    lank: str


@dataclass(frozen=True)
class Mediepost:
    datum: date
    rubrik: str
    lank: str
    var: str


@dataclass(frozen=True)
class Arende:
    fil: str
    falt: dict[str, str]
    ingress: str
    handelser: list[Handelse]
    tillfallen: list[Handelse]
    media: list[Mediepost]

    @property
    def id(self) -> str:
        return self.fil.rsplit("/", 1)[-1].removesuffix(".md")

    @property
    def orter(self) -> list[str]:
        return [ort.strip() for ort in self.falt["ort"].split(",")]


def tolka(fil: str, text: str) -> Arende:
    if not text.startswith("---\n") or text.count("---\n") < 2:
        raise ValueError("front matter saknas")
    _, huvud, kropp = text.split("---\n", 2)
    ingress, avsnitt = dela(kropp)
    if okanda := set(avsnitt) - set(AVSNITT):
        raise ValueError(f"okänt avsnitt: {', '.join(sorted(okanda))}")
    return Arende(
        fil,
        falt(huvud),
        ingress,
        [handelse(rad) for rad in avsnitt.get("Händelser", [])],
        [handelse(rad, TILLFALLEN) for rad in avsnitt.get("Tycka till", [])],
        [mediepost(rad) for rad in avsnitt.get("I media och debatt", [])],
    )


def falt(huvud: str) -> dict[str, str]:
    rader = huvud.strip().splitlines()
    if fel := [rad for rad in rader if ": " not in rad]:
        raise ValueError(f"raden i front matter saknar nyckel: {fel[0]}")
    par = dict(rad.split(": ", 1) for rad in rader)
    if okanda := set(par) - set(KRAVS) - set(VALFRIA):
        raise ValueError(f"okänd nyckel: {', '.join(sorted(okanda))}")
    if saknas := [n for n in KRAVS if n not in par]:
        raise ValueError(f"nyckel saknas: {', '.join(saknas)}")
    return par


def dela(kropp: str) -> tuple[str, dict[str, list[str]]]:
    delar = re.split(r"^## (.+)$", kropp, flags=re.MULTILINE)
    avsnitt = {
        rubrik.strip(): [rad for rad in innehall.splitlines() if rad.strip()]
        for rubrik, innehall in zip(delar[1::2], delar[2::2])
    }
    return " ".join(delar[0].split()), avsnitt


def handelse(rad: str, stegen: Iterable[str] = STEG) -> Handelse:
    datum, steg, text, kalla = poster(rad, 4)
    if steg not in stegen:
        raise ValueError(f"okänt steg {steg!r}: {rad}")
    return Handelse(date.fromisoformat(datum), steg, text, *lank(kalla, rad))


def mediepost(rad: str) -> Mediepost:
    datum, rubrik, var = poster(rad, 3)
    return Mediepost(date.fromisoformat(datum), *lank(rubrik, rad), var)


def poster(rad: str, antal: int) -> list[str]:
    delar = rad.removeprefix("- ").split(" · ")
    if not rad.startswith("- ") or len(delar) != antal:
        raise ValueError(f"raden följer inte formatet: {rad}")
    return delar


def lank(text: str, rad: str) -> tuple[str, str]:
    if not (traff := LANK.fullmatch(text)):
        raise ValueError(f"källan är ingen https-länk: {rad}")
    return traff.group(1), traff.group(2)
