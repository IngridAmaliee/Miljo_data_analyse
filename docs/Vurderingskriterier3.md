Vurderingskriterier oppgave 3 
1. Hvilke metoder vil du bruke for å identifisere og håndtere manglende verdier i datasettet?
   1. For å identifisere manglende data kan man bruke df.isnull().sum() for å finne de manglende verdiene. For å fjerne rader med for mange mangeldne verdier kan man bruke df.dropna() og for å fylle inn for de manglende verdiene kan man bruke for eksempel gjennomsnitt, median eller modus, basert på hva slags verdi det er snakk om. Funksjonen man bruker da er df.fillna(df.mean()). Et eksempel kan være om man mangler temperaturdata for noen dager kan man bruke gjennomsnittstemperatur for dagene før og etter for å fylle inn de manglende radene. 
2. Kan du gi et eksempel på hvordan du vil bruke list comprehensions for å manipulere dataene?
   1. I dette eksempelet tar jeg for meg en liste med temperaturdata som vi vil konvertere fra celsius til farenheit, vi erstatter None verdiene med gjennomsnittstemperaturen:
   2. temperatures_celsius = [10, 15, 20, 25, None, 30]
      valid_temps = [t for t in temperatures_celsius if t is not None]
      mean_temp = sum(valid_temps) / len(valid_temps)
      temperatures_fahrenheit = [t * 9/5 + 32 if t is not None else mean_temp * 9/5 + 32 for t in temperatures_celsius]
      print(temperatures_fahrenheit) 
3. Hvordan kan Pandas SQL (sqldf) forbedre datamanipuleringen sammenlignet med tradisjonelle Pandas-operasjoner?
   1. Med pandas SQL får vi bedre lesbarhet da de er ofte mer strukturerte enn pandas chaining operasjoner(lettere å forstå SELECT, FROM, GROUP BY enn .mean og .query da det er mer intuitivt for mennesker). Det kan også brukes til å sortere datasett før det lastes inn i Pandas, dette sparer lagring. sqldf er også mer praktisk å bruke når man skal sette sammen flere datasett da koden er lettere å forstå. Det er lurt å bruke pandas SQL når man jober med større datasett, slå sammen tabeller og når man vil ha mer lesbar og strukturert kode. 
4. Hvilke spesifikke uregelmessigheter i dataene forventer du å møte, og hvordan planlegger du å håndtere dem?
   1. Vi forventer å møte på uregelmessigheter som manglende data over tidsperioder, dataer som ikke gir mening(for eksempel at temperatur i en by er på 100 grader celsius) og forskjellig format på datoer. For å håndstere manglende data kommer vi nok til å bruke interpolasjon eller gjennomsnittsverdier, avhengig av hva slags dataer som mangler. Ved utliggere(outliers) bruker vi df.describe() og interkvarilavstand for å identisifere de. Ved forskjellig format (for eksempel datoer skrevet på forskjellige metoder), bruker vi pd.toDateTime(df['dato']) for å standardisere. 
