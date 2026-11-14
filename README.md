# Giffå – bevakning av Kungsbacka, förening för förening

Vad som beslutas, planeras och byggs i Kungsbacka kommun, uppdelat på fyra
föreningars områden – Förening Åsa, Förening Kungsbacka, Förening Onsala
och Förening Särö (se [OMRADE.md](OMRADE.md)): kommunstyrelsen, dess
arbetsutskott, nämnderna, bygglov, detaljplaner och det kommunen publicerar
på kungsbacka.se.

**Sidan: <https://moggleif.github.io/giffa/>** – på startsidan när och var
man kan tycka till innan något beslutas, dag för dag och med två spår –
partierna före sammanträdet och alla i samråd och granskning – det som är
på väg upp, där ett organ har informerats men inget förslag finns än, de
uppmärksammade ärendena med
namnen de har i folkmun, som också står först i varje lista, och det nya
sedan förra rundan; på
egna sidor det som pågår (det som rört sig de senaste två åren först), det
som är beslutat, en historik över det som är klart, en sökning på rubrik,
namn och ort, vad som bevakas och en sida för varje ärende. Listorna visar en tidslinje och kort, på mobilen bara
korten. Fastighetsbeteckningar, platser, gator och detaljplaner i ett ärende
länkar till kommunens karta. Varje pågående plan visar på kortet och sin sida var den står i plan- och
bygglagens process och vilka steg som kommer. Ärendets sida har länkar direkt till handlingarna
under de steg där underlaget finns och, för förslag med innehåll, förslaget i korthet.
Utan val syns allt; den som vill väljer en ort direkt, eller först en
förening för att bara se dess orter, och valet står i adressen och följer
med mellan sidorna. Sidan byggs ur ärendena av `webbplats/` och publiceras
på GitHub Pages ([beslut 0002](beslut/0002-sidan-byggs-ur-arendena-i-pages-flodet.md)).
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
handlingslankar/ Lägger handlingarna intill protokollen i ärendena.
tests/       Testerna för bygget, skanningen och handlingslänkarna.
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

## Söndagens handlingar och runda

Varje söndag lägger `handlingar.yml` ärendets handling ur samma
sammanträdes handlingar – tjänsteskrivelsen, ärendets sida eller
sammanträdets PDF – intill protokollet på de händelser som bara länkar
ett protokoll, och öppnar en PR (K26). Senare samma morgon gör en schemalagd
Claude-runda en bevakningsrunda ovanpå den: nya händelser, tillfällen att
tycka till och nya ärenden, i en PR som projektägaren godkänner. Rundan är
en schemalagd uppgift i Claude, inte en fil i repot
([beslut 0009](beslut/0009-handlingslankar-och-sondagsrunda.md)). Lokalt:
`python3 -m handlingslankar <kommunhandlingar>/data/kungsbacka https://moggleif.github.io/kommunhandlingar`.
