---
name: fas-1-3-krav-och-design
description: Fas 1–3 i Giffå. Använd efter bekräftad fas 0 för en ändring av repot, för att skriva krav som Given/When/Then, fatta designbeslut och bestämma hur ändringen ska verifieras.
---

# Fas 1–3 – Krav, design och valideringsstrategi

Skapa en gren innan något skrivs. Committa efter varje fas.

## Fas 1 – Krav

- Skriv kraven i `KRAV.md` som Given/When/Then: önskat tillstånd, inte en
  beskrivning av ändringen.
- Konkreta, testbara och begripliga för någon som inte kan koden.

## Fas 2 – Design och dokumentation

- **Ett beslut som är svårt att ändra får ett beslutsdokument** i
  `beslut/`, enligt `beslut/README.md`.
- Hitta varje fil som beskriver den del som ändras – `README.md`,
  `KRAV.md`, `bevakning/README.md`, `KALLOR.md` – och uppdatera dem nu,
  inte i efterhand.

## Fas 3 – Valideringsstrategi

- Bestäm hur varje krav ska verifieras. Automatiskt i första hand, mot
  sparade sidor i `tests/fixtures/` utan nät.
- Går det inte att automatisera: skriv ner det manuella steget.
