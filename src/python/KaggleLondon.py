import pandas as pd
import os

def csv_til_json_london(csv_file="london_weather.csv", json_file="london_weather.json"):
    """
    Leser en CSV-fil og konverterer innholdet til JSON-format.

    Parametere:
    - csv_file (str): Filnavn eller sti til CSV-filen.
    - json_file (str): Filnavn eller sti for lagring av JSON-resultatet.

    Retur:
    - bool: True hvis konvertering var vellykket, ellers False.
    """

    # --- Parameterverifisering ---
    if not isinstance(csv_file, str) or not csv_file.endswith('.csv'):
        raise ValueError("csv_file må være en streng som slutter på '.csv'.")
    if not isinstance(json_file, str) or not json_file.endswith('.json'):
        raise ValueError("json_file må være en streng som slutter på '.json'.")
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV-filen ble ikke funnet: {csv_file}")

    try:
        df = pd.read_csv(csv_file)
        df.to_json(json_file, orient="records", indent=4)
        print(f"Konvertert '{csv_file}' til JSON og lagret som '{json_file}'")
        return True

    except pd.errors.EmptyDataError:
        print("CSV-filen er tom.")
    except pd.errors.ParserError as e:
        print(f"Feil ved parsing av CSV: {e}")
    except Exception as e:
        print(f"Uventet feil: {e}")
    
    return False

if __name__ == "__main__":
    try:
        success = csv_til_json_london("data/csv/london_weather.csv", "data/json/london_weather.json")
        if success:
            print("JSON-fil er klar for bruk.")
        else:
            print("Konvertering mislyktes.")
    except Exception as e:
        print(f"Kritisk feil: {e}")
