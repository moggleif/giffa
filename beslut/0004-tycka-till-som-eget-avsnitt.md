# 0004 – Tillfällen att tycka till som eget avsnitt i ärendet

## Sammanhang

Bevakningens syfte är att visa när man kan påverka, innan något beslutas
och i rätt tid. Ärendena hade fälten `synpunkter` och `synpunkter_senast`.
De rymde bara ett samråd eller en granskning med en sista dag, inte ett
kommande beslut i en nämnd eller i fullmäktige, och inget ärende använde
dem.

## Beslut

Ett eget avsnitt, *Tycka till*, med rader i samma format som händelserna.
Fler fält räcker inte för flera tillfällen, och framtida datum i
*Händelser* skulle visas i tabellen och under *Nytt* som om de redan
hänt. Raderna tolkas med samma kod som händelserna, och varje tillfälle
har en källa. Fälten `synpunkter` och `synpunkter_senast` tas bort.

## Konsekvenser

- Startsidan visar *Tycka till nu* överst, och kort och rader markeras
  (K12).
- Vad som visas beror på byggdagen. Därför byggs sidan också varje
  morgon i `pages.yml`.
- Rundan för in kommande beslut ur kallelserna och kalendern
  (`runda-2-sortera-och-skriva`).
