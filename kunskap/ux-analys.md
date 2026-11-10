# UX-analys: sidan för politiker och äldre läsare

Varför sidan på <https://moggleif.github.io/giffa/> inte blev så bra som
den borde, och vad som görs åt det. Analysen gjordes 2026-11-10 på sidan
byggd ur `main` efter historiken (PR #15, commit `eb92bdb`), med 108
ärenden. Måtten är ögonblicksbilder, uppmätta med Playwright i Chromium på
en datorskärm 1280 punkter bred och en emulerad iPhone 12, 390 punkter bred. Varje åtgärd har ett issue med etiketten `ux`.

Läsarna som analysen utgår från:

- **Förtroendevalda** som vill se vad som är på väg upp i deras nämnd eller
  ort, hitta ett ärende snabbt och skicka en länk till det.
- **Äldre boende** som läser på mobilen eller surfplattan, ofta med större
  text, och som vill veta om något berör dem och om det går att säga sitt.

Kärnmålet är detsamma för båda: varje ärende ska visa **i vilka steg man
kan tycka till och när**, så att man hinner före beslutet.

## Varför det inte blev bra

Sidan byggdes inifrån och ut. Formatet för ärendena kom först, och sidan
visar det formatet: tidslinjen är lånad från kommunhandlingars sidor om
initiativ och lokalbehov (se [tabell.py](../webbplats/tabell.py)), och den
ger mest åt den som jämför många ärenden på en gång. Frågorna läsarna kommer med – *vad händer i min ort*,
*kan jag påverka det här*, *när* – fick ett avsnitt var, men aldrig sidans
form. Med fyra startärenden märktes det inte; med 108 ärenden från tretton
år gör det.

Fem saker förklarar det mesta:

1. **Allt står på en sida.** Startsidan är 17 400 punkter hög på datorn och
   43 700 på mobilen, med 84 kort, två tidslinjer och 766 länkar. Det som
   går att påverka är fyra rader överst, och resten trycker ner allt annat.
2. **Tidslinjen är byggd för en bred skärm.** Den har en kolumn per år från
   2013 till 2026. På mobilen trycks årtalen ihop till oläslig text,
   rubrikerna bryts i fyra–fem rader, och den som drar i sidled ser bara
   ett par år åt gången. Flera händelser samma år staplas på höjden, så
   raderna blir höga och ikonerna hamnar under fel ärende för ögat.
3. **Datum och ord är skrivna för maskiner och handläggare.** Datum står
   som `2026-11-24` utan veckodag och utan hur långt det är kvar. Stegen
   heter *förslag eller uppdrag*, *yttrande* och *information*, kortet
   säger *Senast: förslag eller uppdrag 2026-11-03*, och rundans anteckning
   talar om arbetsmiljön.
4. **Hur man påverkar ligger gömt.** Förklaringen till varje steg står i en
   hopfälld ruta under listan. Ett tillfälle säger *Beslut väntas,
   preliminärt* men inte vad läsaren kan göra före det: vem man skriver
   till, eller att ett samråd är öppet för alla.
5. **Historiken fyllde *Pågår*.** Ett ärende som inte är avgjort, eller
   vars utfall inte syns i poolen, har status `pågår`; ingressen säger då
   att utfallet är okänt, som i
   [planbeskedet för Må 2:210](../bevakning/ks/2022-03-08-planbesked-ma-2-210.md).
   Av 39 ärenden under *Pågår* har 22 ingen händelse i år, 17 ingen sedan
   2024 eller tidigare och ett ingen sedan 2014. De döljer de 17 som har
   rört sig i år.

Till det kommer att varje ärendes adress är ett ankare på den sida där det
står. Ändrar ärendet status flyttar det till en annan sida, och länken
någon skickat går till fel ställe.

## Läsbarhet och tillgänglighet

Uppmätt mot [WCAG 2.2](https://www.w3.org/TR/WCAG22/), nivå AA:

- **Textstorlek.** Brödtexten är webbläsarens 16 punkter. Ortsmärkena och
  årtalen på korten är 12 punkter, tidslinjens rubriker 14,4. Det är under
  vad många äldre läser utan att förstora.
- **Kontrast.** Färgerna klarar 4,5:1 för text: den dämpade grå
  `#5b6475` på vitt ger 6,0:1, accentfärgen på den ljusblå bakgrunden 6,2:1.
  Ingen ändring behövs där.
- **Fokus.** Länkar och knappar har bara webbläsarens tunna standardram,
  och ikonerna i tidslinjen får en ram i samma färg som ikonen. Det syns
  dåligt (2.4.7, 2.4.11).
- **Hoppa förbi menyn.** Det finns ingen länk till huvudinnehållet (2.4.1).
- **Träffytor.** Ikonerna i tidslinjen är 26 punkter och ligger tätt; det
  klarar minimikravet 24 (2.5.8) men är svårt att träffa med en darrig
  hand.
- **Form, inte bara färg.** Stegen skiljs med form och färg, som de ska
  (1.4.1). Men innebörden av en form står bara i teckenförklaringen ovanför
  tabellen, långt från ikonerna längre ner.
- **Ortsvalet** glöms när man byter sida och går inte att dela som länk.

Klarspråksråden från [Isof](https://www.isof.se/) passar läsarna: skriv datum som man säger dem, sätt
det viktigaste först och förklara fackord där de står.

## Vad som görs

Åtgärderna i den ordning de genomförs, en pull request i taget:

| # | Åtgärd | Löser | Issue |
| - | ------ | ----- | ----- |
| 1 | Större text, tydlig fokusmarkering, länk förbi menyn och större träffytor | Läsbarhet, tillgänglighet | [#16](https://github.com/moggleif/giffa/issues/16) |
| 2 | Datum i klartext med veckodag, och dagar kvar till ett tillfälle | Datum för maskiner | [#17](https://github.com/moggleif/giffa/issues/17) |
| 3 | Stegen och korten i klarspråk, med förklaringen vid ikonerna | Ord för handläggare | [#18](https://github.com/moggleif/giffa/issues/18) |
| 4 | Varje tillfälle att tycka till säger vad man gör och vem man vänder sig till, synligt | Påverkan gömd | [#19](https://github.com/moggleif/giffa/issues/19) |
| 5 | Varje ärende får en egen sida med en adress som inte ändras | Brutna länkar | [#20](https://github.com/moggleif/giffa/issues/20) |
| 6 | Startsidan visar bara det som går att påverka och det nya; *Pågår* och *Beslutat* får egna sidor | Allt på en sida | [#21](https://github.com/moggleif/giffa/issues/21) |
| 7 | *Pågår* skiljer ärenden som rört sig de senaste två åren från dem som stått still | Historiken fyllde Pågår | [#22](https://github.com/moggleif/giffa/issues/22) |
| 8 | På mobilen visas korten i stället för tidslinjen | Tidslinjen på mobil | [#23](https://github.com/moggleif/giffa/issues/23) |
| 9 | Ortsvalet följer med mellan sidorna och syns i adressen | Ortsvalet glöms | [#24](https://github.com/moggleif/giffa/issues/24) |

Det som inte tas med nu: en sökruta (webbläsarens egen sökning räcker när
varje sida är kortare), utskriftsformat, mörkt läge och vilka ledamöterna i
ett organ är och hur man når dem, som ingen av källorna i `KALLOR.md` ger.
De prövas igen när sidan har använts en tid.
