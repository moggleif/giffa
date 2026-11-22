# 0021 – Söndagsrundan mergas automatiskt när den är grön

## Sammanhang

Söndagsrundan ([beslut 0009](0009-handlingslankar-och-sondagsrunda.md))
öppnar en PR varje vecka som projektägaren hittills har godkänt för hand.
Rundan har redan en oberoende granskning i fas 6 och kontrollerna i CI.
Projektägaren vill att rundan når sidan utan att vänta på ett svar.

## Beslut

Den schemalagda söndagsrundan slår på automerge på sin PR när granskningen
i fas 6 inte har något blockerande kvar. PR:en mergas då av GitHub när
alla kontroller är gröna. Projektägarens beställning räknas som
bekräftelsen i fas 7, som för fas 0.

Undantaget gäller bara den schemalagda rundans PR. Alla andra PR:er,
också en runda som någon ber om för hand, mergas av en människa.

## Konsekvenser

- Repot måste tillåta automerge (inställningen *Allow auto-merge*).
- Sammanfattningen av rundan skickas fortfarande till projektägaren, som
  kan rätta i efterhand med en ny PR.
- Har granskningen blockerande fynd som inte gick att rätta öppnas PR:en
  utan automerge och väntar på projektägaren.
- Rundans instruktion står i uppgiften i Claude och följer det här
  beslutet.
