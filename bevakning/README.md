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

Filen heter `ÅÅÅÅ-MM-DD-kort-beskrivning.md` efter datumet på ärendets
första kända händelse när filen skapas. Filnamnet är också adressen till ärendets sida,
`arende/<filnamn>.html` ([beslut 0006](../beslut/0006-en-sida-per-arende.md)),
så en fil byter inte namn sedan den publicerats. Webbplatsen byggs ur filerna
([beslut 0002](../beslut/0002-sidan-byggs-ur-arendena-i-pages-flodet.md)),
och bygget stoppar när en fil inte följer formatet nedan.

## Formatet

```markdown
---
rubrik: Planprogram för Åsaberg
ort: Åsa
organ: Kommunstyrelsen
diarienummer: KS-2003-00165
status: pågår
---

En eller två meningar om vad ärendet gäller, ur källan.

## Händelser

- 2026-06-16 · samrad · Kommunstyrelsen godkände samrådshandlingarna. · [KS protokoll § 161](https://github.com/...#sida-21)
- 2026-06-02 · forslag · KSAU föreslog samråd. · [KSAU protokoll § 209](https://github.com/...#sida-14)

## Tycka till

- 2026-12-01 · samrad · Samrådet om planprogrammet pågår. · [Samrådet på kungsbacka.se](https://www.kungsbacka.se/...)

## I media och debatt

- 2026-06-20 · [Rubriken som den står](https://www.norrahalland.se/...) · Norra Halland
```

**Front matter**, en nyckel per rad:

| Nyckel              | Innehåll                                                      |
| ------------------- | ------------------------------------------------------------- |
| `rubrik`            | Ärendet som det heter i handlingarna                           |
| `ort`               | En eller flera orter ur `OMRADE.md`, åtskilda med komma         |
| `organ`             | Organet som driver ärendet                                     |
| `diarienummer`      | När det finns                                                  |
| `status`            | `pågår`, `beslutat`, `klart` eller `avbrutet` (se nedan)        |

**Status** styr var ärendet står på sidan:

- `pågår` – inte avgjort; sidan *Pågår*.
- `beslutat` – avgjort och att följa; sidan *Beslutat*.
- `klart` – genomfört, byggt, på plats; historiken.
- `avbrutet` – avbrutet eller upphävt utan nytt arbete; historiken.

**Händelserna** står nyast först, en per rad: datum, steg, en mening om
vad som hände och källan som länk, åtskilda med ` · `. Länka till handlingens sida på
[kommunhandlingars webbplats](https://moggleif.github.io/kommunhandlingar/)
med `#sida-N` när den finns där; i `.md` på GitHub fungerar ankaret inte. Stegen ger ikonen i
tabellen, och teckenförklaringen på sidan visar samma betydelser
(`BETYDER` i `webbplats/ikoner.py`, som ett test håller lika med tabellen):

| Steg         | Betyder                                         |
| ------------ | ----------------------------------------------- |
| `forslag`    | förslag, uppdrag eller initiativ                |
| `samrad`     | samråd eller remiss: öppet för synpunkter       |
| `granskning` | granskning av ett planförslag                   |
| `yttrande`   | en nämnd eller myndighet yttrar sig             |
| `beslut`     | beslut eller antagande                          |
| `bygge`      | byggstart eller genomförande                     |
| `klart`      | klart, på plats                                 |
| `avbrutet`   | avbrutet eller upphävt                          |
| `info`       | information, avstämning eller överprövning av en högre instans |

**Tycka till** är valfritt: kommande tillfällen att påverka, i samma
format som händelserna. Datumet är sista dagen för synpunkter eller
sammanträdets dag. Steget är ett av:

| Steg         | Betyder                                                        |
| ------------ | -------------------------------------------------------------- |
| `samrad`     | samråd; datumet är sista dagen för synpunkter                   |
| `granskning` | granskning; datumet är sista dagen för synpunkter               |
| `yttrande`   | en nämnd ska yttra sig; källan är kallelsen                     |
| `beslut`     | ärendet står i kallelsen till sammanträdet                      |
| `vantas`     | ett arbetsutskott har föreslagit beslutet men kallelsen har inte kommit; datumet är organets nästa sammanträde i kommunhandlingars [kalender](https://github.com/moggleif/kommunhandlingar/blob/main/kalender/kungsbacka.csv), som är källan, och sidan märker det preliminärt |

Det gäller alla sorters ärenden, också lokalbehov, handlingsplaner och
initiativ. Startsidan visar dem under *Tycka till nu* och döljer dem som
har passerat (K12). När tillfället har ägt rum flyttar rundan raden till
*Händelser*, med protokollet som källa; ett `vantas` som inte kom upp
flyttas till nästa sammanträde.

Andra avsnitt än *Händelser*, *Tycka till* och *I media och debatt*
stoppar bygget.

**I media och debatt** är valfritt: tidningsartiklar och diskussioner, en
per rad med datum, rubriken som länk och var den stod. Kungsbacka-Posten och
sociala medier tas bara med när en människa länkat dem i ett issue
([KALLOR.md](../KALLOR.md)).

## Rundorna

[`rundor.csv`](rundor.csv) har en rad per bevakningsrunda med periodens
första och sista dag (`fran`, `till`) och en `anteckning` som visas med
perioden, till exempel när perioden inte är fullständigt genomsökt. Händelserna inom den sista radens
period visas som *Nytt* på startsidan.
