# Källor

| Källa | Vad den ger | Adress |
| ----- | ----------- | ------ |
| Kommunens politiska handlingar | Kallelser, handlingar och protokoll från KF, KS, KSAU och nämnderna, som text. Huvudkällan. | https://github.com/moggleif/kommunhandlingar |
| Kungsbacka kommuns webbplats | Nyheter, pågående detaljplaner, samråd och granskningar | https://www.kungsbacka.se |
| Kungsbackas karta | Detaljplaner, bygglov och planområden på karta | https://karta.kungsbacka.se |
| Norra Halland | Lokaltidning; rubriker om orterna | https://www.norrahalland.se |
| Kungsbacka-Posten | Lokaltidning | https://www.kungsbackaposten.se |
| Kungsbacka i siffror | Statistik om kommunen; bakgrund till ärenden, aldrig ett eget ärende | https://github.com/moggleif/politik |

Hämtningen är artig: den följer `robots.txt`, säger vem den är och håller
avstånd mellan anropen. Vad det betyder för varje källa, kontrollerat
2026-11-09:

- **Kungsbackas karta** spärrar automatisk hämtning i sin `robots.txt`.
  Agenten hämtar inte därifrån; en människa kan öppna kartan och länka en
  vy i ett ärende. Sidan bygger länkar till kartan för
  fastighetsbeteckningarna (`webbplats/fastighet.py`) men hämtar ingenting.
- **Kungsbacka-Posten** spärrar AI-agenter, bland dem `ClaudeBot` och
  `anthropic-ai`, för hela webbplatsen i sin `robots.txt`. Agenten hämtar
  aldrig därifrån. En artikel som en människa länkar i ett issue får stå
  som källa med rubrik och datum.
- **Norra Halland** tillåter hämtning utom `/secure/` och `/sec/`. Många
  artiklar är låsta (Premium): ta bara rubrik, datum och länk, och märk en
  uppgift som bara står bakom låset som okänd. En tidningsartikel är en
  signal att leta upp handlingen; ärendet bygger på kommunens egen handling
  när den finns.
