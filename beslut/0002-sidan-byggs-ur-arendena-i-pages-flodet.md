# 0002 – Sidan byggs ur ärendena i Pages-flödet

## Sammanhang

Projektägaren vill ha en startsida med det som är nytt, pågår och är
beslutat, en historik för det som är klart och en sida om vad som bevakas.
Ärendena ska visas som spåren i kommunhandlingar – initiativ och
lokalbehov – med en tabell över åren och ett kort per ärende. Ärendena
ligger som Markdown i `bevakning/`, platserna och källorna i egna filer.
Skrivs sidan för hand står varje uppgift på två ställen.

## Beslut

- Paketet `webbplats/` bygger sidorna ur `bevakning/`, `OMRADE.md`,
  `platser.csv` och `KALLOR.md` med bara Pythons standardbibliotek:
  `python3 -m webbplats <utkatalog> <repoadress>`. Det körs i `pages.yml`
  vid varje ändring på `main`; inget genererat checkas in.
- `docs/` håller det som inte byggs: stilen, skriptet för urvalet och
  `.nojekyll`. Bygget kopierar dem till utkatalogen.
- Ärendets `status` sätts för hand och styr var det står: `pågår` och
  `beslutat` på startsidan, `klart` och `avbrutet` i historiken. Den räknas
  inte fram ur stegen, eftersom ett beslut i ett ärende – ett avtal, en
  budget – inte avgör ärendet.
- Varje händelse har ett steg ur en fast lista, som ger ikonen i tabellen.
- *Nytt* är händelserna inom förra rundans period, som står sist i
  `bevakning/rundor.csv`. Rundan görs en gång i månaden.
- Ett ärende som inte följer formatet stoppar bygget i stället för att
  visas fel. `kontroll.yml` bygger sidan och kör testerna på varje PR.

## Konsekvenser

Format, sida och data hålls i takt: en ny nyckel, status eller ett nytt steg
kräver en ändring i `webbplats/` och i `bevakning/README.md` samtidigt.
Sidan går inte att förhandsgranska utan att köra bygget lokalt. Sidan
laddar inget utifrån; urvalet är ett litet skript och utan det står allt.
