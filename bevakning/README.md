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

## Förslaget i korthet

- Omkring 160 bostäder i småhus. · [Planprogrammet s. 2](https://moggleif.github.io/kommunhandlingar/...#sida-20)

## Händelser

- 2026-06-16 · samrad · Kommunstyrelsen godkände samrådshandlingarna. · [KS protokoll § 161](https://github.com/...#sida-21) · Handlingar: [Tjänsteskrivelse](https://moggleif.github.io/kommunhandlingar/...#sida-124), [Programkartan (PDF)](https://kungsbacka.se/download/...pdf#page=171)
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
| `ort`               | En eller flera orter ur `OMRADE.md`, åtskilda med komma; föreningen följer av orten |
| `organ`             | Organet som driver ärendet                                     |
| `diarienummer`      | När det finns                                                  |
| `status`            | `pågår`, `beslutat`, `klart` eller `avbrutet` (se nedan)        |

**Fastighetsbeteckningar** skrivs som i källan, trakt och nummer:
*Ölmanäs 1:17*, *Frillesås-Rya 3:77*. I ingressen, händelserna och
tillfällena att tycka till gör sidan dem till länkar till kommunens karta,
med de undantag som står i K23.
Platserna i `platser.csv`, gatunamn och plannummer efter *detaljplan*
eller *plan* blir länkar på samma sätt (K24); skriv dem som i källan.

**Status** styr var ärendet står på sidan:

- `pågår` – inte avgjort; sidan *Pågår*, där det utan händelse på två år
  står sist (K19).
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

Stegen och texten ger också processtegen på planernas kort och sidor:
hur ett antagande, ett uppdrag och ett upphävande känns igen står i K33 i
[KRAV.md](../KRAV.md). Skriv därför ett antagande som *antog
detaljplanen* och andra beslut i en plan, som exploateringsavtal, utan
det ordet. Samråd och granskning hör till spåret *för alla*, de andra
stegen till *partierna* (K30); en `info` det senaste året utan förslag
eller tillfälle efter står under *På väg upp* (K32).

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

**Handlingar** är valfritt sist på en rad under *Händelser* eller *Tycka
till*: underlaget som steget bygger på, efter `Handlingar: ` som länkar
åtskilda med `, ` (K25). Länka till handlingens sida på kommunhandlingars
webbplats, och till kommunens PDF med `#page=N` och `(PDF)` i namnet när
sidan är en karta eller bild som inte blev text. Gick sammanträdets
handlingar inte att hämta länkas hela PDF:en utan `#page`, med punkten i
kallelsen i namnet: `Handlingar till sammanträdet, punkt N (PDF)`. Sidan
visar dem direkt under steget. Varje söndag lägger `handlingar.yml` till
ärendets handling på händelser som bara länkar ett protokoll (K26).

**Förslaget i korthet** är valfritt och står före *Händelser*: några
punkter om vad förslaget innebär, ur planprogrammet, planbeskrivningen
eller tjänsteskrivelsen, en per rad med källan som länk efter ` · `. Det
skrivs när ärendet har ett förslag med innehåll; ingressen räcker när den
redan säger vad det gäller.

Andra avsnitt än *Förslaget i korthet*, *Händelser*, *Tycka till* och
*I media och debatt* stoppar bygget.

**I media och debatt** är valfritt: tidningsartiklar och diskussioner, en
per rad med datum, rubriken som länk och var den stod. Kungsbacka-Posten och
sociala medier tas bara med när en människa länkat dem i ett issue
([KALLOR.md](../KALLOR.md)).

## Uppmärksammade ärenden

[`uppmarksammade.csv`](uppmarksammade.csv) är projektägarens lista över
ärenden som många följer och namnen de har i folkmun
([beslut 0010](../beslut/0010-uppmarksammade-och-sok.md), K27). En rad per
namn och ärende:

| Kolumn   | Innehåll                                                       |
| -------- | -------------------------------------------------------------- |
| `namn`   | Namnet folk använder, som *Restaurangstråket i Åsa*, eller ett ämne, som *Dagvatten och översvämningar* |
| `arende` | Ärendets filnamn utan `.md`                                     |
| `kalla`  | Var namnet kommer ifrån: en länk `[Rubrik](https://…)` till en artikel eller handling, eller en text som *projektägaren* eller *ärendets rubrik* |

Ett namn kan stå på flera rader, en per ärende, och ett ärende kan ha
flera namn. Namnen står i filens ordning under *Ärenden med mer uppmärksamhet* på
startsidan och först i listorna *Pågår*, *Beslutat* och *Historik* (K29);
flytta ett namns rader för att flytta namnet och dess ärenden. Namnet visas också, som en färgad
etikett, på
ärendets kort, egen sida och i tidslinjen, och går att söka på under
*Sök*. Ett ärende som inte finns stoppar bygget.

## Rundorna

[`rundor.csv`](rundor.csv) har en rad per bevakningsrunda med periodens
första och sista dag (`fran`, `till`) och en `anteckning` som visas med
perioden, till exempel när perioden inte är fullständigt genomsökt. Händelserna inom den sista radens
period visas som *Nytt* på startsidan.
