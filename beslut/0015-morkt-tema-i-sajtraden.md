# 0015 – Mörkt tema för alla sajterna, med en ikonknapp i sajtraden

## Sammanhang

Bara Kungsbacka kommun och Region Halland hade mörkt tema
(kungsbackakommuns ADR-0074), med en textknapp *Mörkt tema* sist i
sajtens meny. Sedan sajtraden blev en rad på mobilen
([beslut 0014](0014-sajtens-namn-en-gang.md)) låg knappen bakom *Meny*,
och på datorn tog texten plats i menyraden. Giffå och Kungsbacka i siffror
hade inget mörkt tema. Projektägaren bad 2026-11-16 om mörkt tema på alla
sidor, med en ikon i stället för text, mitt på i mobilvyn och på en
lämplig plats på datorn.

## Övervägda alternativ

- **Varje sajt har sin egen knapp.** Så var det; fyra knappar glider isär
  och valet följer inte med mellan sajterna.
- **Knappen i den gemensamma menyn, temat valt i `sajter.js`.** `sajter.js`
  laddas med `defer`, så ett sparat mörkt tema skulle först ritas ljust.
- **Knappen i den gemensamma menyn, temat valt av ett litet skript i
  `<head>`.** Valt.

## Beslut

- **`tema.js`** laddas utan `defer` i varje sidas `<head>` och sätter
  `data-tema` (`ljust` eller `morkt`) på `<html>` ur lagringen innan sidan
  ritas. Nyckeln är `sajter-tema`, och eftersom sajterna har samma värd
  gäller valet på alla.
- **`sajter.js`** lägger knappen i sajtraden, före *Meny*. Den har
  etiketten *Mörkt tema* och `aria-pressed`, och ikonen (måne eller sol)
  ritas av `sajter.css` som en mask i textens färg, så att den följer
  sajtens färger. På mobilen står knappen mitt på raden, mitt i utrymmet
  mellan sajtens namn och *Meny*; med ett kort namn är det mitt på
  skärmen, med ett långt en bit till höger. På datorn står den längst till höger i sajtraden.
- **`sajter.css`** sätter `color-scheme` efter `data-tema`. Varje sajt
  skriver sina färger med `light-dark()` och `color-scheme: light dark`,
  som kungsbackakommun redan gör (ADR-0074 där). En webbläsare utan
  `light-dark()` får ljusa färger och ingen knapp.
- Giffås färger står som variabler i `stil.css` med ett ljust och ett mörkt
  värde.

## Konsekvenser

- Varje sajt laddar `tema.js` och har mörka färger; kungsbackakommun tar
  bort sin egen knapp och sitt eget skript, och ett val som sparats under
  dess gamla nyckel gäller inte längre.
- En sajt som ritar i JavaScript, som diagrammen på Kungsbacka i siffror,
  får läsa temat själv och rita om när `data-tema` byts.
- politik har en fryst kopia av den gemensamma menyn i sina tester och
  kopierar in `tema.js` och de nya `sajter.*`.
