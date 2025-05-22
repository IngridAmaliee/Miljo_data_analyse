# Testing av kode 

I denne mappen finner du unit tester som tester ulike .py filer fra src mappen.   

### Hvorfor bruke unittesting?
Testing brukes for å teste deler av koden isolert for å sikre seg at den oppfører seg som den skal. Med tester kan man endre og forbedre deler av en kode uten å være redd for å ødelegge noe annet, testene viser også hvordan koden skal oppføre seg, noe som gjør det lettere å fange opp feil. Man kan også automatisere testing så man slipper å teste manuelt hver gang. Med unittesting får man altså bedre kvalitet, sturktur og kvalitetsikring under programutviklingen.

#### unittestCleanWeatherData.py 
Denne filen tester koden som renser data.
koden tester:
1. at funksjonen fungerer
2. at alle NULL verdier og uteliggeren 100.0 er fjernet
3. at alle temperaturdata ligger i et realistisk temperaturområde
4. at gjennomsnittet brukes til å erstatte uteliggeren

#### unittestFeilOgMangler.py 
Denne filen tester kode som håndterer feil og mangler i datasettene 
koden tester:
1. Interpolering mellom tall
2. Median fill
3. Forward fill
4. Backward fill
5. Ugyldig metode gir ValueError
6. Andre kolonner blir ikke fylt

#### unittestFindOutliers.py 
Denne filen tester kode som finner og håndterer uteliggere i dataene
koden tester:
1. At koden leser værdata fra en JSON-fil   
2. At den finner uteliggere
3. At den håndterer manglende verdier 
4. Sørger for at ingen falske uteliggere blir rapportert

#### unittestFrostAPI.py 
Denne filen tester koden som henter API fra frost 
Koden tester:
1. At API-kallene fungerer (ved bruk av mock)
2. Suksess og failure
3. Verifisering av filskriving 
4. Fjerner testfilen som blir laget 