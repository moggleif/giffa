"""Krav: K1, K4, K10, K12 och K25 i KRAV.md. Test: tests/test_arende.py.

Läser ett ärende enligt formatet i bevakning/README.md och stoppar med
felet när något inte följer det.
"""

import re
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

STATUS = ("pågår", "beslutat", "klart", "avbrutet")
STEG = {
    "forslag": "förslag",
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
AVSNITT = ("Förslaget i korthet", "Händelser", "Tycka till", "I media och debatt")
LANK = re.compile(r"\[([^\]]+)\]\((https://\S+)\)")
HANDLINGAR = re.compile(rf"Handlingar: {LANK.pattern}(?:, {LANK.pattern})*")


@dataclass(frozen=True)
class Handelse:
    datum: date
    steg: str
    text: str
    kalla: str
    lank: str
    handlingar: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class Punkt:
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
    forslaget: list[Punkt]

    @property
    def id(self) -> str:
        return self.fil.rsplit("/", 1)[-1].removesuffix(".md")

    @property
    def sida(self) -> str:
        return f"arende/{self.id}.html"

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
        [punkt(rad) for rad in avsnitt.get("Förslaget i korthet", [])],
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
    datum, steg, text, kalla, *resten = poster(rad, 4, 5)
    if steg not in stegen:
        raise ValueError(f"okänt steg {steg!r}: {rad}")
    datum = date.fromisoformat(datum)
    return Handelse(datum, steg, text, *lank(kalla, rad), handlingar(resten, rad))


def handlingar(resten: list[str], rad: str) -> tuple[tuple[str, str], ...]:
    if resten and not HANDLINGAR.fullmatch(resten[0]):
        raise ValueError(f"handlingarna är inte https-länkar efter 'Handlingar: ': {rad}")
    return tuple(LANK.findall(resten[0])) if resten else ()


def punkt(rad: str) -> Punkt:
    text, kalla = poster(rad, 2)
    return Punkt(text, *lank(kalla, rad))


def mediepost(rad: str) -> Mediepost:
    datum, rubrik, var = poster(rad, 3)
    return Mediepost(date.fromisoformat(datum), *lank(rubrik, rad), var)


def poster(rad: str, minst: int, hogst: int = 0) -> list[str]:
    delar = rad.removeprefix("- ").split(" · ")
    if not rad.startswith("- ") or not minst <= len(delar) <= max(minst, hogst):
        raise ValueError(f"raden följer inte formatet: {rad}")
    return delar


def lank(text: str, rad: str) -> tuple[str, str]:
    if not (traff := LANK.fullmatch(text)):
        raise ValueError(f"källan är ingen https-länk: {rad}")
    return traff.group(1), traff.group(2)
