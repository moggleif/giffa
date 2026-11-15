# 0012 – KS-mötet byggs med datapoolens kod

## Sammanhang

Partierna har gruppmöte måndagskvällen före kommunstyrelsens
sammanträden. Projektägaren vill ha en sida som går igenom det kommande
sammanträdets dagordning punkt för punkt som underlag där, eftersom det
är före beslutet det går att påverka (issue #56). Kommunhandlingar har
redan en sida per sammanträde i kommunstyrelsen 2026 som läser
kallelsens dagordning, delar handlingarna per punkt, tar fram
sammanfattningen och söker historiken i alla organ (K54 och ADR-0078
där). Tolkningen av kallelsens tabell och handlingens sidor är det
svåra, och den ska inte finnas i två versioner som glider isär.

## Beslut

- **Datapoolens kod importeras, inte skrivs av.** Bygget får en
  utcheckning av kommunhandlingar som tredje argument och läser kalendern,
  kallelsen och handlingarna därifrån. Dagordningen, handlingens sidor och
  sammanfattningen tolkas med `kommunhandlingar.webbplats.dagordning` och
  `punktsidor`, som nås genom att utcheckningens `src/` läggs i
  `PYTHONPATH`. De drar in `markdown-it-py`, som installeras i
  arbetsflödena på samma version som i kommunhandlingar.
- **Historiken länkas, den räknas inte om.** Historiken i alla organ
  kräver datapoolens hela paragrafindex. Kortet länkar till punkten på
  datapoolens sida och visar själv bara ärendena i Giffå med samma
  diarienummer, med deras händelser.
- **Det Giffå lägger till är orterna och ärendena.** Orterna och
  platserna söks med samma mönster som skanningen (`skanning/termer.py`).
  Det som bara står i handlingen märks för sig, eftersom en lång handling
  som en delårsrapport nämner många orter utan att handla om dem.
- **Sidan visar nästa sammanträde och byggs om varje morgon** med resten
  av sidan (beslut 0002), så att den byter till nästa möte dagen efter
  sammanträdet och fylls när kallelsen kommit in i datapoolen.

## Konsekvenser

- Bygget, testerna och arbetsflödena `pages.yml`, `kontroll.yml` och
  `handlingar.yml` behöver en utcheckning av kommunhandlingar, och de kör
  dess kod från `main` utan fäst version. Ändras gränssnittet i
  `dagordning` eller `punktsidor` stoppar bygget, också en PR i Giffå, och
  den publicerade sidan står kvar tills nästa bygge lyckas. Ändras bara
  tolkningen byggs sidan med den nya tolkningen, som datapoolens egen sida.
- Versionen av `markdown-it-py` står i arbetsflödena och README och hålls
  för hand i takt med kommunhandlingars `pyproject.toml`.
- Beslutet ur protokollet visas inte än. Det kan läggas på samma punkt
  när sidan också ska visa ett sammanträde som varit.
