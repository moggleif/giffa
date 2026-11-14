# 0009 – Handlingslänkar i Actions och en schemalagd söndagsrunda

## Sammanhang

Projektägaren vill att protokoll och handlingar kommer in i ärendena utan
att någon behöver be om det, och att nya ärenden skapas varje vecka.
Skanningen och veckans kallelser (beslut 0003 och 0005) öppnar bara issues;
rundan skrivs av en agent när någon ber om det.

## Beslut

Två delar, båda på söndagen:

- **`handlingar.yml`** kör `python3 -m handlingslankar`, som lägger
  tjänsteskrivelsen ur samma sammanträdes handlingar intill protokollet
  (K26). Det är mekaniskt och går att pröva med tester, så det görs av ett
  skript. Arbetsflödet kör testerna och bygget själv, eftersom en PR som
  öppnas av arbetsflödet inte startar Kontroll, och lägger ändringen på
  grenen `automatik/handlingslankar`.
- **En schemalagd Claude-runda** startar senare samma morgon. Den bygger på
  grenen `automatik/handlingslankar` om den PR:en är öppen, gör en
  bevakningsrunda (R1, R2 och granskningen) från förra rundans slut, för in
  nya händelser och tillfällen att tycka till, skapar nya ärenden och
  öppnar en PR. Att skapa ärenden kräver bedömning, så det kan inte vara
  ett skript.

Ingen av dem mergar. Projektägaren godkänner PR:en.

## Konsekvenser

- Repot måste tillåta att Actions skapar pull requests (inställningen
  *Allow GitHub Actions to create and approve pull requests*).
- Mergas Claude-rundans PR följer handlingslänkarna med, och deras PR
  stängs som mergad.
- Den schemalagda rundan styrs av en uppgift i Claude, inte av en fil i
  repot; dess instruktion står i beslutet ovan och i rundans faser.
