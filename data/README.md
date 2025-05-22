# Informasjon om mappestrukturen 

I denne mappen (data) har vi tre ulike datasett og noen ekstra filer som er knyttet ttil disse datasettene. Boston dataene er hentet ut fra Kaggle ved bruk av API. Dataene om Sola er hentet fra Frost ved bruk av API. Dataene fra London er hentet fra Kaggle ved å laste ned csv-filen lokalt på datamaskinen for så å bruke en python kode for å konvertere til en .json fil inne i VSCode. Grunnen til at vi ville ha dette datasettet som en .json fil er fordi vi ville manipulere dataene som i utgangspunktet så nokså bra ut. Vi endret bevisst på noe av dataene fordi vi ville ha et datasett med feil og mangler der vi kunne teste om koden vår (DataPreperation under src) fungerte.

## Datasettene

#### BostonData2.csv
Datasettet om Boston tar for seg forskjellig informasjon om været. Denne informasjonen inkluderer; gjennomsnittelig temperatur over tid, daglig nedbør, vindhastighet over tid, månedlig gjennomsnittstemperatur og temperaturfordeling over perioden 

#### observations_data.json
Datasettet om Sola inneholder informasjon om nedbørstype, fuktighetsblandingsforhold og gjennomsnittstemperaturen i lufta.

#### london_weather.json
London datasettet inneholder informasjon om; Dato, skydekke, solskinn, samlet stråling (global radiation), maksimum temperatur, minimum temperatur, gjennomsnittstemperatur, nedbør, trykkmåling i Pascal(Pa) og snødybde.

#### updated_london_weather.json
Det blir automatisk opprettet en oppdatert .json fil som omhandler værdataene fra London når koden fra clean_weather_data.py (under src) blir kjørt. Denne nye filen inneholder så og si de samme dataene som den originale .json filen om London, men her er det oppdaterte verdier der det opprinnelig var feil og mangler.