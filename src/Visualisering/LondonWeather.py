import pandas as pd
import plotly.express as px
import plotly.io as pio
import numpy as np
import lightgbm as lgb
from lightgbm import LGBMRegressor
import plotly.graph_objects as go
import os
pio.renderers.default = "notebook"

def vis_london_temp(json_fil="../data/json/updated_london_weather.json"):
    """
    Leser inn værdata fra London og visualiserer temperaturfordeling og månedlig gjennomsnitt.
    Parametre:
    json_fil (str): Filsti til JSON-filen med værdata. Må være en eksisterende fil med kolonnene 'min_temp', 'mean_temp', 'max_temp', 'date'.
    """
    # Parameterverifisering
    if not isinstance(json_fil, str):
        raise TypeError("json_fil må være en streng som peker til en JSON-fil.")
    if not os.path.isfile(json_fil):
        raise FileNotFoundError(f"Filen '{json_fil}' finnes ikke.")
    data = pd.read_json(json_fil)
    required_cols = {'min_temp', 'mean_temp', 'max_temp', 'date'}
    if not required_cols.issubset(data.columns):
        raise ValueError(f"JSON-filen må inneholde kolonnene: {required_cols}")

    # Filtrer på dato >= 20140101
    data = data[data['date'] >= 20140101].copy()
    if data.empty:
        print("Ingen data nyere enn 2014-01-01.")
        return

    # Gjør om 'date' til datetime
    data['date'] = pd.to_datetime(data['date'].astype(str), format='%Y%m%d', errors='coerce')
    data = data.dropna(subset=['date'])

    # Legg til en dag-indeks for x-akse
    data['day'] = range(1, len(data) + 1)

    # Histogram for hver temperaturtype
    for col in ['min_temp', 'mean_temp', 'max_temp']:
        fig = px.histogram(
            data,
            x=col,
            nbins=30,
            title=f"Fordeling av {col.replace('_', ' ')} i London (fra 2014)",
            labels={col: 'Temperatur (°C)'}
        )
        fig.show()

    # Gjennomsnittstemperatur per måned
    data_monthly = data.set_index('date').resample('M').mean(numeric_only=True).reset_index()
    fig4 = px.line(
        data_monthly,
        x='date',
        y='mean_temp',
        title="Månedlig gjennomsnittstemperatur London (fra 2014)",
        labels={'mean_temp': 'Temperatur (°C)', 'date': 'Måned'}
    )
    fig4.show()

def vis_london_prediksjon_5aar(json_fil="data/updated_london_weather.json"):
    """
    Predikerer månedlig gjennomsnittstemperatur i London 5 år frem i tid (60 måneder)
    med LightGBM og måned som feature, og visualiserer resultatet.
    Parametre:
    json_fil (str): Filsti til JSON-filen med værdata. Må være en eksisterende fil med kolonnene 'date', 'mean_temp'.
    """
    # Parameterverifisering
    if not isinstance(json_fil, str):
        raise TypeError("json_fil må være en streng som peker til en JSON-fil.")
    if not os.path.isfile(json_fil):
        raise FileNotFoundError(f"Filen '{json_fil}' finnes ikke.")
    data = pd.read_json(json_fil)
    required_cols = {'date', 'mean_temp'}
    if not required_cols.issubset(data.columns):
        raise ValueError(f"JSON-filen må inneholde kolonnene: {required_cols}")

    data = data[data['date'] >= 20140101].copy()
    data['date'] = pd.to_datetime(data['date'].astype(str), format='%Y%m%d', errors='coerce')
    data = data.dropna(subset=['date'])
    data_monthly = data.set_index('date').resample('MS').mean(numeric_only=True).reset_index()
    data_monthly['tid'] = np.arange(len(data_monthly))
    data_monthly['month'] = data_monthly['date'].dt.month
    X = data_monthly[['tid', 'month']]
    y = data_monthly['mean_temp']
    model = lgb.LGBMRegressor(verbose=-1, n_estimators=200)
    model.fit(X, y)
    future_tid = np.arange(len(data_monthly), len(data_monthly) + 60)
    last_date = data_monthly['date'].iloc[-1]
    future_dates = pd.date_range(last_date + pd.offsets.MonthBegin(1), periods=60, freq='MS')
    future_months = future_dates.month
    X_future = pd.DataFrame({'tid': future_tid, 'month': future_months})
    future_preds = model.predict(X_future)
    fig_pred = go.Figure()
    fig_pred.add_trace(go.Scatter(x=data_monthly['date'], y=data_monthly['mean_temp'], mode='lines', name='Historisk'))
    fig_pred.add_trace(go.Scatter(x=future_dates, y=future_preds, mode='lines', name='Prediksjon 5 år frem', line=dict(dash='dash')))
    fig_pred.update_layout(title='London: Gjennomsnittstemperatur med prediksjon 5 år frem (LightGBM, månedlig)',
                           xaxis_title='År', yaxis_title='Gjennomsnittstemperatur (°C)')
    fig_pred.show()

if __name__ == "__main__":
    vis_london_temp()
    vis_london_prediksjon_5aar()