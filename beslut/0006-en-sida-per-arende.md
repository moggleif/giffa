# 0006 – En egen sida per ärende, med filnamnet som adress

## Sammanhang

Ett ärende hade bara ett kort på startsidan eller historiken, och adressen
var ett ankare på den sidan. När status ändrades flyttade kortet, och en
länk som någon skickat gick fel. Det gick inte heller att skicka en länk
till bara ett ärende (se `kunskap/ux-analys.md`).

## Beslut

Varje ärende får en egen sida, `arende/<filnamn>.html`, där filnamnet är
ärendefilens namn utan `.md`. Filnamnet bygger på datumet för den första
händelsen och ändras inte när händelser läggs till. Korten på listorna
visar en sammanfattning och länkar till sidan; alla händelser står bara
där.

## Konsekvenser

- En ärendefil byter inte namn sedan den publicerats (`bevakning/README.md`).
- Listorna blir kortare, eftersom händelserna inte längre står på dem.
- Bygget skriver en sida per ärende, och sidor i en underkatalog hämtar
  stilen och menyn med `../`.
