# 0018 – Sök i sajtraden, i allt på ärendena

## Sammanhang

Sidan *Sök* ([beslut 0010](0010-uppmarksammade-och-sok.md)) sökte bara på
rubriken, namnen i folkmun, orten och organet, och låg som en post bland
de andra i menyn. Projektägaren vill ha en sökning som syns överst och
hittar ett ärende också på en fastighetsbeteckning, ett diarienummer
eller något som bara står i texten, och som tar med kommunstyrelsens
kommande sammanträde.

## Beslut

- **En knapp *Sök* i sajtraden**, med förstoringsglas och ordet, före
  knappen för mörkt tema. Den fäller ut ett stort fält under raden, och
  träffarna kommer medan man skriver. Ordet står med, eftersom läsarna
  också är äldre.
- **Bara på Giffå än så länge.** Knappen läggs till av Giffås eget skript
  (`docs/sokruta.js`), inte av den gemensamma `sajter.js`. De andra
  sajterna har inget eget att söka i ännu; en knapp där som bara hittade
  Giffås ärenden vore missvisande. Datapoolen är för stor för att söka i
  webbläsaren, så den tas upp för sig.
- **Ett sökindex som byggs med sidan**, `sok.json`: varje ärendes rubrik,
  orter, organ, diarienummer, namn och text, punkterna på KS-mötet och
  föreningarnas orter. Skriptet hämtar det först när fältet fälls ut.
  Inget skickas till någon annan värd.
- **Träffar i rubrik, orter, organ, diarienummer och namn först**; de som
  bara står i texten märks *nämns i texten*. Varje ord ska finnas; ingen
  stavningstolerans.
- **Ortvalet gäller ärendena**, men inte punkterna på KS-mötet, som
  visas utan urval också på sin sida (K34).
- **Sidan *Sök* står kvar** med alla ärenden, för den som kommer dit
  från menyn eller utan skript, och fältet är utfällt där. Dess egen ruta
  och `docs/sok.js` tas bort.

Det här ersätter sökrutan i beslut 0010; resten av det beslutet gäller.

## Konsekvenser

- `sok.json` växer med ärendena; med omkring 300 ärenden är det några
  hundra kilobyte, och det hämtas bara av den som söker.
- Ett ord med fel stavning eller utan å, ä och ö hittar inget.
- Ska de andra sajterna få knappen behöver de något eget att söka i, och
  knappen flyttar då till `sajter.js`.
