# 0010 – Uppmärksammade ärenden, namnen folk använder och en sökruta

## Sammanhang

Projektägaren vill att de ärenden som väcker mest intresse ska synas
först och gå att hitta på de namn de har i folkmun, som *jättelagret i
Frillesås* eller *restaurangstråket i Åsa*, i stället för på
fastighetsbeteckningen. Vilka ärenden som är mest intressanta är en
bedömning, och namnen står sällan i handlingarna. UX-analysen 2026-11-10
lät bli en sökruta så länge webbläsarens egen sökning räckte
([kunskap/ux-analys.md](../kunskap/ux-analys.md)); med namn som inte står
på listsidorna räcker den inte längre.

## Beslut

- **En lista som projektägaren styr**, `bevakning/uppmarksammade.csv`, med
  en rad per namn och ärende: `namn`, `arende` (filnamnet utan `.md`) och
  `kalla`. Ett namn kan stå på flera ärenden, och ett ärende kan ha flera
  namn. Namnet är det ärendet kallas i folkmun eller ett gemensamt ämne,
  som *Dagvatten och översvämningar*; sidan skriver därför *Uppmärksammat
  som …* och inte *kallas*. Ordningen i filen är ordningen på startsidan, och sedan K29 också
  först i listorna.
  Källan är en länk till en artikel eller handling, texten *ärendets
  rubrik* när namnet står i rubriken, eller *projektägaren* när namnet
  kommer från projektägaren själv.
- **Namnen ligger utanför ärendefilerna.** Front matter beskriver ärendet
  som det heter i handlingarna; urvalet och namnen är redaktionella val
  som ändras oftare, och en fil är lättare att ändra på GitHub än tjugo.
- **En egen sida *Sök*** med alla ärenden och en sökruta som filtrerar i
  webbläsaren, utan något externt (`docs/sok.js`). Utan skript står hela
  listan.

## Konsekvenser

- Ett namn i listan som pekar på ett ärende som inte finns stoppar bygget,
  så att en felstavning inte försvinner tyst.
- Ett ärende som byter fil byter inte namn (beslut 0006), så listan
  behöver inte följa med statusbyten.
- Rundan föreslår nya namn men skriver dem bara när en källa ger dem.

## Ändring 2026-11-16

Projektägaren tog bort raden *Namnet: …* med källan under varje namn i
avsnittet *Ärenden med mer uppmärksamhet*: den stod i vägen. Källan står
kvar i `uppmarksammade.csv`, och en tidningsartikel som gav ett namn står
under ärendet i *I media och debatt*, märkt med en tidningsikon.

## Ändring 2026-11-19

Sökrutan på sidan *Sök* ersattes av knappen *Sök* i sajtraden, som söker i
allt på ärendena ([beslut 0018](0018-sok-i-sajtraden.md)).
