1. Hvordan kan du bruke NumPy og Pandas til å beregne gjennomsnitt, median og standardavvik for de innsamlede dataene, og hvorfor er disse statistiske målene viktige?
   1. Disse statistiske målene er viktige for å kunne sammenligne de forskjellige byene vi har valgt. Ved å bruke gjennomsnitt finner man raskt ut hvilken by som har gjennomsnittlig mest regn, høyest temperatur osv. (gitt at man har disse dataene). Man kan også se utviklingen over tid. Ved å bruke median finner motstår man avvikene bedre enn ved gjennomsnittet. Her finner man hvilken temperatur byen har hatt flest ganger, eller hvor mye vind man har de fleste dager. Én varm dag drar ikke medianen opp. Ved å regne ut standardavvik finner man ut hvor mye været varierer rundt gjennomsnittet. Høyt standardavvik betyr store variasjoner = ustabilt vær. 
   2. for å regne ut gjennomsnitt, median og standardavvik kan man bruke denne koden i Python(lest av CSV fil):
      1. import pandas as pd
         import numpy as np

         # Lese inn CSV-fil
         df = pd.read_csv('vaerdata.csv')

         # Beregne statistiske mål
         gjennomsnitt_temp = df['temperatur'].mean()
         median_temp = df['temperatur'].median()
         std_temp = df['temperatur'].std()

         gjennomsnitt_vind = df['vind'].mean()
         median_vind = df['vind'].median()
         std_vind = df['vind'].std()

         print("Temperatur - Gjennomsnitt:", gjennomsnitt_temp)
         print("Temperatur - Median:", median_temp)
         print("Temperatur - Standardavvik:", std_temp)

         print("Vind - Gjennomsnitt:", gjennomsnitt_vind)
         print("Vind - Median:", median_vind)
         print("Vind - Standardavvik:", std_vind)

    3. Eventuelt kan man bruke numPy direkte:
        1.  import numpy as np

            temperaturer = df['temperatur'].to_numpy()

            np.mean(temperaturer)
            np.median(temperaturer)
            np.std(temperaturer)


2. Kan du gi et eksempel på hvordan du vil implementere en enkel statistisk analyse for å undersøke sammenhengen mellom to variabler i datasettet?
   1. La oss si vi har to forskjellige variabler i datasettet: temperatur og vind, og vi vil undersøke om det finnes en sammenheng mellom disse. Vi starter med å lage en scatter plot for å visualisere sammenhengen, videre beregner man korrelasjonen mellom de to variablene. Korrelasjonen vil fortelle oss om det er sammenhengen mellom variablene. Videre kan man lage en enkelt lineær regresjon for å se om den ene variabelen påvirker den andre. i Python kan de se slik ut:
      1. import pandas as pd
        import numpy as np
        import matplotlib.pyplot as plt

        # Simulerer fiktive værdata
        data = {
            'temperatur': [12, 14, 15, 17, 16, 15, 13, 12, 11, 10],
            'vind': [3.2, 3.5, 3.7, 4.0, 3.8, 3.6, 3.3, 3.1, 3.0, 2.8]
        }

        df = pd.DataFrame(data)

        # 1. Visualisere med scatter plot
        plt.scatter(df['temperatur'], df['vind'])
        plt.title("Sammenheng mellom temperatur og vind")
        plt.xlabel("Temperatur (°C)")
        plt.ylabel("Vind (m/s)")
        plt.grid(True)
        plt.show()

        # 2. Beregn korrelasjon
        korrelasjon = df['temperatur'].corr(df['vind'])
        print("Korrelasjonskoeffisient:", korrelasjon)

3. Hvordan planlegger du å håndtere eventuelle skjevheter i dataene under analysen, og hvilke metoder vil du bruke for å sikre at analysen er pålitelig?
   1. Først må man gå frem for å finne ut om dataene inneholder skjevheter eller outliers(utliggere), ved å bruke histogrammer og boxplots kan man gjøre en visuell inspeksjon:
      1. import seaborn as sns
        sns.histplot(df['temperatur'], kde=True)
        sns.boxplot(x=df['temperatur'])
       2. beskrivende statistikk: print(df['temperatur'].describe())
    2. For å håndtere outliers kan man bruke IQR metoden for å identifisere ekstreme verdier, man kan da velge om man vil justere eller fjerne disse verdiene:
       1. Q1 = df['temperatur'].quantile(0.25)
        Q3 = df['temperatur'].quantile(0.75)
        IQR = Q3 - Q1
        df_clean = df[(df['temperatur'] >= Q1 - 1.5 * IQR) & (df['temperatur'] <= Q3 + 1.5 * IQR)]
    3. Om dataene er skjevfordelt(for eksempel høyrefordelt) kan man gjøre en log transformasjon for å gjøre dem normalfordelt:
       1. import numpy as np
        df['temperatur_log'] = np.log(df['temperatur'] + 1) 
    4. En annen metode man kan bruke for å håndtere skjevheter er å bruke median, dette vbil være mer pålitelig enn gjennomsnitt da outliers ikke drar snittet. Istedenfor standardavvik kan man bruke IQR da IQR bare måler spredningen i den midterste halvparten av dataene. Dette minsker risikoen for at outliers ødelegger snittet. 
    5. Det siste man kan gjøre for å sikre en pålitelig analyse er å fjerne duplikater, manglende verdier og outliers. Dette sørger for at ingen dataer får mer vekt enn andre på analysen og åpenbart uriktig data blir fjernet. Man burde bruke generell kode, altså kode som andre også kan forstå og bruke for å kunne kjøre analyse senere. Dette sørger for større reproduserbarhet og forståelse, noe som er viktig for samarbeid og videre dokumentasjon. 
4. Hvilke visualiseringer vil du lage for å støtte analysen din, og hvordan vil disse visualiseringene hjelpe deg med å formidle funnene dine?
   1. Jeg ville brukt histogram for å visualisere temperatur. Dette vil vise fordelingen av variabelen og gi god oversikt over eventuell skjevfordeling og outliers. Videre vil jeg bruke boxplot for å visualisere mediam. Boxplot er nyttig for å oppdage ekstremverdier og vurdere spredningen i dataene. Jeg ville også brukt en tidsserieplot for å visualisere utviklingen over tid. Dette er en god modell for å se sesonger, trender og eventuelle uregelmessigheter. 
