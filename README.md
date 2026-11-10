# Giffå – bevakning av södra Kungsbacka

Vad som beslutas, planeras och byggs i Gällinge, Idala, Fjärås, Frillesås,
Förlanda och Åsa: kommunstyrelsen, dess arbetsutskott, nämnderna, bygglov,
detaljplaner och det kommunen publicerar på kungsbacka.se.

**Sidan: <https://moggleif.github.io/giffa/>** – när och var man kan tycka
till innan något beslutas, det nya sedan förra rundan, det som pågår och
det som är beslutat, en historik över det som är
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
skanning/    Söker igenom kommunhandlingar inför månadens runda.
tests/       Testerna för bygget och skanningen.
KALLOR.md    Varifrån uppgifterna hämtas.
kunskap/     Bakgrund om södra Kungsbacka, med källor.
OMRADE.md    Vilka orter och områden som räknas till bevakningen.
platser.csv  Skolor, boenden, idrott, föreningar och planer i orterna.
```

Ett ärende att följa läggs upp som ett issue med mallen *Bevaka ett ärende*.

## Månadens runda

Den första i varje månad söker `skanning.yml` igenom kommunhandlingar efter
orterna, platserna och de öppna ärendena från början av förra rundans
period och öppnar ett
issue med etiketten `runda` ([beslut 0003](beslut/0003-manadens-skanning-i-actions.md)).
Rundan – att föra in träffarna som ärenden – görs sedan av en agent enligt
faserna i `AGENTS.md`, till exempel genom att be den "köra rundan".
Sökningen går också att köra lokalt:

```
python3 -m skanning <kommunhandlingar>/data/kungsbacka https://moggleif.github.io/kommunhandlingar
```
