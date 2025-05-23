# Vurderingskriterier – Oppgave 3: Databehandling

## 1. Hvilke metoder vil du bruke for å identifisere og håndtere manglende verdier i datasettet?

For å identifisere manglende data bruker vi `df.isnull().sum()` for å få oversikt over hvilke kolonner som har `NaN`-verdier.

- For å fjerne rader med for mange manglende verdier kan vi bruke `df.dropna()`.
- For å fylle inn manglende verdier kan vi bruke metoder som gjennomsnitt, median eller modus – avhengig av konteksten.

Eksempel:
```python
df.fillna(df.mean())  # fyll inn med kolonnegjennomsnitt
```

Et praktisk eksempel er hvis vi mangler temperaturdata for noen dager – da kan vi fylle inn med gjennomsnittstemperaturen for dagene før og etter.

## 2. EKan du gi et eksempel på hvordan du vil bruke list comprehensions for å manipulere dataene?
Vi tar utgangspunkt i en liste med temperaturdata i Celsius. Vi vil konvertere disse til Fahrenheit og erstatte None-verdier med gjennomsnittstemperaturen:
```python
temperatures_celsius = [10, 15, 20, 25, None, 30]
valid_temps = [t for t in temperatures_celsius if t is not None]
mean_temp = sum(valid_temps) / len(valid_temps)

temperatures_fahrenheit = [
    t * 9/5 + 32 if t is not None else mean_temp * 9/5 + 32 
    for t in temperatures_celsius
]
print(temperatures_fahrenheit)
```
## 3. Hvordan kan Pandas SQL (sqldf) forbedre datamanipuleringen sammenlignet med tradisjonelle Pandas-operasjoner?
pandasql.sqldf() gir forbedret lesbarhet og struktur, spesielt når du jobber med store datasett eller trenger å kombinere flere datarammer.

- Fordeler:

    - SQL-syntaks (SELECT, FROM, GROUP BY) er ofte mer intuitiv enn df.groupby().mean().query(...).
    - SQL-spørringer er lettere å feilsøke og forstå for ikke-programmerere.
    - Kan filtrere eller sortere data før lasting i Pandas, noe som er effektivt for ytelse og minnebruk.
    - sqldf passer særlig godt til:
    - Kompleks filtrering og aggregering
    - Fletting (joins) av store datasett
    - Brukere som kjenner SQL fra før

## 4. Hvilke spesifikke uregelmessigheter i dataene forventer du å møte, og hvordan planlegger du å håndtere dem?
Vanlige uregelmessigheter vi forventer:

- Manglende verdier over tid
- Ekstreme verdier (uteliggere), f.eks. 100 °C i Oslo
- Ulik datostruktur (f.eks. "01-01-2024" vs "2024/01/01")

Tiltak vi bruker:

- Interpolasjon eller gjennomsnitt for å fylle inn manglende verdier
- df.describe() og IQR-metode for å finne og håndtere uteliggere
- pd.to_datetime(df['dato']) for å standardisere datoformater

Dette sikrer at datasettet er robust, komplett og konsistent før videre analyse og visualisering.

