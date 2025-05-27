# Renser værdata fra london_weather.json og lagrer det i updated_london_weather.json.
# Denne koden håndterer uteliggere og manglende verdier i værdataene.

import pandas as pd
import pandasql as psql
import numpy as np
import json
import os

def load_json_to_dataframe(file_path):
    """Laster JSON-fil til en Pandas DataFrame."""
    if not isinstance(file_path, str):
        raise TypeError("file_path må være en streng.")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Filen '{file_path}' ble ikke funnet.")
    with open(file_path, 'r') as file:
        data = json.load(file)
    if not isinstance(data, list):
        raise ValueError("JSON-filen må inneholde en liste med ordbøker.")
    return pd.DataFrame(data)

def log_null_values(df, column):
    """Logger rader der kolonnen inneholder None/NaN"""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df må være en Pandas DataFrame.")
    if column not in df.columns:
        raise ValueError(f"Kolonnen '{column}' finnes ikke i DataFrame.")
    
    query = f"SELECT * FROM df WHERE {column} IS NULL"
    nulls = psql.sqldf(query, locals())
    if not nulls.empty:
        print(f"Found NULL values in '{column}':")
        print(nulls)
    else:
        print(f"No NULL values found in '{column}'.")

def calculate_bounds(df, column):
    """Returnerer nedre og øvre grense for uteliggere basert på 5%–95% kvantiler."""
    if column not in df.columns:
        raise ValueError(f"Kolonnen '{column}' finnes ikke i DataFrame.")
    return df[column].quantile(0.05), df[column].quantile(0.95)

def replace_outliers_and_nulls(df, column, bounds=None):
    """Erstatter uteliggere og NULL/NaN med gjennomsnitt."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df må være en Pandas DataFrame.")
    if column not in df.columns:
        raise ValueError(f"Kolonnen '{column}' finnes ikke i DataFrame.")

    log_null_values(df, column)

    # Finn grenser
    if bounds and column in bounds:
        lower, upper = bounds[column]
    else:
        lower, upper = calculate_bounds(df, column)

    # Beregn mean basert på gyldige verdier (ikke uteliggere og ikke NaN)
    valid_values = df[(df[column] >= lower) & (df[column] <= upper)][column].dropna()
    if valid_values.empty:
        raise ValueError(f"Ingen gyldige verdier igjen i '{column}' for å beregne gjennomsnitt.")
    
    mean = round(valid_values.mean(), 2)

    outliers = df[(df[column] < lower) | (df[column] > upper)]
    if not outliers.empty:
        print(f"Outliers found in '{column}':")
        print(outliers)
    else:
        print(f"No outliers found in '{column}'.")

    if column == 'snow_depth' and 'date' in df.columns:
        months = pd.to_datetime(df['date'], errors='coerce').dt.month
        is_null = df[column].isnull()
        sommer = is_null & months.between(3, 11)
        vinter = is_null & ~months.between(3, 11)
        df.loc[sommer, column] = 0
        df.loc[vinter, column] = mean
    else:
        df.loc[df[column].isnull(), column] = mean

    df.loc[(df[column] < lower) | (df[column] > upper), column] = mean
    df[column] = df[column].round(2)

    print(f"Replaced NULLs in '{column}' (med sesonglogikk for snow_depth) og outliers med mean value: {mean}")
    return df


def remove_duplicate_and_invalid_dates(df, date_column='date'):
    """Fjerner dupliserte og ugyldige datoer."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df må være en Pandas DataFrame.")
    if date_column not in df.columns:
        raise ValueError(f"Kolonnen '{date_column}' finnes ikke i DataFrame.")

    before = len(df)
    df = df.drop_duplicates(subset=[date_column])
    after = len(df)
    if before != after:
        print(f"Fjernet {before - after} rader med dupliserte datoer.")
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
    """Rensker og standardiserer DataFrame med værdata."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df må være en Pandas DataFrame.")
    if not isinstance(data_keys, list) or not all(isinstance(key, str) for key in data_keys):
        raise TypeError("data_keys må være en liste med strenger.")
    
    if date_column in df.columns:
        df = remove_duplicate_and_invalid_dates(df, date_column)
    for key in data_keys:
        df = replace_outliers_and_nulls(df, key, bounds)
    return df

def save_dataframe_to_json(df, output_file):
    """Lagrer DataFrame til JSON-fil."""
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df må være en Pandas DataFrame.")
    if not isinstance(output_file, str):
        raise TypeError("output_file må være en streng.")
    
    with open(output_file, 'w') as f:
        json.dump(df.to_dict(orient='records'), f, indent=4)
    print(f"Updated data saved to {output_file}")

# Eksempel på bruk
if __name__ == "__main__":
    file_path = "data/json/london_weather.json"
    output_path = "data/json/updated_london_weather.json"
    columns = ['cloud_cover', 'sunshine', 'global_radiation', 'max_temp', 'mean_temp',
               'min_temp', 'precipitation', 'pressure', "snow_depth"]
    bounds = {
        'max_temp': (-35, 40),
        'min_temp': (-35, 30),
        'mean_temp': (-30, 35),
        'precipitation': (0, 100),
        'pressure': (950, 1050),
        'cloud_cover': (0, 100),
        'sunshine': (0, 18),
        'global_radiation': (0, 3500),
        'snow_depth': (0, 100)
    }

    df = load_json_to_dataframe(file_path)
    cleaned_df = clean_weather_dataframe(df, columns, bounds, date_column='date')
    save_dataframe_to_json(cleaned_df, output_path)
