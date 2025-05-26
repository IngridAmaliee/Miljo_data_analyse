import sys
import os
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from FinnerTemp import HentTemp
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "notebook"
import pandas as pd
import xgboost as xgb
from pandas.tseries.frequencies import to_offset
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

def vis_blindern_weather(json_fil="data/observations_data.json", temp_dir=None):
    """
    Leser inn temperaturdata fra en JSON-fil og visualiserer den historiske utviklingen
    i gjennomsnittstemperatur fra Blindern værstasjon fra og med 2014.

    Parametere:
        json_fil (str): Filsti til JSON-filen med observasjonsdata.
        temp_dir (str): (Ubrukt) Parameter for midlertidig katalog, standard None.
    """
    hent_temp = HentTemp()
    results = hent_temp.get_mean_air_temperature_and_reference_time(json_fil)
    if results and len(results) > 0:
        df = pd.DataFrame(results)
        df['referenceTime'] = pd.to_datetime(df['referenceTime'])
        df = df[df['referenceTime'] >= pd.Timestamp('2014-01-01', tz='UTC')]
        if df.empty:
            print("Ingen temperaturdata fra og med 2014.")
        else:
            fig = px.line(
                df, x='referenceTime', y='value',
                title="Blindern: Temperatur over tid (fra 2014)",
                labels={'referenceTime': 'Dato', 'value': 'Temperatur (°C)'}
            )
            fig.show()
    else:
        print("Ingen temperaturdata funnet i observations_data.json.")

def vis_blindern_prediksjon_5aar(json_fil="data/observations_data.json"):
    """
    Leser inn historiske temperaturdata og bruker XGBoost til å predikere
    gjennomsnittstemperatur i Blindern fem år frem i tid basert på sesong- og trendvariabler.

    Parametere:
        json_fil (str): Filsti til JSON-filen med observasjonsdata.
    """
    hent_temp = HentTemp()
    results = hent_temp.get_mean_air_temperature_and_reference_time(json_fil)
    if results and len(results) > 0:
        df = pd.DataFrame(results)
        df['referenceTime'] = pd.to_datetime(df['referenceTime'])
        df = df[df['referenceTime'] >= pd.Timestamp('2014-01-01', tz='UTC')]
        if df.empty:
            print("Ingen temperaturdata fra og med 2014.")
        else:
            df_pred = df.set_index('referenceTime').asfreq('D')
            df_pred = df_pred.ffill()
            df_pred = df_pred.reset_index()
            df_pred['days'] = (df_pred['referenceTime'] - df_pred['referenceTime'].min()).dt.days
            df_pred['dayofyear'] = df_pred['referenceTime'].dt.dayofyear

            X = df_pred[['days', 'dayofyear']]
            y = df_pred['value']
            model = xgb.XGBRegressor(n_estimators=100)
            model.fit(X, y)

            last_date = df_pred['referenceTime'].max()
            future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=5*365, freq='D')
            future_days = (future_dates - df_pred['referenceTime'].min()).days.values
            future_dayofyear = future_dates.dayofyear

            X_future = pd.DataFrame({'days': future_days, 'dayofyear': future_dayofyear})
            y_pred = model.predict(X_future)

            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(x=df_pred['referenceTime'], y=y, mode='lines', name='Historisk'))
            fig_pred.add_trace(go.Scatter(x=future_dates, y=y_pred, mode='lines', name='Prediksjon 5 år frem'))
            fig_pred.update_layout(
                title='Blindern: Gjennomsnittstemperatur med prediksjon 5 år frem (XGBoost, månedlig)',
                xaxis_title='År',
                yaxis_title='Gjennomsnittstemperatur (°C)'
            )
            fig_pred.show()
    else:
        print("Ingen temperaturdata funnet i observations_data.json.")

if __name__ == "__main__":
    """
    Kjører funksjoner for å vise:
    - Historisk temperaturutvikling for Blindern (fra 2014)
    - Predikert temperatur 5 år frem i tid basert på XGBoost
    """
    print("Viser historisk temperatur for Blindern...")
    vis_blindern_weather()

    print("Viser prediktiv temperatur for Blindern 5 år frem...")
    vis_blindern_prediksjon_5aar()
