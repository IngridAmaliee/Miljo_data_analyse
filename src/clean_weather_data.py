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

def replace_outliers_and_nulls(df, column):
    #Erstatter uteliggere og manglende verdier med gjennomsnittet i en kolonne.
    log_null_values(df, column)

    mean = round(np.mean(df[column].dropna()), 2)
    lower, upper = calculate_bounds(df, column)

    outliers = df[(df[column] < lower) | (df[column] > upper)]
    if not outliers.empty:
        print(f"Outliers found in '{column}':")
        print(outliers)
    else:
        print(f"No outliers found in '{column}'.")

    df.loc[df[column].isnull(), column] = mean
    df.loc[(df[column] < lower) | (df[column] > upper), column] = mean
    df[column] = df[column].round(2)

    print(f"Replaced NULLs and outliers in '{column}' with mean value: {mean}")
    return df

def clean_weather_dataframe(df, data_keys):
    #Kjører rens på alle kolonner i `data_keys`.
    for key in data_keys:
        df = replace_outliers_and_nulls(df, key)
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
               'min_temp', 'precipitation', 'pressure', 'snow_depth']

    df = load_json_to_dataframe(file_path)
    cleaned_df = clean_weather_dataframe(df, columns)
    save_dataframe_to_json(cleaned_df, output_path)
