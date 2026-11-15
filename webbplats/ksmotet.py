"""Krav: K34 i KRAV.md, beslut 0012. Test: tests/test_ksmotet.py.

Sidan om kommunstyrelsens kommande sammanträde: länkarna till kallelsen,
handlingarna och datapoolens sida, en översikt med en rad per punkt och en
kolumn per förening, och sedan dagordningen i kallelsens ordning, en punkt
i taget (`motespunkt.py`). Det som saknas sägs.
"""

from html import escape

from webbplats.arende import Arende
from webbplats.datum import klartext
from webbplats.kallelsen import Motet
from webbplats.mall import Sajt, sida
from webbplats.motespunkt import POOL, punktkort, rubriken
from webbplats.punktkoppling import Kopplad, koppla

SIDA = "ks-motet.html"


def ks_motet(sajt: Sajt, motet: Motet | None, arenden: list[Arende], platser: list[dict]) -> str:
    if motet is None:
        text = "<p>Inget kommande sammanträde i kommunstyrelsen i kalendern.</p>"
        return sida(sajt, SIDA, "Kommunstyrelsens nästa sammanträde", text)
    rubrik = f"Kommunstyrelsen {klartext(motet.datum)}"
    if motet.punkter is None:
        return sida(sajt, SIDA, rubrik, "<p>Kallelsen finns inte i datapoolen än.</p>")
    kopplade = [koppla(p, sajt.orter, platser, arenden) for p in motet.punkter]
    inledning = foregaende(motet) + kallorna(motet)
    return sida(sajt, SIDA, rubrik, inledning + innehall(sajt, motet, kopplade))


def foregaende(motet: Motet) -> str:
    if not motet.foregaende:
        return ""
    nasta = "Nästa sammanträde finns inte i kalendern än."
    if motet.nasta:
        nasta = f"Kallelsen till nästa, {klartext(motet.nasta)}, finns inte i datapoolen än."
    return f'<div class="paverka"><p>Det här är föregående sammanträde.</p><p>{nasta}</p></div>'


def kallorna(motet: Motet) -> str:
    bas = f"{POOL}/{motet.katalog}"
    return (
        f'<p><a href="{bas}/kallelse.html">Kallelsen</a> · '
        + (f'<a href="{bas}/handlingar.html">Handlingarna</a> · ' if motet.handlingar else "")
        + f'<a href="{bas}.html">Punkt för punkt i datapoolen</a></p>'
    )


def innehall(sajt: Sajt, motet: Motet, kopplade: list[Kopplad]) -> str:
    if not kopplade:
        return "<p>Dagordningen gick inte att läsa ur kallelsen.</p>"
    return (
        oversikt(sajt.foreningar, kopplade)
        + f"<h2>Dagordningen, {len(kopplade)} {'punkt' if len(kopplade) == 1 else 'punkter'}</h2>"
        + '<div class="kort punkter">'
        + "".join(punktkort(sajt, motet, k) for k in kopplade)
        + "</div>"
    )


# En rad per punkt och en kolumn per förening: ● när en ort eller plats i
# föreningen står i kallelsen, ○ när den bara står i handlingen.
def oversikt(foreningar: dict[str, list[str]], kopplade: list[Kopplad]) -> str:
    huvud = "".join(f'<th scope="col">{escape(kortnamn(n))}</th>' for n in foreningar)
    rader = "".join(
        f'<tr><th scope="row">{nummerlank(k)} {escape(rubriken(k.punkten))}</th>'
        + "".join(cell(k, kortnamn(n), orter) for n, orter in foreningar.items())
        + "</tr>"
        for k in kopplade
    )
    return (
        '<table class="matris"><caption>● nämns i kallelsen · ○ bara i handlingen</caption>'
        f'<thead><tr><th scope="col">Punkt</th>{huvud}</tr></thead><tbody>{rader}</tbody></table>'
    )


def kortnamn(forening: str) -> str:
    return forening.removeprefix("Förening ")


def cell(k: Kopplad, forening: str, orter: list[str]) -> str:
    funna = [t for t in k.traffar if t.ort in orter]
    if not funna:
        return "<td></td>"
    tecken = "○" if all(t.i_handlingen for t in funna) else "●"
    namn = ", ".join(dict.fromkeys(t.ort for t in funna))
    return (
        f'<td data-forening="{escape(forening)}" title="{escape(namn)}">'
        f"{tecken} <small>{escape(namn)}</small></td>"
    )


def nummerlank(k: Kopplad) -> str:
    nummer = k.punkten.punkt.nummer
    return f'<a href="#punkt-{nummer}">{nummer}</a>'
