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
- **Processtegen bara för planerna, och bara det händelserna säger.**
  Detaljplaner och planprogram har en process i plan- och bygglagen;
  andra ärenden har ingen, och en stege för dem skulle gissa. Stegen läses
  ur det som redan finns – händelsernas steg och ord, och tillfällena att
  tycka till – i stället för ett nytt fält i front matter. Två
  granskningsvarv visade att breda ordmönster (*anta*, *uppdrag*) fångar
  exploateringsavtal och andra beslut, så mönstren är snäva och ett läge
  som inte går att läsa ut står som okänt. Reglerna står i K33. Stegen
  står som konstanter i `webbplats/stege.py`; en datafil motiveras när
  ett tredje slag behövs.
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

- En plan vars antagande skrivits utan *antog* eller *antagit* visas som om
  antagandet kommer, och en plan där samråd eller granskning bara nämns i
  ett förslag visas med okänt läge. `bevakning/README.md` säger hur
  antagandet ska skrivas.
- En plan med begränsat förfarande visar granskningen som kommande tills
  den antas; noten under stegen säger varför.
- Kalendern visar inte när kallelsen publicerades, eftersom det datumet
  inte finns i ärendena; tiden för partierna räknas fram till
  sammanträdet.
- Planernas kort blir högre, så *Pågår* blir längre på mobilen.
