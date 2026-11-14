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
  bevakningsrunda från förra rundans slut, för in
  nya händelser och tillfällen att tycka till, skapar nya ärenden och
  öppnar en PR. Att skapa ärenden kräver bedömning, så det kan inte vara
  ett skript.

Projektägarens beställning av söndagsrundan är dess fas 0: period, källor
och orter följer av `bevakning/rundor.csv`, `KALLOR.md` och `OMRADE.md`,
och rundan väntar inte på en ny bekräftelse. Kontrollpunkten i fas 7 står
kvar: ingen av dem mergar, och projektägaren godkänner PR:en.

## Konsekvenser

- Repot måste tillåta att Actions skapar pull requests (inställningen
  *Allow GitHub Actions to create and approve pull requests*).
- Mergas Claude-rundans PR följer handlingslänkarna med. Vid squash-merge
  blir handlingslänkarnas PR kvar öppen och stängs för hand, eller töms vid
  nästa söndags körning.
- Grenen `automatik/handlingslankar` ägs av arbetsflödet och skrivs om varje
  söndag; ändringar görs i en annan gren.
- En PR som öppnas av arbetsflödet startar inte Kontroll. Är Kontroll ett
  krav för att merga körs den genom att någon pushar till grenen eller
  startar arbetsflödet för hand.
- Den schemalagda rundan styrs av en uppgift i Claude, inte av en fil i
  repot; dess instruktion följer det här beslutet och rundans faser.
  Finns uppgiften inte görs rundan när någon ber om den, som förut.
