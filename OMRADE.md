# Område

Bevakningen gäller hela Kungsbacka kommun, uppdelad på fyra föreningars
områden. Indelningen följer Moderaternas fyra lokalföreningar i kommunen
som de beskrivs på [kungsbackamoderaterna.se](https://www.kungsbackamoderaterna.se/engagera-dig/),
kompletterad av projektägaren med de orter som föreningarnas sidor inte
nämner (Förlanda, Tölö, Älvsåker, Inlag, Lerberg och Släp). Föreningarna
står i den ordning sidan visar dem; varje ort hör till en förening.

## Förening Åsa

- Gällinge
- Idala
- Fjärås
- Frillesås
- Förlanda
- Åsa

## Förening Kungsbacka

- Kungsbacka stad
- Hede
- Anneberg
- Tölö
- Älvsåker
- Inlag
- Lerberg

## Förening Onsala

- Onsala
- Gottskär

## Förening Särö

- Särö
- Kullavik
- Malevik
- Vallda
- Släp

Ett ärende hör till bevakningen när det berör någon av orterna eller
landsbygden runt dem. "Kungsbacka stad" är innerstaden och stadsdelarna
runt den som inte har en egen ort i listan. Ärenden som gäller hela
kommunen tas med när de får särskild betydelse för en ort; skälet skrivs i
ärendet.

## Platser

[`platser.csv`](platser.csv) listar skolor, förskolor, äldreboenden,
idrottsanläggningar, bibliotek, föreningar, detaljplaner och andra platser
i orterna. Agenten söker på namnen där, inte bara på ortnamnen, eftersom en
handling ofta bara nämner skolan eller fastigheten.

| Kolumn       | Innehåll                                                       |
| ------------ | -------------------------------------------------------------- |
| `namn`       | Namnet som det skrivs i handlingarna                            |
| `typ`        | grundskola, förskola, äldreboende, idrott, förening, detaljplan … |
| `ort`        | En av orterna ovan                                             |
| `anteckning` | Vad platsen är; "bekräfta" när orten är osäker                  |
| `handlingar` | Hur många handlingar i kommunhandlingar som nämner namnet       |
| `exempel`    | Länk till en handling som nämner platsen                       |

Listan byggs ut när en runda hittar en ny plats. Ett namn som kan höra till
en annan del av kommunen tas bara med när en handling knyter det till en
ort ovan, och osäkra poster märks "bekräfta".
