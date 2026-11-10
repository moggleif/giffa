# 0005 – Veckans kallelser i Actions

## Sammanhang

Sidan ska visa när man kan tycka till, innan beslut (K12, beslut 0004).
Kallelsen till ett sammanträde kommer ungefär en vecka före mötet. Den
månatliga skanningen (beslut 0003) hinner därför ofta inte fånga ett
ärende innan det har avgjorts.

## Beslut

Ett eget arbetsflöde, `kallelser.yml`, kör skanningen varje måndag med
`--kommande`. Då söks bara dokument till sammanträden efter dagen, och ett
issue med etiketten `kallelser` öppnas när något träffar. Koden är
densamma som för månadens skanning; bara urvalet av dokument skiljer.

## Konsekvenser

- Ett issue i veckan, och bara när något träffar. En kallelse som
  publiceras mer än en vecka före mötet kan stå i två veckors issue.
- Den som läser issuet för in träffar som rör ett bevakat ärende under
  *Tycka till* (`bevakning/README.md`). Det görs av en agent eller en
  människa, precis som rundan.
