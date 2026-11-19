# 0018 – Sök i sajtraden, på alla projektets sajter

## Sammanhang

Sidan *Sök* ([beslut 0010](0010-uppmarksammade-och-sok.md)) sökte bara på
rubriken, namnen i folkmun, orten och organet, och låg som en post bland
de andra i menyn. Projektägaren vill ha en sökning som syns överst på alla
projektets sajter och hittar allt: ett ärende på en fastighetsbeteckning,
ett diarienummer eller något som bara står i texten, kommunstyrelsens
kommande sammanträde, protokollen i datapoolerna och sidorna i
*Kungsbacka i siffror*. Sajterna är statiska och ligger på samma värd.

## Beslut

- **En knapp *Sök* i den gemensamma sajtraden**, med förstoringsglas och
  ordet, före knappen för mörkt tema. Den fäller ut ett stort fält under
  raden, och träffarna kommer medan man skriver. Ordet står med, eftersom
  läsarna också är äldre.
- **Sökningen bor hos Giffå, som menyn** ([beslut 0013](0013-gemensam-meny-fran-giffa.md)):
  `sajter.js` laddar `sok.css`, `sokning.js` (sökningen utan sidan) och
  `sokruta.js` (knappen, fältet och träffarna) från samma ställe. Ingen
  sajt behöver ändra sina sidor för att få knappen.
- **Varje sajt skriver sitt eget sökindex**, `sok.json` bredvid sin start,
  där sajtradens länk pekar. Formatet är gemensamt:

  ```json
  {"grupper": [{"rubrik": "Ärenden", "poster": [
    {"rubrik": "…", "adress": "arende/x.html", "om": ["Åsa", "pågår"],
     "traff": "det som söks först, i små bokstäver",
     "text": "det som söks sedan, i små bokstäver"}]}]}
  ```

  `adress` räknas från indexets plats. `text` kan saknas. Giffås poster
  har också `orter` och `kallas`, och Giffås index `foreningar`, för
  urvalet (K22).
- **En sökning söker i alla sajterna** och visar dem en i taget, den
  visade först. Indexen hämtas först när fältet fälls ut, alla på en gång.
  Inget skickas till någon annan värd.
- **Träff i det som söks först står först**; de som bara står i texten
  märks *nämns i texten*. Varje ord ska finnas; ingen stavningstolerans.
- **Högst tjugo träffar per grupp står direkt**, resten bakom en knapp, så
  att ett vanligt ord inte ritar tusentals rader.
- **Ortvalet gäller Giffås ärenden** på Giffå, men inte punkterna på
  KS-mötet, som visas utan urval också på sin sida (K34).
- **Sidan *Sök* står kvar** med alla ärenden, för den som kommer dit från
  menyn eller utan skript, och fältet är utfällt där. Dess egen ruta och
  den gamla `docs/sok.js` tas bort.

Det här ersätter sökrutan i beslut 0010; resten av det beslutet gäller.

## Konsekvenser

- Varje sajt bygger sitt index: Giffå i `webbplats/sokindex.py`,
  datapoolerna (kungsbackakommun och regionhalland, samma kod) ur
  protokollens paragrafer, och politik ur sina sidor. En sajt utan index
  står med raden *Gick inte att söka i …* tills det finns.
- Datapoolens index är stort, några megabyte för en kommun, men hämtas
  bara av den som söker och komprimeras av GitHub Pages.
- Ett ord med fel stavning eller utan å, ä och ö hittar inget.
- Ändras formatet måste alla sajternas index följa med.
