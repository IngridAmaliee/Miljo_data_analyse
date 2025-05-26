from datetime import datetime
from meteostat import Daily
import pandas as pd
import os

def hent_boston_data_csv(filnavn='BostonData2.csv', start_aar=2013, slutt_aar=2023):
    """
    Henter daglige værdata for Boston og lagrer til CSV.

    Parametere:
    - filnavn (str): Navnet på filen som skal lagres i /data
    - start_aar (int): Startår for datasettet (fra 1. mars)
    - slutt_aar (int): Sluttår for datasettet (til 1. mars)

    Retur:
    - pd.DataFrame: Innhentede data
    """

    # --- Parameterverifisering ---
    if not isinstance(filnavn, str) or not filnavn.endswith('.csv'):
        raise ValueError("filnavn må være en streng som slutter med '.csv'")
    if not isinstance(start_aar, int) or not isinstance(slutt_aar, int):
        raise TypeError("start_aar og slutt_aar må være heltall.")
    if start_aar >= slutt_aar:
        raise ValueError("start_aar må være mindre enn slutt_aar.")

    # --- Sett periode ---
    start = datetime(start_aar, 3, 1)
    end = datetime(slutt_aar, 3, 1)

    # --- Hent data fra Meteostat ---
    try:
        print(f"Henter data for Boston (ID: 72509) fra {start.date()} til {end.date()}...")
        data = Daily('72509', start, end).fetch().reset_index()
    except Exception as e:
        raise ConnectionError(f"Klarte ikke hente data fra Meteostat: {e}")

    if data.empty:
        raise ValueError("Ingen data ble hentet fra Meteostat.")

    # --- Filtrer ønskede kolonner ---
    ønskede_kolonner = ['time', 'tavg', 'tmin', 'tmax', 'prcp', 'wdir', 'wspd', 'snow']
    missing_cols = set(ønskede_kolonner) - set(data.columns)
    if missing_cols:
        raise ValueError(f"Følgende kolonner mangler i datasettet: {missing_cols}")

    data = data[ønskede_kolonner]

    # --- Lagre til data-mappen ---
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        data_dir = os.path.join(project_root, 'data')
        os.makedirs(data_dir, exist_ok=True)

        filsti = os.path.join(data_dir, filnavn)
        data.to_csv(filsti, index=False)
        print(f"Boston-data er lagret i: {filsti}")
        return data

    except Exception as e:
        raise IOError(f"Feil ved lagring av CSV: {e}")

if __name__ == "__main__":
    try:
        hent_boston_data_csv(filnavn='bostonData2.csv', start_aar=2013, slutt_aar=2023)
    except Exception as e:
        print(f"Feil: {e}")

