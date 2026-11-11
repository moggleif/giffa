"""Krav: K8 och K22 i KRAV.md. Test: tests/test_sidor.py.

Sidan om vad som bevakas, byggd ur OMRADE.md, platser.csv och KALLOR.md så
att uppgifterna bara står på ett ställe.
"""

from html import escape

from webbplats.mall import Sajt, sida

RUNDAN = (
    "<p>En bevakningsrunda görs en gång i månaden. Den söker igenom källorna "
    "nedan efter orterna och efter namnen på platserna, eftersom en handling "
    "ofta bara nämner skolan, planen eller fastigheten. Det som hittas förs in "
    "som ärenden; det som är nytt sedan förra rundan står överst på startsidan.</p>"
)


def bevakar(sajt: Sajt, platser: list[dict[str, str]], kallor: list[list[str]]) -> str:
    innehall = (
        RUNDAN
        + "<h2>Föreningarna och orterna</h2>"
        + "".join(forening(namn, orter) for namn, orter in sajt.foreningar.items())
        + f"<p>Vad som räknas till varje förening står i {fil(sajt, 'OMRADE.md')}.</p>"
        + kalltabell(sajt, kallor)
        + platstabell(sajt, platser)
    )
    return sida(sajt, "bevakar.html", "Vad vi bevakar", innehall)


def forening(namn: str, orter: list[str]) -> str:
    return f"<h3>{escape(namn)}</h3><p>{escape(', '.join(orter))}</p>"


def fil(sajt: Sajt, namn: str) -> str:
    return f'<a href="{escape(sajt.repo)}/blob/main/{namn}">{namn}</a>'


def kalltabell(sajt: Sajt, kallor: list[list[str]]) -> str:
    rader = "".join(
        f'<tr><th scope="row">{escape(namn)}</th><td>{escape(vad)}</td>'
        f'<td><a href="{escape(adress)}">{escape(adress)}</a></td></tr>'
        for namn, vad, adress in kallor
    )
    return (
        '<h2>Källorna</h2><div class="tabell"><table><thead><tr><th>Källa</th>'
        f"<th>Vad den ger</th><th>Adress</th></tr></thead><tbody>{rader}</tbody>"
        f"</table></div><p>Hur varje källa får hämtas står i {fil(sajt, 'KALLOR.md')}.</p>"
    )


def platstabell(sajt: Sajt, platser: list[dict[str, str]]) -> str:
    rader = "".join(platsrad(p) for p in sorted(platser, key=lambda p: (p["ort"], p["typ"])))
    return (
        f"<h2>Platserna</h2><p>{len(platser)} platser ur {fil(sajt, 'platser.csv')}, "
        "med antalet handlingar i kommunhandlingar som nämner dem.</p>"
        '<div class="tabell"><table><thead><tr><th>Plats</th><th>Typ</th><th>Ort</th>'
        f"<th>Anteckning</th><th>Handlingar</th></tr></thead><tbody>{rader}</tbody></table></div>"
    )


def platsrad(plats: dict[str, str]) -> str:
    namn = escape(plats["namn"])
    if plats["exempel"].startswith("https://"):
        namn = f'<a href="{escape(plats["exempel"])}">{namn}</a>'
    return (
        f'<tr><th scope="row">{namn}</th><td>{escape(plats["typ"])}</td>'
        f"<td>{escape(plats['ort'])}</td><td>{escape(plats['anteckning'])}</td>"
        f'<td class="tal">{escape(plats["handlingar"])}</td></tr>'
    )
