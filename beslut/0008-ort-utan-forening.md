# 0008 – Orten går att välja utan att först välja förening

Ersätter den del av [0007](0007-fyra-foreningar-pa-en-sida.md) som säger
att läsaren väljer en förening och sedan en ort i den.

## Sammanhang

Med 0007 syntes ortknapparna först när en förening var vald. Den som ville
se en ort fick först veta vilken förening orten hör till. Projektägaren
ville kunna välja ort direkt; har man valt en förening ska bara dess orter
visas, annars alla.

## Beslut

Under föreningsknapparna står alltid alla orter i en enda rad, i svensk
bokstavsordning och inte uppdelade per förening; det är så läsaren letar
efter sin ort. En vald förening döljer de andra föreningarnas
ortknappar och visar ärendena i sina orter; en vald ort visar bara den
ortens ärenden. Förening och ort är två val som står var för sig i
adressen, `?forening=`, `?ort=` eller båda. En ort som inte hör till den
valda föreningen släpps. En tryckt knapp som trycks igen släpper sitt val,
*Alla* släpper båda (K21, K22).

Knappar valdes framför en rullgardin: alla val syns på en gång,
de är stora att träffa och fungerar likadant som föreningsknapparna.

## Konsekvenser

- Länkar med `?ort=` eller `?forening=` fungerar som förut. En länk med
  bara `?ort=` visar nu alla gruppers knappar, inte bara ortens förening.
- Utan val är listan över orter lång, och vilken förening en ort hör till
  syns inte i den. En ny ort i `OMRADE.md` gör listan längre.
