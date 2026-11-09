# Bevakning

Ett ärende per Markdown-fil, i katalogen för den källa där det först syntes:

```
bevakning/ks/              Kommunstyrelsen
bevakning/ksau/            Kommunstyrelsens arbetsutskott
bevakning/namnder/         Nämnderna
bevakning/bygglov/         Bygglov
bevakning/detaljplaner/    Detaljplaner
bevakning/kungsbacka-se/   Övrigt från kungsbacka.se
```

Filen heter `ÅÅÅÅ-MM-DD-kort-beskrivning.md` efter dagen ärendet först
syntes, och börjar med:

```markdown
---
rubrik: Ny förskola i Frillesås
ort: Frillesås
organ: Förskole- och grundskolenämnden
diarienummer: FGN 2026/0123
forst_sedd: 2026-11-09
status: pågår
kallor:
  - https://www.kungsbacka.se/...
---
```

Under front matter följer händelserna i ärendet, nyast först, var och en med
datum och länk till källan.
