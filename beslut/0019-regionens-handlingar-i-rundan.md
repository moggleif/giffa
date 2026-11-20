# 0019 – Regionens handlingar i rundan, med samma skanning

## Sammanhang

Region Halland beslutar om vård, tandvård, kollektivtrafik, regionala
vägar och folkhögskolan i Åsa, och yttrar sig över kommunens
detaljplaner. Projektägaren har lagt regionens handlingar som text i
`moggleif/regionhalland`, byggd med samma kod som kommunens datapool och
i samma format: `data/regionhalland/<organ>/<år>/<datum>/`. Regionens
handlingar nämner sällan orterna; de skriver *Kungsbacka* om allt i
kommunen, också om vårdcentralen i Fjärås eller busslinjen till Åsa.

## Beslut

- **Samma skanning, en källa i taget.** `skanning` tar källan som
  argument, och `skanning.yml` och `kallelser.yml` kör den för båda
  repona med en matris. Varje källa får sitt eget issue, så att en lång
  rapport inte tränger undan den andra.
- **Kommunens namn som extra term, bara i regionens handlingar.** I
  kommunens egna handlingar skulle *Kungsbacka* träffa varje sida. Namnet
  står i arbetsflödet, med `--kommunnamn`, inte i koden.
- **Bilagorna fälls ihop som handlingarna.** Allt som inte är protokoll
  eller kallelse räknas som handlingar i rapporten; regionens bilagor
  heter `bilaga-*.md`.
- **Regionens egna ärenden i `bevakning/region/`**, med regionens organ.
  Ett ärende som gäller hela kommunen tas med när det får betydelse för en
  ort, som `OMRADE.md` säger. Regionens yttranden över kommunens
  detaljplaner läggs i planens ärende.
- **Länkar:** protokoll och kallelser till sidan på regionens webbplats
  med `#sida-N`. En bilaga visas där bara med sin härkomst, så den länkas
  till texten i `moggleif/regionhalland` på GitHub.

## Konsekvenser

- Ortnamnet *Åsa* är också ett förnamn och ger träffar i regionens
  handlingar som inte rör orten. Rundan sorterar bort dem.
- Ett nytt repo med samma format kan läggas till som en rad i matrisen.
- Rapportens rubrik och de källor som inte söktes automatiskt tar källans
  namn ur dokumentbasens sista led, så `KALLOR.md` länkar repona med deras
  nuvarande namn.
