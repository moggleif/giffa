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
organ, diarienummer, senaste steget och en länk *Läs mer* till ärendets
egen sida (K18). Raden i tabellen länkar också dit. Knappar ovanför väljer
förening och ort enligt K22; utan skriptet står alla.

## K5 – Kort startsida, listor på egna sidor

**Givet** ärenden med `status` `pågår` eller `beslutat`,
**när** sidan byggs,
**så** står de på sidorna *Pågår* respektive *Beslutat* i menyn, med
tidslinjen och korten. Startsidan visar bara *Tycka till nu* (K12), det
nya (K6) och hur många ärenden som står på *Pågår*, *Beslutat* och
*Historik*, med länkar.

## K6 – Nytt sedan förra rundan

**Givet** att den sista raden i `bevakning/rundor.csv` anger förra rundans
period,
**när** sidan byggs,
**så** visar startsidan överst perioden, radens anteckning och ett kort
för varje ärende med en händelse i perioden. Kortet visar de nya händelserna med källor bakom en hopfälld
del och länkar till ärendets sida (K18). Har inget ärende en ny händelse står
det, med perioden.

## K7 – Historik

**Givet** ärenden med `status` `klart` eller `avbrutet`,
**när** sidan byggs,
**så** står de på historiksidan och inte på *Pågår* eller *Beslutat*.

## K8 – Vad som bevakas

**Givet** `OMRADE.md`, `platser.csv` och `KALLOR.md`,
**när** sidan byggs,
**så** visar sidan *Vad vi bevakar* föreningarna med sina orter, platserna
och källorna ur just de filerna, och länkar till dem för reglerna.

## K9 – Länkar mellan sidan och repot

**Givet** en sida på webbplatsen,
**när** den visas,
**så** länkar sidfoten till repot och varje ärendes egen sida till ärendets fil, och
`README.md` länkar till webbplatsen.

## K10 – Hellre stanna än visa fel

**Givet** ett ärende som inte följer formatet i `bevakning/README.md` –
okänd status, ort, steg, nyckel eller okänt avsnitt, ett datum som inte går att läsa,
en källa utan `https`-länk, händelser som inte står nyast först eller samma
filnamn i två kataloger –
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
står i teckenförklaringen överst på varje lista. Ikonens text
börjar med stegets namn och datum, kortet säger *Senaste steget:* med
namn och datum, och årtalen på kortet står som *Pågått 2014–2026*.

## K17 – Så gör du

**Givet** ett kommande tillfälle att tycka till enligt K12,
**när** sidan byggs,
**så** har varje tillfälle på ärendets kort och sida en rad *Så gör du:*
för just det steget med en länk till källan. Under *Tycka till nu* (K31)
står förklaringen *Så kan du påverka, steg för steg* öppen en gång under
listan i stället för vid varje tillfälle.

## K18 – En egen sida per ärende

**Givet** ett ärende i `bevakning/`,
**när** sidan byggs,
**så** har det en egen sida `arende/<filnamn>.html` med ort, organ,
diarienummer, status, ingress, tillfällena att tycka till, alla händelser
med källor och handlingar (K25), länkarna under *I media och debatt*
och en länk till filen i repot. Kort, tabellrader, *Tycka till nu* och
*Nytt sedan förra rundan* länkar dit, och adressen är densamma vilken status ärendet än har.

## K19 – Det som rör sig först

**Givet** ärenden med `status` `pågår`,
**när** sidan *Pågår* byggs,
**så** står, efter de uppmärksammade (K29), först de som har en händelse de senaste två åren (730 dagar)
räknat från byggdagen, och sedan, under en egen rubrik med datumet, de som
inte har det, med en mening om att det som inte syns i källorna inte
betyder att inget har hänt. Kortet visar när det senaste steget togs (K16).
Ärendefilernas status ändras inte.

## K20 – Korten på mobilen

**Givet** en lista med ärenden,
**när** den visas på en skärm högst 640 punkter bred (40 rem à 16
punkter i mediefrågan),
**så** visas korten och teckenförklaringen men inte tidslinjen; korten har
samma ärenden och länkar till ärendenas sidor. På en bredare skärm visas
tidslinjen också.

## K21 – Valet följer med

**Givet** att en förening eller en ort har valts med knapparna på en lista
eller startsidan,
**när** sidan visas med skriptet,
**så** står valet i adressen (`?forening=Förening Åsa`, `?ort=Åsa` eller
båda),
bakåtknappen återställer förra valet och en länk med valet visar samma
urval. Sidans länkar till andra sidor på webbplatsen tar med valet, också
från sidor utan knappar,
så att valet följer med tills läsaren väljer om. Utan skriptet står allt.

## K22 – Fyra föreningar, allt utan val

**Givet** föreningarna och deras orter i `OMRADE.md`, där varje ort står
under en enda förening,
**när** en lista eller startsidan visas,
**så** syns alla ärenden tills läsaren väljer. Knapparna visar *Alla* och
föreningarna i filens ordning, och under dem alla orter i en rad i
bokstavsordning, så att en ort går att välja direkt. En vald förening visar
ärendena i dess orter och bara dess ortknappar; en vald ort visar bara den
ortens ärenden, och väljs en förening efteråt står orten kvar om den hör
dit. En tryckt knapp som trycks igen släpper sitt val, *Alla* släpper
båda. Blir en lista tom för valet står det så. En ort under två
föreningar, eller en förening utan orter, stoppar bygget.

## K23 – Fastigheten på kartan

**Givet** en fastighetsbeteckning som *Ölmanäs 1:17* eller
*Frillesås-Rya 3:77* i ett ärendes ingress, händelser eller tillfällen
att tycka till,
**när** sidan byggs,
**så** är beteckningen en länk till Kungsbackas karta som visar just den
fastigheten. Kartan hämtas inte; bara länken byggs. Ett ord med versal
närmast framför hör till trakten, som i *Ölmevalla Hallen 1:17* och
*Nedre Ögärdet 2:13*, utom när det inleder meningen (*På Särö 1:493*).
Ett bolagsnamn som *Castellum Varla 3:34 AB* länkas inte. I en uppräkning eller
ett intervall som *Åsa 5:153 och 5:89* eller *Bäcken 1:31–1:34* får varje
nummer en egen länk med trakten från den första beteckningen.

## K24 – Platser, gator och detaljplaner på kartan

**Givet** en plats ur `platser.csv`, ett gatunamn eller ett plannummer
efter ordet *detaljplan* eller *plan* i ett ärendes ingress, händelser
eller tillfällen att tycka till,
**när** sidan byggs,
**så** är namnet en länk till kartans sökning på det, som för
fastigheterna i K23. En gata länkas utan husnummer. Platser av typen
förening, hemtjänst, detaljplan, planprogram, planbesked, område och
vatten länkas inte, eftersom de inte är en plats som säkert går att söka
fram. Ett förled som *Gamla* i *Gamla Särövägen* hör till gatan. Länkarna
till kartan öppnas i en ny flik, också i rubrikerna.

## K25 – Handlingarna intill steget

**Givet** ett steg i ett ärende vars underlag finns bland handlingarna,
som tjänsteskrivelse, planbeskrivning, karta eller utredning,
**när** ärendets sida byggs,
**så** står länkar direkt till handlingarna under steget, på ärendets
sida som under *Tycka till nu* och *Nytt sedan förra rundan*, så att man inte
behöver leta i protokollet eller kallelsen. En länk går till sidan i
kommunhandlingars text, eller till kommunens PDF på rätt sida när handlingen
är en karta eller bild som inte blir text. Har ärendet ett förslag med
innehåll, som ett planprogram eller en planbeskrivning, står *Förslaget i
korthet* överst: några punkter om vad förslaget innebär, var och en med en
länk till sidan den bygger på.

## K26 – Handlingarna intill protokollet varje söndag

**Givet** händelser i `bevakning/` som bara länkar ett protokoll, och
kommunhandlingars handlingar och kallelser till samma sammanträde,
**när** arbetsflödet `handlingar.yml` körs på söndagen eller för hand,
**så** läggs ärendets handling intill protokollet och arbetsflödet öppnar
en PR. En sida hör till ärendet när paragrafens diarienummer står i sidans
huvud, eller, när huvudet saknar diarienummer, ärendets hela rubrik.
Tjänsteskrivelsen – en sida med rubriken TJÄNSTESKRIVELSE överst – länkas
som *Tjänsteskrivelse*; finns ingen länkas ärendets första sida som
*Handlingarna i ärendet*. Gick handlingarna inte att hämta länkas
sammanträdets PDF med punkten i kallelsen. Protokollet står kvar. En
händelse som redan har handlingar, eller vars datum inte är sammanträdets,
lämnas som den är. Förteckningar och förslagslistor över många ärenden
länkas inte, och ett allmänt ärende som information eller anmälan av beslut
länkas bara till en tjänsteskrivelse. Hittas inget ändras inget och ingen PR
öppnas.

## K27 – Uppmärksammat, med namnen folk använder

**Givet** att projektägaren skrivit ett namn – det ärendet kallas i
folkmun, eller ett gemensamt ämne som *Dagvatten och översvämningar* – och
ett eller flera ärenden i `bevakning/uppmarksammade.csv`, med en källa till
namnet,
**när** sidan byggs,
**så** står namnen under *Ärenden med mer uppmärksamhet* på startsidan, i den ordning de
står i filen, med sina ärenden under och källan till namnet intill. Namnet
står också under rubriken som en färgad etikett: på ärendets kort och egna
sida efter orden *Uppmärksammat som*, och i tidslinjen med samma ord bara
för skärmläsare, så att den som känner ärendet under ett annat
namn känner igen det. Ortsvalet gäller rutan som allt annat, för namnen
och för varje ärende under dem. Ett ärende som inte finns, ett tomt fält,
samma namn och ärende två gånger eller en källa som är en länk men inte en
https-länk stoppar bygget.

## K28 – Sök på rubrik och namn

**Givet** sidan *Sök*,
**när** man skriver ett eller flera ord i sökrutan,
**så** syns bara de ärenden där varje ord finns i rubriken, i ett namn
ur `bevakning/uppmarksammade.csv`, i orterna eller i organet, utan hänsyn
till stora och små bokstäver. Utan ord syns alla ärenden, och utan skript
syns hela listan så att webbläsarens egen sökning fungerar. Finns ingen
träff står det.

## K29 – Uppmärksammat först i listorna

**Givet** ärenden i `bevakning/uppmarksammade.csv` (K27),
**när** listorna *Pågår*, *Beslutat* och *Historik* byggs,
**så** står de uppmärksammade ärenden som hör till listan först, under
rubriken *Ärenden med mer uppmärksamhet* och i namnens ordning i filen – först namnet
som står överst, med dess ärenden i radernas ordning – och
resten följer under som förut: på *Pågår* med uppdelningen i det som rört
sig och det som stått still (K19), på de andra under *Övriga ärenden*.
Namnen står som färgade etiketter i tidslinjen och på korten. Har listan
inget uppmärksammat ärende ser den ut som förut.

## K30 – Två spår, ett tecken och en färg var

**Givet** ett steg eller ett tillfälle att tycka till,
**när** sidan byggs,
**så** hör det till ett av två spår: *tycka till för alla* (samråd och
granskning) eller *diskutera i partiet* (allt annat: information, förslag,
yttrande och beslut, där partierna kan ta upp ärendet före
sammanträdet). Varje spår har ett eget tecken – en pratbubbla för alla,
två personer för partierna – och en egen färg, och samma tecken och färg
står överallt: i tidslinjen, på korten, under *Tycka till nu*, under
*På väg upp* och i processtegen. Tecknet har spårets namn som text för
skärmläsare. Etiketterna för uppmärksammade ärenden har en tredje färg.

## K31 – Tycka till nu som en kalender

**Givet** de kommande tillfällena att tycka till (K12),
**när** startsidan byggs,
**så** står de under *Tycka till nu* dag för dag, med dagen som rubrik med
veckodag och hur många dagar det är kvar, och under varje dag en rad per
ärende med spårets tecken (K30), ärendet, orten, vad som ska hända,
källan och handlingarna (K25). Inledningen förklarar de två tecknen. En
dag utan ärenden för det valda urvalet döljs.

## K32 – På väg upp

**Givet** pågående ärenden vars senaste händelse är en *information* och
som inte har något kommande tillfälle att tycka till,
**när** startsidan byggs,
**så** står de ärenden vars information är högst ett år gammal räknat från
byggdagen under *På väg upp*, efter *Tycka till nu*, med det nyaste
först: partiernas tecken (K30), ärendet, orten, datumet och källan. Listan
säger bara att ett organ har informerats och inget om när ett beslut
kommer. Finns inget står det.

## K33 – Processtegen

**Givet** ett pågående ärende,
**när** dess kort och egna sida byggs,
**så** visar *Var ärendet står* stegen för ärendets slag i ordning – för
en detaljplan *Uppdrag, Samråd, Granskning, Antagande*, för ett
planprogram *Uppdrag, Samråd, Godkännande*, för andra ärenden
*Information, Förslag, Beslut* – med spårets tecken (K30) och för varje
steg om det är gjort, är där ärendet står nu eller kommer. Ett gjort
steg och steget nu har datumet för den senaste händelsen i steget, steget
nu och ett kommande steg datumet för sitt kommande tillfälle när det
finns, och ett kommande steg utan tillfälle står som *datum inte känt
än*. Slaget avgörs av hur rubriken börjar (*Detaljplan*, *Planprogram*).
Ett samråd eller en granskning räknas när händelsen har det steget; ett
antagande eller godkännande bara när ett beslut säger att planen antogs
(*antog*, *antagit*) eller att planprogrammet godkändes. För planerna
står att stegen följer plan- och bygglagens standardförfarande och att
ett begränsat förfarande inte har någon granskning, med länk till lagen.
Steget nu är det med den senaste händelsen, så att en plan som börjat om
efter ett upphävt antagande står på sitt nya steg. Avgjorda ärenden har
ingen stege.
