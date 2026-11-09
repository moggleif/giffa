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
3. Återge vad källan säger. Inga slutsatser, inga värderingar. Okänt skrivs
   som okänt.
4. Läs din egen diff mot reglerna i `AGENTS.md` innan fasen är klar.

Committa, och starta sedan granskningsagenten (`.claude/agents/granskare.md`)
med grenens namn och perioden. Hittar den något blockerande: rätta och gör
om fasen.
