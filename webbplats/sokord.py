"""Krav: K34 i KRAV.md, beslut 0012. Test: tests/test_ksmotet.py.

Sökorden på en punkt på dagordningen: vad rubriken säger att ärendet är,
ur en kort lista ord, och platserna i platser.csv som rubriken eller
förslaget nämner. Högst två ord ur listan och högst fyra sökord i allt,
så att märkena går att läsa.
"""

from skanning.termer import monster
from webbplats.kallelsen import Punkten

ORDEN = (
    ("planbesked", "Planbesked"),
    ("detaljplan", "Detaljplan"),
    ("exploateringsavtal", "Exploateringsavtal"),
    ("lokalprojekt", "Lokalprojekt"),
    ("remiss", "Remiss"),
    ("taxa", "Taxa"),
    ("delårsrapport", "Delårsrapport"),
    ("budget", "Budget"),
    ("borgen", "Borgen"),
    ("initiativ", "Initiativ"),
    ("motion", "Motion"),
    ("medborgarförslag", "Medborgarförslag"),
    ("information", "Information"),
)
HOGST = 4


def sokord(punkten: Punkten, platser: list[dict[str, str]]) -> list[str]:
    rubrik = punkten.punkt.rubrik.lower()
    orden = [sokordet for ordet, sokordet in ORDEN if ordet in rubrik][:2]
    namn = [p["namn"] for p in platser if monster(p["namn"]).search(punkten.kallelsen)]
    return list(dict.fromkeys(orden + namn))[:HOGST]
