"""Krav: K26 i KRAV.md. Test: tests/test_handlingslankar.py.

Hittar ett ärendes tjänsteskrivelse bland sammanträdets handlingar. En sida
räknas till ärendet när diarienumret står i sidans huvud. Står det inget
diarienummer i huvudet räcker ärendets hela rubrik, eftersom rubrikerna
för till exempel projektbeställningar börjar likadant. En tjänsteskrivelse
känns igen på rubriken TJÄNSTESKRIVELSE i huvudet; ett protokollsutdrag
som nämner tjänsteskrivelsen räknas inte, och inte heller en förteckning över många ärenden. Finns ingen länkas den första
sidan i ärendet, utom för allmänna ärenden som information och anmälan av
beslut. Gick handlingarna inte att hämta ges punkten i kallelsen, så att
sammanträdets PDF kan länkas.
"""

import re

from handlingslankar.sidor import DIARIENUMMER, Paragraf, huvud, siffror

ALLMAN = re.compile(r"(information från|information -|anmälan av)", re.I)
TJANSTESKRIVELSE = re.compile(r"^\s*TJÄNSTESKRIVELSE", re.M)
PUNKT = re.compile(r"(\d+)\.?")
# En sida med många diarienummer, eller kallelsens kolumn Beteckning, är en
# förteckning eller förslagslista över många ärenden, inte ärendets handling.
FLERA_ARENDEN = 4
BETECKNING = re.compile(r"\bBeteckning\b")


def ord_(text: str) -> str:
    return re.sub(r"[^a-zåäö0-9 ]", "", re.sub(r"\s+", " ", text.lower())).strip()


def forteckning(text: str) -> bool:
    return len(set(DIARIENUMMER.findall(text))) >= FLERA_ARENDEN or bool(BETECKNING.search(huvud(text)))


def i_arendet(text: str, paragraf: Paragraf) -> bool:
    if forteckning(text):
        return False
    numren = {siffror(d) for d in DIARIENUMMER.findall(huvud(text))}
    if numren:
        return siffror(paragraf.diarienummer) in numren
    return bool(paragraf.rubrik) and ord_(paragraf.rubrik) in ord_(huvud(text))


def handling(handlingar: dict[int, str], paragraf: Paragraf) -> tuple[int, str] | None:
    funna = [nr for nr, text in sorted(handlingar.items()) if i_arendet(text, paragraf)]
    skrivelser = [nr for nr in funna if TJANSTESKRIVELSE.search(huvud(handlingar[nr]))]
    if skrivelser:
        return skrivelser[0], "Tjänsteskrivelse"
    if funna and not ALLMAN.match(paragraf.rubrik):
        return funna[0], "Handlingarna i ärendet"
    return None


def diarienummer_i(cell: str, paragraf: Paragraf) -> bool:
    return any(siffror(d) == siffror(paragraf.diarienummer) for d in DIARIENUMMER.findall(cell))


def punkt(kallelse: str, paragraf: Paragraf) -> str | None:
    for rad in kallelse.splitlines():
        celler = [c.strip() for c in rad.split("|")][1:]
        traff = PUNKT.fullmatch(celler[0]) if celler else None
        if traff and any(diarienummer_i(c, paragraf) for c in celler):
            return traff[1]
    return None
