import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from xgboost import XGBRegressor
import plotly.io as pio
pio.renderers.default = "browser"

def vis_boston_weather(csv_fil=r"C:\anvendt_prog\Anvendt_prosjekt\data\BostonData2.csv"):
    # Les inn datafilen
    data = pd.read_csv(csv_fil)
    data.fillna(data.mean(numeric_only=True), inplace=True)
    data['time'] = pd.to_datetime(data['time'])

    # Temperaturutvikling
    fig1 = px.line(data, x='time', y='tavg', title="Gjennomsnittlig temperatur over tid Boston",
                   labels={'tavg': 'Temperatur (°C)', 'time': 'Dato'})
    fig1.show()

    # Månedlig gjennomsnittlig nedbørsmengde (barplot)
    data_monthly = data.set_index('time').resample('MS').mean(numeric_only=True).reset_index()
    fig2 = px.bar(data_monthly, x='time', y='prcp', title="Månedlig gjennomsnittlig nedbør Boston",
                  labels={'prcp': 'Nedbør (mm)', 'time': 'Måned'})
    fig2.show()

    # Vindhastighet
    fig3 = px.line(data, x='time', y='wspd', title="Vindhastighet over tid Boston",
                   labels={'wspd': 'Vindhastighet (km/t)', 'time': 'Dato'})
    fig3.show()

    # Månedlig gjennomsnittstemperatur
    fig4 = px.line(data_monthly, x='time', y='tavg', title="Månedlig gjennomsnittstemperatur Boston",
                   labels={'tavg': 'Temperatur (°C)', 'time': 'Måned'})
    fig4.show()

    # Histogram for temperaturfordeling
    fig5 = px.histogram(data, x='tavg', nbins=30, title="Temperaturfordeling Boston",
                        labels={'tavg': 'Temperatur (°C)'})
    fig5.update_traces(marker_line_color='black', marker_line_width=1)
    fig5.update_layout(yaxis_title="Antall dager")
    fig5.show()

    # --- Prediktiv modell for tavg (5 år frem) med XGBoost og måned som feature ---
    monthly = data.set_index('time').resample('MS').mean(numeric_only=True).reset_index()
    monthly['tid'] = np.arange(len(monthly))
    monthly['month'] = monthly['time'].dt.month  # Legg til måned som feature

    X = monthly[['tid', 'month']]
    y = monthly['tavg']
    model = XGBRegressor(n_estimators=200)
    model.fit(X, y)

    # Prediksjon for 5 år (60 måneder)
    future_tid = np.arange(len(monthly), len(monthly) + 60)
    last_date = monthly['time'].iloc[-1]
    future_dates = pd.date_range(last_date + pd.offsets.MonthBegin(1), periods=60, freq='MS')
    future_months = future_dates.month

    X_future = pd.DataFrame({'tid': future_tid, 'month': future_months})
    future_preds = model.predict(X_future)

    # Plotly-visualisering av historisk og predikert tavg
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=monthly['time'], y=monthly['tavg'], mode='lines', name='Historisk tavg'))
    fig_pred.add_trace(go.Scatter(x=future_dates, y=future_preds, mode='lines', name='Predikert tavg (5 år, XGBoost)', line=dict(dash='dash')))
    fig_pred.update_layout(title='Prediksjon av gjennomsnittstemperatur i Boston (neste 5 år, XGBoost, månedlig)',
                           xaxis_title='Dato', yaxis_title='Gjennomsnittstemperatur (tavg)')
    fig_pred.show()

    print("Analyse fullført. Grafene er vist :)")

if __name__ == "__main__":
    vis_boston_weather()
