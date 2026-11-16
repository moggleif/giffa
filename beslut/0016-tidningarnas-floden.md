# 0016 – Tidningarnas flöden varje morgon

## Sammanhang

Projektägaren vill att ärendena visar vad tidningarna skrivit om dem
(*I media och debatt*, K27), och att det fylls på av sig självt. Agentens
egen miljö når inte tidningarna, men GitHub Actions gör det. Norra
Halland och SVT Halland har RSS-flöden med rubrik, länk, datum och ingress;
flödena visar bara de senaste dygnens artiklar.

Vad varje tidning tillåter står i `KALLOR.md`. Kungsbacka-Posten,
Göteborgs-Posten, Hallandsposten och Hallands Nyheter spärrar AI-agenter i
sin `robots.txt`, och Sveriges Radios webbplats nekade agentens hämtning.
De läses inte automatiskt. SVT spärrar bara insamlingsrobotar och träning
av AI-modeller, och tillåter uttryckligen agenter som hämtar på en
människas begäran; vi tar bara rubrik, datum och länk, så SVT läses.

## Beslut

Ett arbetsflöde, `tidningar.yml`, läser flödena i `tidningar/floden.csv`
varje morgon med `python3 -m tidningar`. En artikel tas med när rubriken
eller ingressen nämner en ort, en plats eller ett uppmärksammat namn och
samtidigt något kommunen beslutar om (ord som *detaljplan*, *skola*,
*dagvatten*), och när varken ett ärende eller veckans issue redan länkar
den. Träffarna samlas i ett issue per vecka med etiketten `tidningar`,
skrivna i ärendenas format för *I media och debatt*, med orden som
träffade på en egen rad under. Artiklar som stod i förra veckans issue
tas inte med igen.

Att avgöra vilket ärende en artikel hör till kräver bedömning. Det görs av
söndagsrundan (beslut 0009), som för in artiklarna under ärendena.

Hämtningen är artig: `robots.txt` läses före flödet, User-Agent säger vem
vi är, och ett anrop som inte lyckas görs inte om utan står i issuet.

## Konsekvenser

- Ett issue i veckan, påfyllt med en kommentar per dag som har nya träffar.
- Bara rubrik, datum och länk förs in i ärendena; en Premium-artikels
  innehåll används inte.
- Äldre artiklar finns inte i flödena. När arbetsflödet kom till söktes
  de för hand med en webbsökning, och rubrik och datum lästes ur varje
  artikel; söndagsrundan kan söka efter fler.
- Ett flöde som inte går att läsa står i issuet varje dag tills det går
  igen, också när det inte finns några träffar.
- Ett nytt flöde är en rad i `tidningar/floden.csv` och en rad i
  `KALLOR.md`, efter att tidningens `robots.txt` kontrollerats.
