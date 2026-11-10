"""Krav: K4, K5, K6 och K9 i KRAV.md. Test: tests/test_sidor.py.

Ett kort per ärende under tabellen, och korten för det som är nytt sedan
förra rundan överst på startsidan.
"""

from html import escape

from webbplats.arende import STEG, Arende, Handelse


def kort(arende: Arende, repo: str) -> str:
    falt, senaste = arende.falt, arende.handelser[0]
    return (
        f'<article id="{arende.id}" data-ort="{escape("|".join(arende.orter))}">'
        f"{markor(arende)}<h3>{escape(falt['rubrik'])}</h3>"
        f'<p class="organ">{escape(organ(arende))}</p>'
        + (f"<p>{escape(arende.ingress)}</p>" if arende.ingress else "")
        + f"<p>Senast: {STEG[senaste.steg]} {senaste.datum}</p>"
        + synpunkter(arende)
        + f"<details><summary>Läs mer: händelserna och källorna, "
        f"{len(arende.handelser)} st</summary>"
        f"<ol>{''.join(post(h) for h in arende.handelser)}</ol>{media(arende)}"
        f'<p><a href="{escape(repo)}/blob/main/{escape(arende.fil)}">Ärendet i repot</a>'
        "</p></details></article>"
    )


def markor(arende: Arende) -> str:
    forsta, sista = arende.handelser[-1].datum.year, arende.handelser[0].datum.year
    aren = str(forsta) if forsta == sista else f"{forsta}–{sista}"
    orter = "".join(f"<span>{escape(o)}</span>" for o in arende.orter)
    return f'<p class="markor"><span>{aren}</span>{orter}</p>'


def organ(arende: Arende) -> str:
    diarienummer = arende.falt.get("diarienummer")
    return arende.falt["organ"] + (f" · {diarienummer}" if diarienummer else "")


def synpunkter(arende: Arende) -> str:
    if "synpunkter" not in arende.falt:
        return ""
    senast = arende.falt.get("synpunkter_senast")
    nar = f" senast {senast}" if senast else ""
    return (
        f'<p class="paverka">Lämna synpunkter{escape(nar)}: '
        f'<a href="{escape(arende.falt["synpunkter"])}">så gör du</a></p>'
    )


def post(handelse: Handelse) -> str:
    return (
        f"<li><time>{handelse.datum}</time> <strong>{STEG[handelse.steg]}</strong> "
        f"{escape(handelse.text)} "
        f'<a href="{escape(handelse.lank)}">{escape(handelse.kalla)}</a></li>'
    )


def media(arende: Arende) -> str:
    if not arende.media:
        return ""
    poster = "".join(
        f'<li><time>{m.datum}</time> <a href="{escape(m.lank)}">{escape(m.rubrik)}</a>'
        f" – {escape(m.var)}</li>"
        for m in arende.media
    )
    return f"<h4>I media och debatt</h4><ul>{poster}</ul>"


def nytt_kort(arende: Arende, nya: list[Handelse], adress: str) -> str:
    return (
        f'<article data-ort="{escape("|".join(arende.orter))}">{markor(arende)}'
        f"<h3>{escape(arende.falt['rubrik'])}</h3>"
        f"<details><summary>{len(nya)} ny{'a' * (len(nya) > 1)} "
        f"händelse{'r' * (len(nya) > 1)}</summary>"
        f"<ol>{''.join(post(h) for h in nya)}</ol></details>"
        f'<p><a href="{escape(adress)}#{arende.id}">Hela ärendet</a></p></article>'
    )
