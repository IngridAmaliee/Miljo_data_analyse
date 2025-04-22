1. Hvilke spesifikke typer visualiseringer planlegger du å lage for å representere endringer i luftkvalitet og temperaturdata, og hvorfor valgte du disse?
   1. For å visualisere endringer i luftkvalitet og temperatur er det flere forskjellige metoder man kan bruke, basert på de forskjellige typene data. For å visualisere utviklingen over tid kan man bruke en tidsserieplot, altså et linjediagram. Dette gjøres ved  å plotte inn begge variabler i samme figur, med to Y akser. Eksempel:
      1. plt.plot(df['dato'], df['luftkvalitet'], label='PM2.5')
        plt.plot(df['dato'], df['temperatur'], label='Temperatur')
        plt.legend()
    2. Om man ønsker å visualisere for eksempel temperatur opp mot lutkvalitet kan man bruke et scatterplot(punktdiagram). Et slik diagram viser hvordan to variabler henger sammen ved å plassere begge i samme diagram. En regresjonslinje legges til for å vise den generelle trenden mellom verdiene. Eksempel:
       1. sns.lmplot(x='temperatur', y='luftkvalitet', data=df)
    3. Om man ønsker å se hvordan verdier utvikler seg over forskjellige perioder kan man bruke boxplot. Dette er en visualisering man ofte bruker om man vil se forandringen av værmønstre gjennom årstidene. Eksempel:
       1. df['måned'] = pd.to_datetime(df['dato']).dt.month
        sns.boxplot(x='måned', y='luftkvalitet', data=df)
2. Hvordan kan Matplotlib og Seaborn brukes til å forbedre forståelsen av de analyserte dataene, og hvilke funksjoner i disse bibliotekene vil være mest nyttige?
   1. Matplotlib er et bibliotek i Python hvor man kan visualsiere data med ulike typer grafer. Seaborn er bygget på matplotlib og sørger or at vi kan lage bedre visualiseringer av statistiske dataer som er penere og mer informative. Dette egner seg spesielt godt til datanaylse og forskning. Ved å bruke disse bibliotekene er det lettere å forstå data siden man kan se det visuelt, framfor å bare se tallene foran seg. 
3. Hvordan vil du håndtere og visualisere manglende data i grafene dine for å sikre at de fortsatt er informative?
   1. For å håndtere manglende data i grafer kan det være hensiktsmessig å fylle inn med gjennomsnitt av nærliggende data. Mangler man for eksempel temperaturdata for noen dager i Boston, kan man regne ut gjennomsnittstemperaturen for dagene før og etter og legge inn dette de dagene som mangler.
   2. Om det ikke er hensiktsmessig med gjennomsnittsdata kan man legge inn en kode som viser hvor man mangler data. Da kan man bruke biblioteket missingno:
      1. import missingno as msno
        msno.matrix(df)
        msno.heatmap(df)
    2. eller matplotlib og seaborn, eksempel:
       1. import seaborn as sns
        import matplotlib.pyplot as plt
        # Marker rader med manglende temperatur
        df['mangler_temp'] = df['temperatur'].isnull()
        # Farg punkter med og uten manglende verdier forskjellig
        sns.scatterplot(x='dato', y='123', hue='mangler_temp', data=df)
        plt.title("markering for manglende temperaturdata")
4. Kan du beskrive prosessen for å lage interaktive visualiseringer med Widgets, Plotly eller Bokeh, og hvilke fordeler dette kan gi i forhold til statiske visualiseringer?
   1. Ved å lage interaktive visualiseringer med Widgets, Plotly og Bokeh har man mange fordeler man ikke får ved å bruke statiske grafer. Med plotly.express eller plotly.graph_objects kan man lage interaktive grafer hvor man kan zoome, hovre og klikke rett inn i jupyter notebook eller inn i en nettleser. Eksempel:
      1. import plotly.express as px
        fig = px.scatter(df, x='temperatur', y='PM2_5', color='måned', hover_data=['dato'])
        fig.update_layout(title='Sammenheng mellom temperatur og PM2.5')
        fig.show()
   2.  Med Bokeh kan man lage gode visualiseringer for nettsider og kan kombineres med Widgets. Bokeh er bra å bruke når man jobber med store datasett og om man vil at brukeren skal interagere med grafene. Det fungerer også bra sammen med pandas, Numpy og Jupyter Notebook. Eksempel:
       1.  from bokeh.plotting import figure, show
            from bokeh.models import HoverTool
            from bokeh.io import output_notebook

            output_notebook()

            p = figure(title="Temperatur over tid", x_axis_type='datetime')
            p.line(df['dato'], df['temperatur'], line_width=2)

            hover = HoverTool(tooltips=[("Dato", "abc"), ("Temp", "def")], formatters={'@x': 'datetime'})
            p.add_tools(hover)

            show(p)

   3. Med ipywidgets og Plotly kan man lage små interaktive apper i notebook, dette er praktisk for eksempel ved presentasjoner eller om man ønsker å ha dynamisk filtrering og visualisering. Eksempel:
      1. import ipywidgets as widgets
        from IPython.display import display

        def oppdater_graf(måned):
            filtered = df[df['måned'] == måned]
            fig = px.line(filtered, x='dato', y='temperatur', title=f'Temperatur i måned {måned}')
            fig.show()

        widgets.interact(oppdater_graf, måned=widgets.Dropdown(options=df['måned'].unique()))

5. Hvordan vil du evaluere effektiviteten av visualiseringene dine i å formidle de viktigste funnene fra dataanalysen til et bredere publikum?