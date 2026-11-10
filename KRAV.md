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
**så** visar GitHub Pages sidan byggd ur den ändringen. Sidan byggs också
om varje morgon, så att passerade tillfällen att tycka till försvinner
(K12).

## K4 – Ärendena som tabell och kort

**Givet** ärenden i `bevakning/`,
**när** sidan byggs,
**så** står de i en tabell med en rad per ärende och en kolumn per år, där
varje händelse är en ikon som länkar till källan och där stegen skiljs åt
med form, inte bara färg. Under tabellen har varje ärende ett kort med ort,
organ, diarienummer, senaste steget och, under *Läs mer*, alla händelser
med källor och länkarna under *I media och debatt*. Raden i tabellen länkar
till kortet. Knappar ovanför visar bara ärendena i en vald ort; utan
skriptet står alla.

## K5 – Startsidan: pågår och beslutat

**Givet** ärenden med `status` `pågår` eller `beslutat`,
**när** sidan byggs,
**så** visar startsidan dem under *Pågår* respektive *Beslutat*.

## K6 – Nytt sedan förra rundan

**Givet** att den sista raden i `bevakning/rundor.csv` anger förra rundans
period,
**när** sidan byggs,
**så** visar startsidan överst perioden, radens anteckning och ett kort
för varje ärende med en händelse i perioden. Kortet visar de nya händelserna med källor bakom en hopfälld
del och länkar till ärendets kort. Har inget ärende en ny händelse står
det, med perioden.

## K7 – Historik

**Givet** ärenden med `status` `klart` eller `avbrutet`,
**när** sidan byggs,
**så** står de på historiksidan och inte på startsidan.

## K8 – Vad som bevakas

**Givet** `OMRADE.md`, `platser.csv` och `KALLOR.md`,
**när** sidan byggs,
**så** visar sidan *Vad vi bevakar* orterna, platserna och källorna ur
just de filerna, och länkar till dem för reglerna.

## K9 – Länkar mellan sidan och repot

**Givet** en sida på webbplatsen,
**när** den visas,
**så** länkar sidfoten till repot och varje ärendekort till ärendets fil, och
`README.md` länkar till webbplatsen.

## K10 – Hellre stanna än visa fel

**Givet** ett ärende som inte följer formatet i `bevakning/README.md` –
okänd status, ort, steg, nyckel eller okänt avsnitt, ett datum som inte går att läsa,
en källa utan `https`-länk eller händelser som inte står nyast först –
**när** sidan byggs,
**så** avbryts bygget med filens namn och felet, och inget publiceras.

## K11 – Månadens skanning

**Givet** orterna i `OMRADE.md`, platserna i `platser.csv`, diarienumren i
de ärenden som inte är klara eller avbrutna och förra rundan i
`bevakning/rundor.csv`,
**när** arbetsflödet `skanning.yml` körs den första i månaden eller för
hand,
**så** öppnas ett issue med etiketten `runda` som för varje dokument i
kommunhandlingar med sammanträdesdatum från början av förra rundans period
– eftersom protokoll publiceras veckor efter sammanträdet – listar datum,
organ, de sidor som nämner en term, en länk till den första och termerna.
Protokoll och kallelser står först och handlingarna hopfällda sist i
varje avsnitt.
Kommande sammanträden står för sig, ingen text ur handlingarna återges,
dokument utan text listas som inte sökta och källorna i `KALLOR.md` som
inte söktes automatiskt skrivs ut. Ett mellanslag i en term matchar också
radbrott, och ett diarienummer räknas också med mellanslag efter
prefixet. Blir rapporten för lång för ett issue kortas den, och hela finns
som artefakt. Finns dagens issue redan öppnas inget nytt.

## K12 – Tycka till i rätt tid

**Givet** ärenden med avsnittet *Tycka till*, där varje rad är ett
kommande samråd, en granskning, ett yttrande, ett beslut eller ett väntat
beslut med datum och källa,
**när** sidan byggs,
**så** listar startsidan under *Tycka till nu*, före det nya, alla
tillfällen från och med byggdagen med det närmaste först och en länk till
ärendet. Ärendets kort och rad i tabellen markerar dess kommande
tillfällen, en kort förklaring säger vad man kan göra i varje steg, med
källa, ett väntat beslut märks preliminärt och det som har passerat visas
inte. Ett annat steg i avsnittet
stoppar bygget.

## K13 – Veckans kallelser

**Givet** kommunhandlingars kallelser och handlingar till sammanträden
efter dagen, och samma termer som i K11,
**när** arbetsflödet `kallelser.yml` körs på måndagen eller för hand,
**så** öppnas ett issue med etiketten `kallelser` som listar datum, organ,
sidor och termer per dokument som i månadens skanning, med handlingarna
hopfällda och dokument utan text listade som inte sökta. Hela rapporten
sparas som artefakt. Finns inga
träffar öppnas inget issue, och finns veckans issue redan öppnas inget
nytt.

## K14 – Läsbar för alla

**Givet** en sida på webbplatsen,
**när** den visas,
**så** är brödtexten minst 18 punkter och ingen text mindre än 15, den
första länken hoppar förbi menyn till innehållet, allt som går att välja
får en tydlig fokusram, knappar och stegikoner har träffytor på minst 32
punkter och löptexten står i en spalt på högst cirka 70 tecken.

## K15 – Datum som man säger dem

**Givet** ett datum på sidan,
**när** sidan byggs,
**så** står det som man säger det, till exempel *24 november 2026*, med
ISO-datumet i `datetime`. Ett tillfälle att tycka till visar också
veckodagen och hur många dagar det är kvar räknat från byggdagen i svensk
tid, till exempel *tisdag 24 november 2026, om 14 dagar*. Sidfoten säger
när sidan byggdes på samma sätt.

## K16 – Stegen i klarspråk

**Givet** stegen i `bevakning/README.md`,
**när** sidan byggs,
**så** har varje steg ett kort namn och betydelsen ur tabellen där, som
står i teckenförklaringen direkt ovanför varje tidslinje. Ikonens text
börjar med stegets namn och datum, kortet säger *Senaste steget:* med
namn och datum, och årtalen på kortet står som *Pågått 2014–2026*.
