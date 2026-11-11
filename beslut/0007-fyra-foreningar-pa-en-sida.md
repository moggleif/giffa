# 0007 – Hela kommunen på en sida, uppdelad på fyra föreningar

## Sammanhang

Giffå bevakade de sex orterna i södra Kungsbacka. Projektägaren ville att
de andra tre föreningarnas områden – Kungsbacka, Onsala och Särö – också
bevakas. Antingen kunde varje förening få en egen sida (och kanske ett
eget repo), eller så kunde den sida som finns täcka hela kommunen.

Ett ärende berör ofta flera orter, och källorna – kommunstyrelsen,
nämnderna, bygglov, detaljplaner – är desamma för hela kommunen. Med fyra
sidor skulle samma ärende skrivas och hållas i takt på flera ställen, och
rundan skulle göras fyra gånger.

## Beslut

En sida och ett repo för hela kommunen. `OMRADE.md` delar orterna på fyra
föreningar, en rubrik per förening med en lista över dess orter, och varje
ort hör till en enda förening. Ett ärende anger bara orter; föreningen
följer av orten. Utan val syns allt. Läsaren kan välja en förening och sedan
en ort i den; valet står i adressen som `?forening=` eller `?ort=`
och följer med mellan sidorna, som ortsvalet gjorde förut (K21, K22).

Indelningen följer Moderaternas fyra lokalföreningar i kommunen, enligt
deras webbplats, kompletterad av projektägaren för orter som föreningarnas
sidor inte nämner.

## Konsekvenser

- Adressen och namnet Giffå behålls; länkar med `?ort=` fungerar som förut.
- Rundan söker i hela kommunen. Platser och historik för de nya orterna
  läggs till i egna PR:ar, en förening i taget.
- Ett ärende som gäller hela kommunen tas fortfarande bara med när det
  får särskild betydelse för en ort, med skälet i ärendet.
- En ny förening eller en ort som flyttar är en ändring i `OMRADE.md`, inte
  i koden.
