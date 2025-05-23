# kode som kunn finner utliggere i london_weather.json

import json
import numpy as np

def find_outliers_in_weather_data(file_path, data_key='max_temp'):
    
    try:
        # Åpne og les JSON-filen
        with open(file_path, 'r') as file:
            data = json.load(file)
        
        # Ekstraher verdiene for den spesifikke nøkkelen (for eksempel max_temp), hopp over None verdier
        sample_data_with_outliers = np.array([entry[data_key] for entry in data if entry[data_key] is not None])

        # Sett grenseverdier direkte
        lower_limit = -50
        upper_limit = 50

        # Finn uteliggere ved å bruke grenseverdiene
        outliers = sample_data_with_outliers[(sample_data_with_outliers < lower_limit) | (sample_data_with_outliers > upper_limit)]

        if len(outliers) > 0:
            return outliers
        else:
            print(f"Det er ingen uteliggere for '{data_key}' basert på de angitte grensene.")
            return None
    except Exception as e:
        print(f"Feil ved behandling av filen: {e}")
        return None

# Eksempel på hvordan du kan bruke funksjonen:
file_path = "C:\anvendt_prog\Anvendt_prosjekt\data\london_weather.json"
outliers = find_outliers_in_weather_data(file_path, data_key='max_temp')

# Skriv ut uteliggerne
if outliers is not None:
    print("Outliers:", outliers)
    
# Eksempel på hvordan du kan bruke funksjonen for min_temp
file_path = "C:\anvendt_prog\Anvendt_prosjekt\data\london_weather.json"
outliers = find_outliers_in_weather_data(file_path, data_key='min_temp')

# Skriv ut uteliggerne
if outliers is not None:
    print("Outliers for min_temp:", outliers)