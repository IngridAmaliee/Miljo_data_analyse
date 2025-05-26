# Informasjon om mappestrukturen 

Denne mappen inneholder tre ulike datasett og tilhørende filer som brukes i prosjektets analyser og rensetrinn.

## Om datasettene

Datasettet `BostonData2.csv` og `london_weather.csv` er hentet fra Kaggle. London-dataene ble konvertert fra CSV til JSON for enklere manipulering og testing i VSCode. Vi introduserte bevisst feil og manglende verdier i dette datasettet for å teste funksjonaliteten i våre rensings- og databehandlingsmoduler (spesielt `cleanWeatherData.py`). 

Datasettet `observations_data.json` er hentet direkte fra Frost API og inneholder værdata for Blindern (Oslo). 

## Datasettene

### `BostonData2.csv`
Inneholder værdata for Boston, inkludert:
- Gjennomsnittstemperatur over tid
- Daglig nedbør
- Vindhastighet
- Månedlig temperaturstatistikk
- Temperaturfordeling over en lengre periode

### `observations_data.json`
Inneholder værdata for Blindern hentet fra Frost API, inkludert:
- Nedbørstype
- Fuktighetsblanding
- Gjennomsnittstemperatur i luften

### `london_weather.json`
Inneholder værdata for London, inkludert:
- Dato
- Skydekke
- Solskinn
- Global stråling
- Maks/min/gjennomsnittstemperatur
- Nedbør
- Lufttrykk (Pa)
- Snødybde

### `updated_london_weather.json`
Denne filen opprettes automatisk ved kjøring av `cleanWeatherData.py` og inneholder de samme datapunktene som `london_weather.json`, men med uteliggere og manglende verdier renset og erstattet.
