# 0011 – Två spår för att påverka, processtegen och kalendern

## Sammanhang

UX-analysen 2026-11-14 ([kunskap/ux-analys-2026-11-14.md](../kunskap/ux-analys-2026-11-14.md))
visade att bara de ärenden som har ett datum säger något om påverkan, att
påverkan visas som text och inte som en bild, och att den bruna färgen
delades av samråd, yttranden och uppmärksammade ärenden. Projektägaren lade
till att man också kan tycka till inom politiken: partierna kan ta upp ett
ärende redan när ett organ har informerats, innan det finns ett förslag.
Projektägaren valde förslag 1–3 och 12 ur analysen.

## Beslut

- **Två spår, inte ett.** Samråd och granskning är *tycka till för alla*;
  information, förslag, yttrande och beslut är *diskutera i partiet*.
  Spåret följer av steget i ärendets fil, så ingen ny uppgift behövs i
  formatet (`webbplats/spar.py`). Varje spår har ett tecken och en färg som
  används överallt; uppmärksammat får en tredje färg.
- **Processtegen läses ur det som redan finns** – händelsernas steg och
  text, statusen och tillfällena att tycka till – i stället för ett nytt
  fält för förfarandet i front matter. Slaget avgörs av hur rubriken börjar.
  Ett uppdrag och ett antagande känns igen på orden i händelsen eller
  tillfället, eftersom planerna också har andra beslut, som
  exploateringsavtal och principavtal. Steget nu är det med den senaste
  händelsen, och en information om att antagandet upphävts nollställer
  stegen. Stegen för de tre slagen står som konstanter i
  `webbplats/stege.py`; en datafil motiveras när ett fjärde slag behövs.
- **Hellre märka än gissa.** Kommande steg utan tillfälle står som *datum
  inte känt än*, och planernas stege säger att den följer
  standardförfarandet och att ett begränsat förfarande saknar granskning,
  med länk till lagen. *På väg upp* säger bara att ett organ har
  informerats.
- **Kalendern behåller handlingarna.** Analysen föreslog att flytta dem
  till ärendets sida, men K25 och projektägarens tidigare önskan är att
  handlingarna står intill varje steg. *Så gör du* står i stället en gång
  under listan på startsidan och kvar vid varje tillfälle på kortet och
  ärendets sida.

## Konsekvenser

- En plan vars antagande skrivits utan att säga att planen antas eller
  antogs visas som om antagandet kommer. `bevakning/README.md` säger hur antagandet ska
  skrivas.
- En plan med begränsat förfarande visar granskningen som kommande tills
  den antas; noten under stegen säger varför.
- Kalendern visar inte när kallelsen publicerades, eftersom det datumet
  inte finns i ärendena; tiden för partierna räknas fram till
  sammanträdet.
- Korten blir högre, så *Pågår* blir längre på mobilen.
