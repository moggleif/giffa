---
name: runda-2-sortera-och-skriva
description: Fas R2 i Giffå. Använd efter insamlingen för att föra varje träff till ett befintligt eller nytt ärende i bevakning/.
---

# Fas R2 – Sortera och skriv

Skapa en gren innan något skrivs.

1. **Sortera.** Hör träffen till ett ärende som redan finns i `bevakning/`
   (samma diarienummer, plan eller fastighet)? Då är den en ny händelse
   där. Annars blir den ett nytt ärende.
2. **Skriv** enligt formatet i `bevakning/README.md`. Ett nytt ärende blir
   en fil i källans mapp; en ny händelse läggs överst, med datum och länk,
   och `status` uppdateras när händelsen ändrar den.
3. **Tycka till.** Gå igenom *Kommande sammanträden* i månadens issue och
   kallelserna som har kommit. Ska ett bevakat ärende upp, eller pågår ett
   samråd eller en granskning, skriv det under *Tycka till* i ärendet med
   datum och källa. Har ett arbetsutskott föreslagit ett beslut som inte
   står i någon kallelse än, skriv det som `vantas` med organets nästa
   sammanträde ur kommunhandlingars kalender. Se också efter nästa steg för
   ärendena i kommunhandlingars tabeller för lokalbehov, initiativ och
   handlingsplaner. Tillfällen som har ägt rum flyttas till *Händelser*
   (`bevakning/README.md`).
4. **Rundan.** Lägg rundans period sist i `bevakning/rundor.csv`; det är
   den som visas som *Nytt* på startsidan. Bygg sidan och kör testerna
   enligt `README.md` – ett ärende utanför formatet stoppar bygget.
5. Återge vad källan säger. Inga slutsatser, inga värderingar. Okänt skrivs
   som okänt.
6. Läs din egen diff mot reglerna i `AGENTS.md` innan fasen är klar.

Committa, och starta sedan granskningsagenten (`.claude/agents/granskare.md`)
med grenens namn och perioden. Hittar den något blockerande: rätta och gör
om fasen.
