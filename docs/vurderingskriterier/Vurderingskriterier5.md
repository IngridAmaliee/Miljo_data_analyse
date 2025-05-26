# Vurderingskriterier – Oppgave 5: Visualisering
## 1. Hvilke spesifikke typer visualiseringer planlegger du å lage for å representere endringer i luftkvalitet og temperaturdata, og hvorfor valgte du disse?
Vi har valgt visualiseringstyper som passer til ulike typer analysebehov:

`Tidsserieplot` (linjediagram) Brukes for å vise endringer i temperatur og andre værvariabler over tid. Dette er implementert i main.ipynb og egne visualiseringsnotebooks for London, Blindern og Boston.
```
plt.plot(df['date'], df['mean_temp'])
plt.title("Temperatur over tid – London")
```

`Boxplot`: Brukes for å sammenligne fordelingen av temperatur over måneder eller årstider, og identifisere uteliggere.
```
df['month'] = pd.to_datetime(df['date']).dt.month
sns.boxplot(x='month', y='mean_temp', data=df)
```

`Scatterplot`: Brukes for å utforske sammenhenger, f.eks. mellom solskinn og temperatur.
```
sns.scatterplot(data=df, x='sunshine', y='mean_temp')
```

`Histogram`: Brukes for å vise fordelingen av én variabel, f.eks. pressure.
```
sns.histplot(df['pressure'], bins=30, kde=True)
```

Visualiseringene er valgt fordi de gjør det enklere å oppdage mønstre, sesonger og ekstreme verdier som ikke alltid er synlige i rådataene.

## 2. Hvordan kan Matplotlib og Seaborn brukes til å forbedre forståelsen av de analyserte dataene, og hvilke funksjoner i disse bibliotekene vil være mest nyttige?
Vi benytter Matplotlib og Seaborn i kombinasjon. Matplotlib gir fleksibilitet, mens Seaborn gir ferdigstilte statistiske visualiseringer med få kodelinjer.

Nyttige funksjoner:
- seaborn.scatterplot() for å vise relasjoner
- seaborn.boxplot() for fordeling og uteliggere
- seaborn.heatmap() for korrelasjonsmatriser
- matplotlib.pyplot.plot() for tidsserier
- matplotlib.pyplot.subplot() for å kombinere flere grafer
- Disse verktøyene gjør det lettere å kommunisere funn og oppdage skjulte trender.

## 3. Hvordan vil du håndtere og visualisere manglende data i grafene dine for å sikre at de fortsatt er informative?
I cleanWeatherData.py håndterer vi manglende verdier eksplisitt:

- Numeriske mangler fylles med gjennomsnitt (unntak: snow_depth, som får verdi 0 i sommermånedene).
- Uteliggere erstattes med gjennomsnitt eller filtreres ut før visualisering.

For å vise hvor data mangler, kan vi bruke missingno eller Seaborn:
```
import missingno as msno
msno.matrix(df)  # Visualiserer manglende data som diagram

# Alternativ: Marker i grafen
df['missing'] = df['mean_temp'].isnull()
sns.scatterplot(x='date', y='mean_temp', hue='missing', data=df)
```
Dette sikrer at mangler ikke skjules og gir god oversikt for beslutningstaking.

## 4. Kan du beskrive prosessen for å lage interaktive visualiseringer med Widgets, Plotly eller Bokeh, og hvilke fordeler dette kan gi i forhold til statiske visualiseringer?
Vi bruker Plotly, ipywidgets og Bokeh for å lage interaktive grafer

Fordeler:

- Gir mulighet for zoom, hover og filter
- Perfekt til presentasjoner og utforskning
- Brukervennlig og intuitivt

Med `Plotly`:
```
import plotly.express as px
fig = px.scatter(df, x='mean_temp', y='sunshine', color='month', hover_data=['date'])
fig.update_layout(title="Sammenheng mellom temperatur og solskinn – interaktiv")
fig.show()

```
Med `ipywidgets`:
```
import ipywidgets as widgets
from IPython.display import display

def oppdater_graf(mnd):
    subset = df[df['month'] == mnd]
    fig = px.line(subset, x='date', y='mean_temp', title=f'Temperatur i måned {mnd}')
    fig.show()

widgets.interact(oppdater_graf, mnd=widgets.Dropdown(options=sorted(df['month'].unique())))
```
Med `Bokeh`:
```
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
output_notebook()

p = figure(x_axis_type="datetime", title="Temperatur over tid – Bokeh")
p.line(df['date'], df['mean_temp'], line_width=2)
show(p)
```
## 5. Hvordan vil du evaluere effektiviteten av visualiseringene dine i å formidle de viktigste funnene fra dataanalysen til et bredere publikum?
Effektiviteten evalueres gjennom:

- Lesbarhet og design: Klar tittel, forklarende akser, tydelige farger
- Fanger innsikt: Fanger visualiseringene trender, uteliggere og sesongmønstre?
- Respons fra medstudenter og veileder: Vi har justert visualiseringer basert på tilbakemeldinger
- Bruk av interaktive elementer: Lar brukeren selv utforske dataene (spesielt viktig i Jupyter og presentasjoner)
- Refleksjonsnotatet: Diskuterer hva som fungerte og hva som kan forbedres
