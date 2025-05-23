# Renser værdata fra london_weather.json og lagrer det i updated_london_weather.json.
# Denne koden håndterer uteliggere og manglende verdier i værdataene.

import pandas as pd
import pandasql as psql
import numpy as np
import json

def load_json_to_dataframe(file_path):
     #Laster JSON-fil til en Pandas DataFrame.
    with open(file_path, 'r') as file:
        data = json.load(file)
    return pd.DataFrame(data)

def log_null_values(df, column):
    #Logger rader der kolonnen inneholder None/NaN
    query = f"SELECT * FROM df WHERE {column} IS NULL"
    nulls = psql.sqldf(query, locals())
    if not nulls.empty:
        print(f"Found NULL values in '{column}':")
        print(nulls)
    else:
        print(f"No NULL values found in '{column}'.")

def calculate_bounds(df, column):
    #Returnerer nedre og øvre grense for uteliggere basert på 5%–95% kvantiler.
    return df[column].quantile(0.05), df[column].quantile(0.95)

def replace_outliers_and_nulls(df, column, bounds=None):
    # Erstatter uteliggere med gjennomsnitt, og NULL/NaN med gjennomsnitt (unntak: snow_depth i sommerhalvåret)
    log_null_values(df, column)

    mean = round(np.mean(df[column].dropna()), 2)
    # Bruk spesifikke grenser hvis oppgitt, ellers 5%-95% kvantiler
    if bounds and column in bounds:
        lower, upper = bounds[column]
    else:
        lower, upper = calculate_bounds(df, column)

    outliers = df[(df[column] < lower) | (df[column] > upper)]
    if not outliers.empty:
        print(f"Outliers found in '{column}':")
        print(outliers)
    else:
        print(f"No outliers found in '{column}'.")

    # Håndter NULL/NAN
    if column == 'snow_depth' and 'date' in df.columns:
        # Konverter dato til måned
        months = pd.to_datetime(df['date'], errors='coerce').dt.month
        # Sett NULL til 0 for mars-november (3-11), ellers til mean
        is_null = df[column].isnull()
        sommer = is_null & months.between(3, 11)
        vinter = is_null & ~months.between(3, 11)
        df.loc[sommer, column] = 0
        df.loc[vinter, column] = mean
    else:
        # Sett NULL/NAN til mean for alle andre kolonner
        df.loc[df[column].isnull(), column] = mean
    # Sett uteliggere til gjennomsnitt
    df.loc[(df[column] < lower) | (df[column] > upper), column] = mean
    df[column] = df[column].round(2)

    print(f"Replaced NULLs in '{column}' (med sesonglogikk for snow_depth) og outliers med mean value: {mean}")
    return df

def remove_duplicate_and_invalid_dates(df, date_column='date'):
    # Fjern rader med dupliserte datoer
    before = len(df)
    df = df.drop_duplicates(subset=[date_column])
    after = len(df)
    if before != after:
        print(f"Fjernet {before - after} rader med dupliserte datoer.")
    # Fjern rader med ugyldige datoer
    try:
        valid_dates = pd.to_datetime(df[date_column], errors='coerce')
        invalid_mask = valid_dates.isnull()
        if invalid_mask.any():
            print(f"Fjernet {invalid_mask.sum()} rader med ugyldige datoer.")
            df = df[~invalid_mask]
    except Exception as e:
        print(f"Feil ved sjekk av datoer: {e}")
    return df

def clean_weather_dataframe(df, data_keys, bounds=None, date_column='date'):
    # Fjern dupliserte og ugyldige datoer hvis kolonnen finnes
    if date_column in df.columns:
        df = remove_duplicate_and_invalid_dates(df, date_column)
    #Kjører rens på alle kolonner i `data_keys`.
    for key in data_keys:
        df = replace_outliers_and_nulls(df, key, bounds)
    return df

def save_dataframe_to_json(df, output_file):
    #Lagrer DataFrame til JSON-fil.
    with open(output_file, 'w') as f:
        json.dump(df.to_dict(orient='records'), f, indent=4)
    print(f"Updated data saved to {output_file}")

# Eksempel på bruk
if __name__ == "__main__":
    file_path = "data/london_weather.json"
    output_path = "data/updated_london_weather.json"
    columns = ['cloud_cover', 'sunshine', 'global_radiation', 'max_temp', 'mean_temp',
               'min_temp', 'precipitation', 'pressure', "snow_depth"]
    # Sett egne grenser for uteliggere per kolonne (eksempelverdier, tilpass etter behov)
    bounds = {
        'max_temp': (-35, 40),           # Temperatur i London: -35 til 40°C
        'min_temp': (-35, 30),           # Minimumstemperatur: -35 til 30°C
        'mean_temp': (-30, 35),          # Døgnmiddeltemperatur: -30 til 35°C
        'precipitation': (0, 100),       # Nedbør i mm/døgn: 0 til 100
        'pressure': (950, 1050),         # Lufttrykk i hPa: 950 til 1050
        'cloud_cover': (0, 100),         # Skydekke i prosent: 0 til 100
        'sunshine': (0, 18),             # Soltimer pr døgn: 0 til 18
        'global_radiation': (0, 3500),   # Stråling i Wh/m2: 0 til 3500
        'snow_depth': (0, 100)           # Snødybde i cm: 0 til 100
    }
    df = load_json_to_dataframe(file_path)
    cleaned_df = clean_weather_dataframe(df, columns, bounds, date_column='date')
    save_dataframe_to_json(cleaned_df, output_path)
