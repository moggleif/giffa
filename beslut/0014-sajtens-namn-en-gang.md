# 0014 – Sajtens namn står en gång, i sajtraden

## Sammanhang

Med den gemensamma menyn ([beslut 0013](0013-gemensam-meny-fran-giffa.md))
stod sajtens namn på varje sida två gånger – markerat i sajtraden och som
länk först i sajtens meny – och på startsidorna en tredje gång som rubrik.
På Kungsbacka kommun stod det fyra gånger. På mobilen tog sajtraden två
till tre rader innan något innehåll syntes. Projektägaren bad 2026-11-16
om ett helhetsgrepp och godkände förslaget med ett menyträd för alla fyra
sajterna.

## Beslut

- **Sajtraden är sajtens namn.** När skriptet kört döljs `.sajtnamn` i
  sajtens meny. Utan skriptet finns ingen sajtrad, och namnet står kvar
  först i menyn.
- **På smal skärm är sajtraden en rad**: den visade sajten och knappen
  *Meny*. Knappen flyttas därför in i sajtraden. Den utfällda menyn har de
  andra sajterna sist, under *Projektets andra sajter*. På bred skärm står
  sajtraden hel, som förut.
- **En sidas rubrik är aldrig sajtens namn.** Startsidan får en rubrik som
  säger vad sajten visar; fliken heter rubriken och sedan sajten.
- Formen i beslut 0013 gäller i övrigt oförändrad, och de andra sajterna
  behöver inte ändra sin meny för det här.

## Konsekvenser

- En besökare på mobilen ser sajten, knappen och sidans rubrik direkt.
- De andra sajterna är ett klick bort på mobilen i stället för synliga.
  Det är priset för en rad; på datorn syns de som förut.
- politik har en fryst kopia av `sajter.*` i sina tester och behöver
  kopiera in de nya filerna.
