# Giffå – bevakning av södra Kungsbacka

Vad som beslutas, planeras och byggs i Gällinge, Idala, Fjärås, Frillesås,
Förlanda och Åsa: kommunstyrelsen, dess arbetsutskott, nämnderna, bygglov,
detaljplaner och det kommunen publicerar på kungsbacka.se.

**Sidan: <https://moggleif.github.io/giffa/>** – det nya sedan förra
rundan, det som pågår och det som är beslutat, en historik över det som är
klart och vad som bevakas. Den byggs ur ärendena av `webbplats/` och
publiceras på GitHub Pages ([beslut 0002](beslut/0002-sidan-byggs-ur-arendena-i-pages-flodet.md)).
Bygg den lokalt med

```
python3 -m webbplats _site https://github.com/moggleif/giffa
python3 -m unittest discover -s tests -t .
```

## Struktur

```
bevakning/   Ett ärende per fil, ordnat efter källa, och rundorna (se bevakning/README.md).
.claude/     Agentinstruktioner: faserna och granskaren (se AGENTS.md).
beslut/      Beslut som är svåra att ändra.
KRAV.md      Vad bevakningen ska göra.
webbplats/   Bygger sidan ur bevakning/, OMRADE.md, platser.csv och KALLOR.md.
docs/        Sidans stil och skript, som kopieras med i bygget.
tests/       Testerna för bygget.
KALLOR.md    Varifrån uppgifterna hämtas.
kunskap/     Bakgrund om södra Kungsbacka, med källor.
OMRADE.md    Vilka orter och områden som räknas till bevakningen.
platser.csv  Skolor, boenden, idrott, föreningar och planer i orterna.
```

Ett ärende att följa läggs upp som ett issue med mallen *Bevaka ett ärende*.
