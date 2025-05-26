# Enhetstester

Denne mappen inneholder alle enhetstester (unittest) for applikasjonens mest kritiske funksjoner. Testene er skrevet i Python med unittest-rammeverket og bidrar til å verifisere at funksjonene fungerer som forventet både i suksess og feilsituasjoner. 

Alle testene følger Arrange-Act-Assert-prinsippet og dekker både positive og negative testtilfeller. 

## Testfiler i mappen:
- `unittestCleanWeatherData.py`
- `unittestFeilOgMangler.py`
- `unittestFindOutliers.py`
- `unittestFrostAPI.py`

### Hvorfor bruke enhetstesting?
Testing brukes for å teste deler av koden isolert for å sikre seg at den oppfører seg som den skal. Med tester kan man endre og forbedre deler av en kode uten å være redd for å ødelegge noe annet. 
Testene:
- Tester koden isolert, modul for modul
- Avdekker feil tidlig i utviklingsløpet
- Øker tryggheten ved refaktorering
- Dokumenterer forventet funksjonalitet
- Gjør det enkelt å automatisere testkjøring
- Øker kvalitet og robusthet i hele systemet

## Oversikt over testfiler

#### `unittestCleanWeatherData.py`

Denne testen tester renselogikken i cleanWeatherData.py, og fokuserer på håndtering av manglende verdier og uteliggere.

Kort oppsummering:
1. At funksjonene fungerer som forventet og returnerer en renset DataFrame.
2. At alle NULL-verdier fjernes og erstattes korrekt.
3. At uteliggeren 100.0 blir erstattet.
4. At alle temperaturverdier etter rensing ligger innenfor et fornuftig område (her: −50 °C til 60 °C).
5. At gjennomsnittsverdien fra ikke-manglende data brukes som erstatning (f.eks. 11.0 i testdataene).
6. At testfilene ryddes opp etter bruk 


#### `unittestFeilOgMangler.py` 

Denne koden definerer funksjonen handle_missing_data (fra filen FeilOgMangler.py i src-mappen), som behandler manglende verdier (NaN) i en Pandas DataFrame ved å bruke én av fire strategier: 'mean', 'median', 'ffill' eller 'bfill'.

Kort oppsummering:
1. Interpolering mellom tall (mean)
2. Median fill både med og uten numeric_only = True
3. Forward fill (ffill) 
4. Backward fill (bfill)
5. Ugyldig metode gir ValueError
6. Sikre at ikke- numeriske kolonner ikke endres ved numeric_only = True

#### `unittestFindOutliers.py` 

Denne unittest-filen tester funksjonen find_outliers_in_weather_data() (fra find_outliers.py i src-mappen), som identifiserer uteliggere i en JSON-fil basert på faste grenser (f.eks. under -50 eller over 50 °C).

Kort oppsummering:
1. Om funksjonen klarer å identifisere faktiske uteliggere (som -55 og 60).
2. At den returnerer None når ingen verdier er uteliggere.
3. At den hopper over None-verdier i datasettet uten å krasje.
4. At resultatet er en NumPy-array, som forventet fra funksjonen.
5. At testfilene ryddes opp etter bruk 

#### `unittestFrostBlindern.py`

Denne unittest-filen tester funksjonen hent_og_lagre_data() (fra FrostBlindern.py i src-mappen), som henter værdata fra Frost API og lagrer dem som JSON. Testene bruker unittest.mock for å simulere API-respons – noe som gjør dem både raske og uavhengige av internettforbindelse eller faktisk API-nøkkel.

Kort oppsummering:
1. Simulerer et vellykket API-kall og verifiserer at data lagres riktig i JSON.
2. Simulerer et API-feilscenario og sjekker at funksjonen håndterer det med SystemExit.
3. Verifiserer at filen blir lagret riktig og ryddes opp etter test.
4. Bruker mock og miljøvariabler for å unngå ekte API-kall.
