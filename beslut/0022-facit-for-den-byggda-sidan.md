# 0022 – Facit för den byggda sidan, med fryst klocka

## Sammanhang

Testerna av `webbplats/` letar efter delsträngar i HTML:en, och testet av
bygget ser bara att filerna finns. En refaktorisering som flyttar eller
tappar markup syns därför inte säkert. Bygget läste dessutom klockan
själv, så samma rot gav olika sidor från dag till dag. Politik har redan
ett facit för sina sidor.

## Beslut

Varje sida och `sok.json` jämförs med ett incheckat facit i
`tests/facit/` (K40). Facit byggs ur en egen fryst rot,
`tests/fixtures/sajt/`, med ärenden som täcker sidans grenar: planernas
steg, laga kraft, överklagande och upphävande, planprogram, alla
tillfällen att tycka till, handlingar, förslaget i korthet, media,
uppmärksammade namn, flera orter, alla statusar och ett stilla ärende.
`tests/fixtures/rot/` lämnas som den är, eftersom skanningens tester
räknar dess orter och diarienummer.

`bygg()` delas: `sidor()` bygger sidorna som text ur roten, poolen och en
byggtid som argument, och `bygg()` läser klockan, kopierar `docs/` och
skriver filerna. Att lägga byggtiden som ett femte argument till `bygg()`
hade gått över gränsen för parametrar.

## Konsekvenser

- En avsedd ändring av sidan kräver att facit skrivs om med
  `python3 -m tests.test_facit --skriv-om`, och diffen visar i PR:en vad
  ändringen gör med sidan.
- KS-mötet byggs med kungsbackakommuns kod, som Kontroll hämtar från
  `main` där ([beslut 0012](0012-ks-motet-ur-datapoolens-kod.md)). Ändrar
  den koden vad sidan visar faller facit för `ks-motet.html` i nästa PR
  här, och facit skrivs om då.
- Rundorna ändrar bara `bevakning/` och rör inte facit.
