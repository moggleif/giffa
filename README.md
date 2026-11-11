# Giffå – bevakning av Kungsbacka, förening för förening

Vad som beslutas, planeras och byggs i Kungsbacka kommun, uppdelat på fyra
föreningars områden – Förening Åsa, Förening Kungsbacka, Förening Onsala
och Förening Särö (se [OMRADE.md](OMRADE.md)): kommunstyrelsen, dess
arbetsutskott, nämnderna, bygglov, detaljplaner och det kommunen publicerar
på kungsbacka.se.

**Sidan: <https://moggleif.github.io/giffa/>** – på startsidan när och var
man kan tycka till innan något beslutas och det nya sedan förra rundan; på
egna sidor det som pågår (det som rört sig de senaste två åren först), det
som är beslutat, en historik över det som är klart, vad som bevakas och en
sida för varje ärende. Listorna visar en tidslinje och kort, på mobilen bara
korten. Utan val syns allt; den som vill väljer en förening och sedan en ort,
och valet står i adressen och följer med mellan sidorna. Sidan byggs ur
ärendena av `webbplats/` och publiceras på GitHub Pages
([beslut 0002](beslut/0002-sidan-byggs-ur-arendena-i-pages-flodet.md)).
Bygg den lokalt med

```
python3 -m webbplats _site https://github.com/moggleif/giffa
python3 -m unittest discover -s tests -t .
node --test tests/*.js
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
kunskap/     Bakgrund om orterna och om sidans läsare, med källor.
OMRADE.md    Föreningarna och vilka orter som hör till var och en.
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

## Veckans kallelser

Varje måndag söker `kallelser.yml` igenom kallelserna och handlingarna till
kommande sammanträden på samma sätt och öppnar ett issue med etiketten
`kallelser` när något träffar ([beslut 0005](beslut/0005-veckans-kallelser.md)).
Det som rör ett bevakat ärende förs in under *Tycka till*, så att det syns
på sidan före mötet. Lokalt: `python3 -m skanning --kommande …`.
