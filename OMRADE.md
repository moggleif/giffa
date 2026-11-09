# Område

Bevakningen gäller den södra delen av Kungsbacka kommun:

- Gällinge
- Idala
- Fjärås
- Frillesås
- Förlanda
- Åsa

Ett ärende hör till bevakningen när det berör någon av orterna eller
landsbygden runt dem. Ärenden som gäller hela kommunen tas med när de får
särskild betydelse för södra delen; skälet skrivs i ärendet.

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
