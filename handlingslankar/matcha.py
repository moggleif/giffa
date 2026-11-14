"""Krav: K26 i KRAV.md. Test: tests/test_handlingslankar.py.

Hittar ett ärendes tjänsteskrivelse bland sammanträdets handlingar på
diarienumret eller rubriken. Sidor som listar många ärenden, som
innehållsförteckningar och förslagslistor, hoppas över. Ett allmänt ärende,
som information eller anmälan av beslut, länkas bara via tjänsteskrivelsen.
Gick handlingarna inte att hämta till poolen ges punkten i kallelsen, så att
sammanträdets PDF kan länkas.
"""

import re

from handlingslankar.sidor import Paragraf, kod

ALLMAN = re.compile(r"(information från|information -|anmälan av)", re.I)
FORTECKNING = re.compile(r"\.{5,}|…{3,}")
DIARIENUMMER = re.compile(r"\b20\d\d-\d{5}\b")


def forteckning(text: str) -> bool:
    return len(FORTECKNING.findall(text)) >= 3 or len(set(DIARIENUMMER.findall(text))) >= 4


def ord_(text: str) -> str:
    return re.sub(r"[^a-zåäö0-9 ]", "", re.sub(r"\s+", " ", text.lower())).strip()


def traffar(handlingar: dict[int, str], paragraf: Paragraf) -> list[int]:
    nummer, titel = kod(paragraf.diarienummer), ord_(paragraf.rubrik)[:60]
    return [
        nr for nr, text in sorted(handlingar.items())
        if nr > 0 and not forteckning(text)
        and (nummer in kod(text) or (len(titel) > 25 and titel in ord_(text)))
    ]


def handling(handlingar: dict[int, str], paragraf: Paragraf) -> tuple[int, str] | None:
    funna = traffar(handlingar, paragraf)
    for nr in funna:
        if re.search("tjänsteskrivelse", "".join(handlingar[nr].splitlines(True)[:30]), re.I):
            return nr, "Tjänsteskrivelse"
    if not funna or funna[0] <= 3 or ALLMAN.match(paragraf.rubrik):
        return None
    return funna[0], "Handlingarna i ärendet"


def punkt(kallelse: str, paragraf: Paragraf) -> str | None:
    nummer = kod(paragraf.diarienummer)
    for rad in kallelse.splitlines():
        celler = [c.strip() for c in rad.split("|")]
        if len(celler) > 4 and any(len(kod(c)) >= 9 and kod(c) in nummer for c in celler):
            traff = re.fullmatch(r"(\d+)\.?", celler[1])
            if traff:
                return traff[1]
    return None
