# Beskrivelse av mappe 

Denne mappen inneholder all logikk og funksjonalitet knyttet til innhenting, konvertering og behandling av miljødata, både fra API og lokale filer. Alt skript er utviklet for å kunne brukes både direkte og i samspill med main.ipynb. 

## Filoversikt - `src`

### main.ipynb
Prosjektets hovedgrensesnitt og demonstrasjonsfil. Filen inneholder trinnvis gjennomgang av datainnhenting, behandling, visualisering og analyse. 

## Filoversikt - `python`

### cleanWeatherData.py 
Renser værdata fra London ved hjelp av blant annet pandas, numpy og pandasql. 

### FeilOgMangler.py
Hjelpefunksjon som håndterer feil og mangler i samtlige datasett. Filen støtter flere strategier som mean, median, ffill og bfill. 

### findOutliers.py
Identifiserer ekstreme verdier fra datasett basert på absolutte terskler (f eks -10°C til 10°C). Programmet brukes som en del av kvalitetssikring av data. 

### findParameters.py 
Henter og lagrer metadata og parametere som skal brukes i koden frostBlindern.py. Disse parameterne representerer værstasjoner. 

### FinnerTemp.py
Funksjonalitet som henter ut eksklusivt temperatur data fra frostBlindern.py. Brukes også i forbindelse med prediktive modeller. 

### FrostBlindern.py
Henter inn datasett med værdata for Blindern (Oslo) fra Frost ved hjelp av en API nøkkel og lagrer det som en strukturert JSON- fil. Dette krever gyldig API- nøkkel i .env. (dataen er altså ikke lagret lokalt).

### KaggleBoston.py
Henter inn en .csv fil ved bruk av en API (bostonData2.csv, som du finner i datamappen). Denne filen håndterer innlasting og konvertering for videre behandling. 

### KaggleLondon.py
Denne filen konverterer værdata for London fra csv nedlastet fra Kaggle til en JSON- fil for videre analyse. 

---

Se tester mappen for tilhørende tester. 

Kjør main.ipynb for full oversikt og sammenehng mellom alle delene. 