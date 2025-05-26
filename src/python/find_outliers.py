# kode som kunn finner utliggere i london_weather.json

import json
import numpy as np
import os

def find_outliers_in_weather_data(file_path, data_key='max_temp', lower_limit=-50, upper_limit=50):
    """
    Identifiserer uteliggere i værdata basert på forhåndsdefinerte grenser.

    Parametere:
    file_path (str): Filbane til JSON-filen med værdata.
    data_key (str): Nøkkelen i hver datapost som inneholder verdien (f.eks. 'max_temp').
    lower_limit (float): Nedre grenseverdi for å vurdere uteliggere.
    upper_limit (float): Øvre grenseverdi for å vurdere uteliggere.

    Retur:
    np.ndarray | None: Numpy-array med uteliggere, eller None hvis ingen funnet.
    """

    # --- Parameterverifisering ---
    if not isinstance(file_path, str):
        raise TypeError("file_path må være en streng.")
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Filen '{file_path}' finnes ikke.")
    if not isinstance(data_key, str):
        raise TypeError("data_key må være en streng.")
    if not isinstance(lower_limit, (int, float)) or not isinstance(upper_limit, (int, float)):
        raise TypeError("lower_limit og upper_limit må være numeriske verdier.")
    if lower_limit >= upper_limit:
        raise ValueError("lower_limit må være mindre enn upper_limit.")

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Sjekk at data er en liste med dicts
        if not isinstance(data, list) or not all(isinstance(entry, dict) for entry in data):
            raise ValueError("JSON-filen må inneholde en liste med ordbøker.")

        # Ekstraher verdier, hopp over None eller manglende nøkler
        values = [entry[data_key] for entry in data if data_key in entry and entry[data_key] is not None]

        if not values:
            print(f"Ingen gyldige verdier funnet for '{data_key}' i datasettet.")
            return None

        values_array = np.array(values)

        outliers = values_array[(values_array < lower_limit) | (values_array > upper_limit)]

        if outliers.size > 0:
            return outliers
        else:
            print(f"Det er ingen uteliggere for '{data_key}' basert på grensene {lower_limit}–{upper_limit}.")
            return None

    except json.JSONDecodeError:
        print("Feil: Kunne ikke lese JSON-formatet. Sjekk at filen er gyldig.")
        return None
    except Exception as e:
        print(f"Uventet feil ved behandling av filen: {e}")
        return None

if __name__ == "__main__":
    file_path = "data/london_weather.json"
    
    for key in ['max_temp', 'min_temp']:
        outliers = find_outliers_in_weather_data(file_path, data_key=key)
        if outliers is not None:
            print(f"Outliers for {key}:", outliers)
