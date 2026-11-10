---
name: fas-7-8-leverera
description: Fas 7–8 i Giffå. Använd när granskningen är klar, för att presentera arbetet, öppna pull request och driva den till grönt.
---

# Fas 7–8 – Leverera

## Fas 7 – Kontrollpunkt och pull request

1. Kontrollera att granskningens fynd finns och att inget blockerande är
   kvar.
2. Presentera det färdiga arbetet och **vänta på bekräftelse**.
3. Uppdatera grenen mot senaste `main` och kör all verifiering igen.
4. Öppna en PR med mallen: kort rubrik i imperativ (under 70 tecken), vad
   som ändrats, granskningens fynd och hur vart och ett hanterades, och
   `Closes #<nr>` när arbetet kommer från ett issue. För en
   bevakningsrunda: period, källor, nya ärenden, ärenden med nya händelser
   och det som inte gick att nå, och
   `Closes #<nr>` för månadens issue med etiketten `runda`.

## Fas 8 – CI och avslut

- Vänta tills alla kontroller är gröna. Faller något: hitta orsaken och
  rätta på grenen.
- Merge görs av en människa.
- Efter merge publicerar `pages.yml` sidan; kontrollera att körningen gick
  igenom.
