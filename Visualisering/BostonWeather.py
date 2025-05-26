import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
pio.renderers.default = "notebook"





def vis_boston_weather(csv_fil="data/bostonData2.csv"):
    """
    Leser inn værdata fra Boston og visualiserer temperatur, nedbør og vind
    ved hjelp av interaktive grafer.

    Parametre:
    csv_fil (str): Filsti til CSV-filen med værdata.
    """
    # Leser inn datafilen
    data = pd.read_csv(csv_fil)
    data['time'] = pd.to_datetime(data['time'])
    data.drop_duplicates(inplace=True)
    data = data[(data['time'].dt.year >= 2014)]
    data.fillna(data.mean(numeric_only=True), inplace=True)

    # Temperaturutvikling
    fig1 = px.line(data, x='time', y='tavg',
                   title="Gjennomsnittlig temperatur over tid Boston",
                   labels={'tavg': 'Temperatur (°C)', 'time': 'Dato'})
    fig1.show()

    # Månedlig gjennomsnittlig nedbørsmengde (barplot)
    data_monthly = data.set_index('time').resample('MS').mean(numeric_only=True).reset_index()
    fig2 = px.bar(data_monthly, x='time', y='prcp',
                  title="Månedlig gjennomsnittlig nedbør Boston",
                  labels={'prcp': 'Nedbør (mm)', 'time': 'Måned'})
    fig2.show()

    # Vindhastighet
    fig3 = px.line(data, x='time', y='wspd',
                   title="Vindhastighet over tid Boston",
                   labels={'wspd': 'Vindhastighet (km/t)', 'time': 'Dato'})
    fig3.show()

    # Månedlig gjennomsnittstemperatur
    fig4 = px.line(data_monthly, x='time', y='tavg',
                   title="Månedlig gjennomsnittstemperatur Boston",
                   labels={'tavg': 'Temperatur (°C)', 'time': 'Måned'})
    fig4.show()

    # Histogram for temperaturfordeling
    fig5 = px.histogram(data, x='tavg', nbins=30,
                        title="Temperaturfordeling Boston",
                        labels={'tavg': 'Temperatur (°C)'})
    fig5.update_traces(marker_line_color='black', marker_line_width=1)
    fig5.update_layout(yaxis_title="Antall dager")
    fig5.show()

    print("Analyse fullført. Grafene er vist :)")


def boxplot_mnd_gjennomsnitt(csv_fil):
    """
    Lager et boxplot som viser fordelingen av gjennomsnittstemperatur per 
    måned fra 2014 og fremover. Gir innsikt i sesongvariasjon og spredning.

    Parametre:
    csv_fil (str): Filsti til CSV-filen med værdata.
    """
    # Leser inn datafilen og konverterer dato
    data = pd.read_csv(csv_fil)
    data['time'] = pd.to_datetime(data['time'])
    data.drop_duplicates(inplace=True)
    data = data[data['time'].dt.year >= 2014]
    data.fillna(data.mean(numeric_only=True), inplace=True)

    # Ekstraherer år og måned
    data['year'] = data['time'].dt.year
    data['month'] = data['time'].dt.month_name(locale='no_NO').str[:3].str.capitalize()

    # Beregner månedlige gjennomsnitt og lager boxplot
    monthly_avg = data.groupby(['year', 'month'])['tavg'].mean().reset_index()
    ordered_months = ["Jan", "Feb", "Mar", "Apr", "Mai", "Jun",
                      "Jul", "Aug", "Sep", "Okt", "Nov", "Des"]
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='month', y='tavg', data=monthly_avg,
                order=ordered_months)
    plt.title('Boxplot av gjennomsnittlig temperatur per måned (2014 og fremover)')
    plt.xlabel('Måned')
    plt.ylabel('Gjennomsnittstemperatur (tavg)')
    plt.show()

    print("Boxplot av gjennomsnittlig temperatur per måned fra 2014 er vist.")



def vis_boston_prediksjon_5aar(csv_fil="data/bostonData2.csv"):
    data = pd.read_csv(csv_fil)
    data['time'] = pd.to_datetime(data['time'])
    data = data[(data['time'].dt.year >= 2014)]
    data.fillna(data.mean(numeric_only=True), inplace=True)
    monthly = data.set_index('time').resample('MS').mean(numeric_only=True).reset_index()
    monthly['tid'] = np.arange(len(monthly))
    monthly['month'] = monthly['time'].dt.month

    X = monthly[['tid', 'month']]
    y = monthly['tavg']
    model = XGBRegressor(n_estimators=200)
    model.fit(X, y)

    # Prediksjon for 5 år (60 måneder)
    future_tid = np.arange(len(monthly), len(monthly) + 60)
    last_date = monthly['time'].iloc[-1]
    future_dates = pd.date_range(last_date + pd.offsets.MonthBegin(1),
                                  periods=60, freq='MS')
    future_months = future_dates.month
    X_future = pd.DataFrame({'tid': future_tid, 'month': future_months})
    future_preds = model.predict(X_future)

    # Visualisering av historisk og predikert temperatur
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=monthly['time'], y=monthly['tavg'],
                                  mode='lines', name='Historisk tavg'))
    fig_pred.add_trace(go.Scatter(x=future_dates, y=future_preds,
                                  mode='lines', name='Predikert tavg (5 år, XGBoost)',
                                  line=dict(dash='dash')))
    fig_pred.update_layout(title='Prediksjon av gjennomsnittstemperatur i Boston (neste 5 år, XGBoost, månedlig)',
                           xaxis_title='Dato', yaxis_title='Gjennomsnittstemperatur (tavg)')
    fig_pred.show()


def regresjonsanalyse_boston(csv_fil):
    """
    Utfører lineær regresjonsanalyse på månedlig gjennomsnittstemperatur
    fra 2014 og frem til siste tilgjengelige dato, og predikerer 
    temperaturutviklingen 5 år frem i tid.

    Evaluerer modellen med R²-score og MSE, og visualiserer både
    historiske verdier, gjennomsnitt og fremtidig prediksjon.

    Parametre:
    csv_fil (str): Filsti til CSV-filen med værdata.
    """
    # Leser inn datafilen og filtrerer fra 2014
    data = pd.read_csv(csv_fil)
    data['time'] = pd.to_datetime(data['time'])
    data = data[data['time'] >= '2014-01-01']
    data.drop_duplicates(inplace=True)
    data.fillna(data.mean(numeric_only=True), inplace=True)
    siste_dato = data['time'].max()

    # Beregner månedlig gjennomsnitt og lager tidsvariabel
    monthly = data.set_index('time').resample('MS') \
        .mean(numeric_only=True).reset_index()
    monthly['tid'] = np.arange(len(monthly))
    X = monthly[['tid']]
    y = monthly['tavg']

    # Deler data i trening og test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Trener lineær regresjonsmodell og evaluerer
    linreg = LinearRegression()
    linreg.fit(X_train, y_train)
    y_pred_test = linreg.predict(X_test)
    r2 = r2_score(y_test, y_pred_test)
    mse = mean_squared_error(y_test, y_pred_test)
    print(f"R²-score (testdata): {r2:.3f}")
    print(f"Mean Squared Error (testdata): {mse:.3f}")

    # Predikerer 5 år frem i tid (60 måneder)
    future_tid = np.arange(len(monthly), len(monthly) + 60)
    future_dates = pd.date_range(
        start=siste_dato + pd.offsets.MonthBegin(1),
        periods=60, freq='MS'
    )
    X_future = pd.DataFrame({'tid': future_tid})
    y_future_pred = linreg.predict(X_future)

    # Visualiserer historisk tavg, historisk snitt og prediksjon
    fig_linreg = go.Figure()
    fig_linreg.add_trace(go.Scatter(
        x=monthly['time'], y=y, mode='lines', name='Historisk tavg'
    ))
    fig_linreg.add_trace(go.Scatter(
        x=[monthly['time'].min(), siste_dato],
        y=[y.mean(), y.mean()],
        mode='lines',
        name='Historisk gjennomsnitt (2014–2023)',
        line=dict(color='green', dash='dash')
    ))
    fig_linreg.add_trace(go.Scatter(
        x=future_dates, y=y_future_pred, mode='lines',
        name='Predikert tavg (Lineær regresjon)',
        line=dict(color='red', dash='dot')
    ))
    fig_linreg.update_layout(
        title='Lineær regresjonsanalyse: Temperatur i Boston '
              '(fra 2023 + 5 år frem)',
        xaxis_title='Dato',
        yaxis_title='Gjennomsnittstemperatur (tavg)'
    )
    fig_linreg.show()

    print("Lineær regresjonsanalyse fullført.")








if __name__ == "__main__":
    csv_fil = "data/BostonData2.csv"
    vis_boston_weather(csv_fil)
    regresjonsanalyse_boston(csv_fil)
    boxplot_mnd_gjennomsnitt(csv_fil)