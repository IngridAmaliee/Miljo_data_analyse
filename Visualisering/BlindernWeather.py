import sys
import os
import shutil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from FinnerTemp import HentTemp
import plotly.express as px
import plotly.io as pio
pio.renderers.default = "browser"
import pandas as pd
from datetime import timedelta
import xgboost as xgb
from pandas.tseries.frequencies import to_offset
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

def vis_blindern_weather(json_fil=r"/Users/evinehfagerhaug/Library/Mobile Documents/com~apple~CloudDocs/Downloads/TDT4114/Miljo_data_analyse/data/observations_data.json", temp_dir=None):
    hent_temp = HentTemp()
    results = hent_temp.get_mean_air_temperature_and_reference_time(json_fil)
    if results and len(results) > 0:
        df = pd.DataFrame(results)
        df['referenceTime'] = pd.to_datetime(df['referenceTime'])
        # Filtrer på data fra og med 2014, matcher tidssone
        df = df[df['referenceTime'] >= pd.Timestamp('2014-01-01', tz='UTC')]
        if df.empty:
            print("Ingen temperaturdata fra og med 2014.")
        else:
            fig = px.line(df, x='referenceTime', y='value',
                          title="Blindern: Temperatur over tid (fra 2014)",
                          labels={'referenceTime': 'Dato', 'value': 'Temperatur (°C)'} )
            fig.show()
            # --- Prediktiv visualisering 5 år frem i tid med XGBoost (med sesongvariasjon) ---
            # Forbered data
            df_pred = df.set_index('referenceTime').asfreq('D')
            df_pred = df_pred.ffill()
            df_pred = df_pred.reset_index()
            df_pred['days'] = (df_pred['referenceTime'] - df_pred['referenceTime'].min()).dt.days
            df_pred['dayofyear'] = df_pred['referenceTime'].dt.dayofyear
            X = df_pred[['days', 'dayofyear']]
            y = df_pred['value']
            # Tren XGBoost-modell med sesongvariabel
            model = xgb.XGBRegressor(n_estimators=100)
            model.fit(X, y)
            # Lag fremtidig dato-range
            last_date = df_pred['referenceTime'].max()
            future_dates = pd.date_range(last_date + pd.Timedelta(days=1), periods=5*365, freq='D')
            future_days = (future_dates - df_pred['referenceTime'].min()).days.values
            future_dayofyear = future_dates.dayofyear
            X_future = pd.DataFrame({'days': future_days, 'dayofyear': future_dayofyear})
            y_pred = model.predict(X_future)
            # Visualiser fremtidig prediksjon
            import plotly.graph_objects as go
            fig_pred = go.Figure()
            fig_pred.add_trace(go.Scatter(x=df_pred['referenceTime'], y=y, mode='lines', name='Historisk'))
            fig_pred.add_trace(go.Scatter(x=future_dates, y=y_pred, mode='lines', name='Prediksjon 5 år frem'))
            fig_pred.update_layout(title='Blindern: Temperatur med prediksjon 5 år frem (XGBoost, sesong)',
                                  xaxis_title='Dato', yaxis_title='Temperatur (°C)')
            fig_pred.show()
    else:
        print("Ingen temperaturdata funnet i observations_data.json.")

    # Slett midlertidig mappe hvis spesifisert (alltid etter plot)
    if temp_dir:
        # Slett alle forekomster av temp_dir i hele prosjektet
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        for root, dirs, files in os.walk(project_root):
            for d in dirs:
                if d == temp_dir:
                    temp_path = os.path.join(root, d)
                    if os.path.exists(temp_path) and os.path.isdir(temp_path):
                        try:
                            shutil.rmtree(temp_path)
                            print(f"Mappen '{temp_path}' er slettet.")
                        except Exception as e:
                            print(f"Kunne ikke slette mappen '{temp_path}': {e}")

def vis_blindern_weather_with_extended_regression(json_fil="data/observations_data.json", temp_dir="__pycache__"):
    hent_temp = HentTemp()
    results = hent_temp.get_mean_air_temperature_and_reference_time(json_fil)
    
    if not results or len(results) == 0:
        print("Ingen temperaturdata funnet.")
        return

    df = pd.DataFrame(results)
    df['referenceTime'] = pd.to_datetime(df['referenceTime'])
    df = df[df['referenceTime'] >= pd.Timestamp('2014-01-01', tz='UTC')]

    if df.empty:
        print("Ingen data etter 2014.")
        return

    # --- XGBoost-prediksjon ---
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
    future_dates = pd.date_range(start=last_date + timedelta(days=1), periods=5*365, freq='D')
    future_days = (future_dates - df_pred['referenceTime'].min()).days.values
    future_dayofyear = future_dates.dayofyear
    X_future = pd.DataFrame({'days': future_days, 'dayofyear': future_dayofyear})
    y_future_pred = model.predict(X_future)

    # --- Lineær regresjonsanalyse ---
    linreg = LinearRegression()
    linreg.fit(df_pred[['days']], y)
    all_days = np.concatenate([df_pred['days'].values, future_days])
    all_dates = list(df_pred['referenceTime']) + list(future_dates)
    y_trend_full = linreg.predict(all_days.reshape(-1, 1))

    # --- Visualisering ---
    fig = go.Figure()

    # Historiske data
    fig.add_trace(go.Scatter(x=df_pred['referenceTime'], y=y, mode='lines', name='Historisk'))

    # XGBoost-prediksjon
    fig.add_trace(go.Scatter(x=future_dates, y=y_future_pred, mode='lines', name='Prediksjon (XGBoost)', line=dict(color='blue', dash='dot')))

    # Lineær regresjonslinje utvidet 5 år
    fig.add_trace(go.Scatter(x=all_dates, y=y_trend_full, mode='lines', name='Trendlinje (regresjon)', line=dict(color='red')))

    fig.update_layout(
        title='Blindern: Temperatur med prediksjon og trendlinje 5 år frem',
        xaxis_title='Dato',
        yaxis_title='Temperatur (°C)',
        template='plotly_white'
    )

    fig.show()

    # Slett midlertidig mappe hvis spesifisert
    if temp_dir:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        for root, dirs, _ in os.walk(project_root):
            for d in dirs:
                if d == temp_dir:
                    temp_path = os.path.join(root, d)
                    try:
                        shutil.rmtree(temp_path)
                        print(f"Slettet midlertidig mappe: {temp_path}")
                    except Exception as e:
                        print(f"Kunne ikke slette {temp_path}: {e}")

if __name__ == "__main__":
    # Kjør funksjonen som lager XGBoost-prediksjon og trendlinje
    vis_blindern_weather_with_extended_regression()

    # Om du også har en annen funksjon, f.eks. vis_blindern_weather:
    vis_blindern_weather()


