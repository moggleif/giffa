# Krav

Vad bevakningen ska göra, som Given/When/Then. Hur kraven skrivs står i
`.claude/skills/fas-1-3-krav-och-design/SKILL.md`.

## K1 – Ett ärende per fil

**Givet** att något i en ort i `OMRADE.md` har tagits upp i en källa i
`KALLOR.md`,
**när** en bevakningsrunda för in det,
**så** finns det som en fil i `bevakning/<källa>/` enligt formatet i
`bevakning/README.md`, med en länk till källan för varje händelse.

## K2 – Händelser läggs till, inte nya filer

**Givet** att ett ärende redan finns i `bevakning/`,
**när** samma ärende syns igen i en källa,
**så** läggs en ny händelse överst i den befintliga filen, och `status`
uppdateras när händelsen ändrar den.

## K3 – Sidan publiceras från main

**Givet** en ändring som sammanfogats till `main`,
**när** arbetsflödet `pages.yml` har kört,
**så** visar GitHub Pages innehållet i `docs/` från den ändringen.
