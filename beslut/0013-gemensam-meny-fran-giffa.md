# 0013 – En gemensam meny för sajterna, ritad av ett skript från Giffå

## Sammanhang

Projektet har tre sajter på samma adress, moggleif.github.io: Giffå,
datapoolen kommunhandlingar (för läsaren *Kungsbacka kommun*) och
politik (*Kungsbacka i siffror*). Fler kommuner och regioner kan komma.
Projektägaren vill att Giffå håller ihop dem: man ska nå de andra sajterna
från Giffå och komma tillbaka. UX-analysen av menyerna 2026-11-15 visade
tre menyer med tre utseenden, tre sätt att visa var man är och tre
beteenden på mobilen, och att ingen nämnde de andra sajterna.

Tre sätt prövades: ett gemensamt skript från Giffå, en lista som varje
sajt hämtar när den byggs, och en rad i varje repo som Giffå kontrollerar.
Projektägaren valde skriptet, för att få en snyggare meny och fler
möjligheter, och att varje sajts meny ska följa samma form.

## Beslut

- **Giffå äger formen, varje sajt sitt innehåll.** `docs/sajter.css` och
  `docs/sajter.js` publiceras med Giffå och laddas av alla sajter med
  `/giffa/sajter.css` och `/giffa/sajter.js`. Eftersom sajterna delar
  adress räknas filerna som sajtens egna (`'self'`), också i politiks
  innehållspolicy.
- **Listan över sajterna står i `sajter.js`.** En ny sajt läggs till där.
  Blir de fler än fyra samlas de under en rubrik *Fler* – det byggs när
  den femte kommer.
- **Sajtens meny är vanlig HTML i en fast form** som varje sajt bygger
  själv: `<nav class="sajtmeny">` med `<a class="sajtnamn">` och en `<ul>`
  med högst sex poster. En post är en länk eller `<details>` med
  `<summary>` och en `<ul>`, eller `<div class="grupper">` med grupper av
  `<p class="grupp">` och `<ul>`. Den visade sidan har `aria-current`.
  Ingen fjärde nivå.
- **Skriptet lägger till det som kräver skript:** sajtraden före
  `.sajtmeny`, knappen *Meny* på smal skärm och att bara en undermeny är
  öppen. Utan skript står sajtens meny kvar som en lista.
- **Varje sajt sätter sin accentfärg och yta** med `--sajtaccent` och
  `--sajtyta`, och sajtradens bredd med `--sajtbredd` och `--sajtkant`.
- **Sökningen över alla sajter och ett gemensamt ortval** ingår inte nu;
  de blir egna steg.

## Konsekvenser

- En ändring i Giffå ändrar menyn på alla sajter vid nästa publicering av
  Giffå, utan att de andra repona rörs. Ett fel i skriptet syns också på
  alla; därför testas skriptet i `tests/test_sajter.js`.
- De andra sajterna är beroende av Giffå vid visning. Går filerna inte att
  nå står sajtens meny kvar utan stil och utan sajtrad.
- kommunhandlingar och politik bygger sin meny i formen ovan och laddar de
  två filerna; i övrigt bestämmer de själva över sina menyer.
