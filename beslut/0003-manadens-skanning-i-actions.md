# 0003 – Månadens skanning i Actions, rundan skrivs av en agent

## Sammanhang

Bevakningsrundan görs en gång i månaden. Att söka igenom hundratals
handlingar efter orter och platser är mekaniskt; att föra in träffarna som
ärenden kräver omdöme. En Action som kör en språkmodell kräver en
API-nyckel som secret och kostar per körning. Kungsbacka.se och tidningarna
har sidor som ändras och regler för automatisk hämtning (`KALLOR.md`).

## Beslut

- Paketet `skanning/` söker med bara standardbiblioteket igenom
  kommunhandlingars dokument från dagen efter förra rundan, sida för sida,
  efter orterna, platserna och de öppna ärendenas diarienummer.
- `skanning.yml` kör det den första i varje månad och öppnar ett issue med
  etiketten `runda`. Ingen API-nyckel behövs.
- Issuet återger ingen text ur handlingarna, bara datum, organ, sidor och
  termer, eftersom handlingarna kan innehålla personnamn.
- Rundan – sortera, skriva ärenden, kungsbacka.se och tidningarna – görs av
  en agent med faserna R1–R2 och utgår från issuet.

## Konsekvenser

Varje månad finns ett underlag utan att någon behöver starta något. En
runda som inte blir av gör att nästa issue täcker två månader, eftersom
perioden räknas från förra rundan. Bara årets och fjolårets handlingar
hämtas. Kungsbacka.se, kartan och tidningarna söks inte automatiskt.
