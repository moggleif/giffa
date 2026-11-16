# Källor

| Källa | Vad den ger | Adress |
| ----- | ----------- | ------ |
| Kommunens politiska handlingar | Kallelser, handlingar och protokoll från KF, KS, KSAU och nämnderna, som text. Huvudkällan. | https://github.com/moggleif/kommunhandlingar |
| Kungsbacka kommuns webbplats | Nyheter, pågående detaljplaner, samråd och granskningar | https://www.kungsbacka.se |
| Kungsbackas karta | Detaljplaner, bygglov och planområden på karta | https://karta.kungsbacka.se |
| Norra Halland | Lokaltidning; rubriker om orterna | https://www.norrahalland.se |
| SVT Halland | Regionala nyheter; rubriker om orterna | https://www.svt.se/nyheter/lokalt/halland/ |
| Sveriges Radio P4 Halland | Regionala nyheter | https://sverigesradio.se/halland |
| Kungsbacka-Posten | Lokaltidning | https://www.kungsbackaposten.se |
| Göteborgs-Posten, Hallandsposten, Hallands Nyheter | Regionala tidningar | https://www.gp.se |
| Kungsbacka i siffror | Statistik om kommunen; bakgrund till ärenden, aldrig ett eget ärende | https://github.com/moggleif/politik |

Hämtningen är artig: den följer `robots.txt`, säger vem den är och håller
avstånd mellan anropen. Vad det betyder för varje källa, kontrollerat
2026-11-09:

- **Kungsbackas karta** spärrar automatisk hämtning i sin `robots.txt`.
  Agenten hämtar inte därifrån; en människa kan öppna kartan och länka en
  vy i ett ärende. Sidan bygger länkar till kartan för
  fastighetsbeteckningar, platser, gator och detaljplaner
  (`webbplats/kartlankar.py`) men hämtar ingenting.
- **Kungsbacka-Posten** spärrar AI-agenter, bland dem `ClaudeBot` och
  `anthropic-ai`, för hela webbplatsen i sin `robots.txt`. Agenten hämtar
  aldrig därifrån. En artikel som en människa länkar i ett issue får stå
  som källa med rubrik och datum.
- **Göteborgs-Posten, Hallandsposten och Hallands Nyheter** spärrar
  `ClaudeBot`, `Claude-Web` och `anthropic-ai` för hela webbplatsen
  (kontrollerat 2026-11-16) och behandlas som Kungsbacka-Posten.
- **Sveriges Radio** nekade agentens hämtning, också av `robots.txt`
  (2026-11-16). Agenten hämtar inte därifrån; en artikel som en människa
  länkar får stå med rubrik och datum.
- **SVT** tillåter alla under `User-agent: *` men spärrar `ClaudeBot` och
  `anthropic-ai`, och förbjuder att innehållet används för att träna
  AI-modeller (kontrollerat 2026-11-16). Agenten tar bara rubrik, datum och
  länk. Flödet för Halland läses varje morgon av `tidningar.yml` (K37,
  [beslut 0016](beslut/0016-tidningarnas-floden.md)).
- **Norra Halland** tillåter hämtning utom `/secure/` och `/sec/`. Många
  artiklar är låsta (Premium): ta bara rubrik, datum och länk, och märk en
  uppgift som bara står bakom låset som okänd. En tidningsartikel är en
  signal att leta upp handlingen; ärendet bygger på kommunens egen handling
  när den finns. Flödet `https://norrahalland.se/feed` läses varje morgon
  av `tidningar.yml` (K37).
