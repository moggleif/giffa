# 0017 – En varning om AI överst, i den gemensamma menyn

## Sammanhang

Sidorna på projektets sajter sammanställs av AI ur offentliga handlingar.
Projektägaren bad 2026-11-16 om en varning överst på alla sidor om att
sidorna är skapade av AI och att fel och tolkningar kan förekomma. Tre
texter föreslogs; projektägaren valde varningstriangeln ur det kortaste
förslaget och texten *Skapad med AI utifrån offentliga handlingar. Fel kan
förekomma, så kontrollera mot källan.*, alltid synlig.

## Beslut

- **Varningen ritas av `sajter.js`**, som alla sajterna laddar
  ([beslut 0013](0013-gemensam-meny-fran-giffa.md)). Den står före
  sajtraden, efter sidans hopplänk, så att hopplänken förblir först.
  Ingen sajt behöver ändras.
- **Ingen stängknapp.** Varningen ska synas på varje sida.
- **En smal rad i dämpad bärnstensfärg** med genomskinlig bakgrund, så att
  den fungerar i både ljust och mörkt tema utan egna färger per sajt.
  Triangeln ritas av `sajter.css` och läses inte upp; raden har
  `role="note"`.

## Konsekvenser

- Utan skript visas ingen varning, liksom ingen sajtrad.
- På de smalaste skärmarna tar varningen två till tre rader.
- Kungsbacka i siffror (politik) kör sina kontroller mot en fryst kopia av
  `sajter.js` och `sajter.css`. Där syns varningen först när kopian byts ut.
