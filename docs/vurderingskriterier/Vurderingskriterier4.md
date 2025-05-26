## 1. Hvordan kan du bruke NumPy og Pandas til å beregne gjennomsnitt, median og standardavvik for de innsamlede dataene, og hvorfor er disse statistiske målene viktige?
I prosjektet bruker vi Pandas og NumPy til å beregne gjennomsnitt (mean), median (median) og standardavvik (std) for å analysere temperatur- og værdata. Dette er implementert både eksplisitt i analyse- og renseloggene (f.eks. clean_weather_data.py, FinnerTemp.py) og benyttes for å erstatte manglende verdier eller uteliggere.

Eksempel fra rensing:
```
mean = round(np.mean(df[column].dropna()), 2)
median = df[column].median()
std = df[column].std()
```
Disse statistiske målene er sentrale for å:
- Forstå sentraltendens og variasjon i miljødata
- Sammenligne byer (f.eks. London vs. Oslo)
- Identifisere ekstreme værmønstre og uregelmessigheter
- Danne grunnlag for videre prediktiv modellering

Gjennomsnitt gir et overblikk over "typiske" verdier, median gir robusthet mot uteliggere, og standardavvik beskriver spredningen i datamaterialet.

## 2. Kan du gi et eksempel på hvordan du vil implementere en enkel statistisk analyse for å undersøke sammenhengen mellom to variabler i datasettet?
Vi benytter funksjoner fra Pandas, matplotlib og scikit-learn for å utforske relasjoner i datasettet, for eksempel mellom skydekke og solskinn. I main.ipynb har vi utført analyse og korrelasjonsberegning mellom cloud_cover og sunshine fra London-datasettet:

```
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

plt.scatter(subset['cloud_cover'], subset['sunshine'], alpha=0.6, label='Data')
plt.xlabel('Skydekke (%)')
plt.ylabel('Solskinn (timer)')
plt.title('Sammenheng mellom skydekke og solskinn i London')
plt.show()

print(f"Korrelasjon mellom skydekke og solskinn: {corr:.2f}")
```
Dette gir innsikt i hvordan økt skydekke påvirker mengden solskinn, og gir et grunnlag for videre prediktiv modellering og forståelse av samspillet mellom værvariabler.

## 3. Hvordan planlegger du å håndtere eventuelle skjevheter i dataene under analysen, og hvilke metoder vil du bruke for å sikre at analysen er pålitelig?
Skjevheter håndteres på flere nivåer:

- Rensing: 
  - I clean_weather_data.py fjerner vi eller korrigerer uteliggere og manglende verdier basert på definerte grenser og sesonglogikk (f.eks. snow_depth settes til 0 i sommermånedene).
- Uteliggere: 
  - I find_outliers.py identifiseres uteliggere gjennom terskelverdier (eks. -50 til +50 °C). Disse logges og behandles eksplisitt.
- Standardisering: 
  - Vi bruker pandas.to_datetime() for å standardisere datoformat, og drop_duplicates() for å eliminere duplikater.
- Bruk av robuste mål: 
  - Median og IQR benyttes fremfor kun gjennomsnitt og standardavvik der det er hensiktsmessig, for å redusere påvirkning fra ekstreme verdier.

Disse tiltakene sikrer høyere datakvalitet og pålitelig analyse.

## 4. Hvilke visualiseringer vil du lage for å støtte analysen din, og hvordan vil disse visualiseringene hjelpe deg med å formidle funnene dine?
Visualiseringene er implementert i bl.a. LondonWeather.py, BostonWeather.py og BlindernWeather.py. Vi benytter:
- Tidsserieplott: 
  - For å vise utvikling i temperatur og nedbør over tid
- Boxplot: 
  - For å illustrere fordeling og uteliggere
- Scatterplot: 
  - For å utforske sammenhenger (f.eks. solskinn vs. temperatur)
- Histogram: 
  - For å analysere fordeling (f.eks. normalitet i trykk eller temperatur)

Disse hjelper oss med å oppdage trender, variasjoner og ekstreme verdier, og gir grunnlag for videre prediksjon og refleksjon.