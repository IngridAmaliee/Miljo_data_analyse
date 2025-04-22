import pandas as pd
import json

class HentTemp:
    def __init__(self):
        pass

    # Metode 1: Hente tmin, tmax og tavg fra CSV-fil
    def get_min_max_temperature(self, file_path):
        try:
            # Les CSV-filen til en Pandas DataFrame og hopp over problematiske linjer
            df = pd.read_csv(file_path, on_bad_lines='skip')
            
            # Hent ut time, tmin, tmax og tavg kolonnene
            tmin_tmax_tavg = df[['time', 'tmin', 'tmax', 'tavg']]
            
            # Returner DataFrame med 'time', 'tmin', 'tmax', og 'tavg'
            return tmin_tmax_tavg

        except Exception as e:
            print(f"Error loading file: {e}")
            return None

    # Metode 2: Hente max, mean og min temperatur fra JSON-fil
    def get_temperatures_from_json(self, file_path):
        try:
            # Åpne og last inn JSON-data fra filen
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Sjekk om data er en liste (som kan inneholde flere objekter)
            if isinstance(data, list):
                temperatures = []
                for entry in data:
                    # Hent ut max_temp, mean_temp og min_temp fra hvert objekt i listen
                    temp_data = {
                        "max_temp": entry.get("max_temp"),
                        "mean_temp": entry.get("mean_temp"),
                        "min_temp": entry.get("min_temp")
                    }
                    temperatures.append(temp_data)
            else:
                # Hvis data ikke er en liste, hent bare én verdi (som tidligere)
                temperatures = {
                    "max_temp": data.get("max_temp"),
                    "mean_temp": data.get("mean_temp"),
                    "min_temp": data.get("min_temp")
                }

            # Returner temperaturene
            return temperatures
        
        except Exception as e:
            print(f"Error loading file: {e}")
            return None

    # Metode 3: Hente verdien til 'mean_k(air_temperature P1D)' og referencetime
    def get_mean_air_temperature_and_reference_time(self, file_path):
        try:
            # Åpne og last inn JSON-data fra filen
            with open(file_path, 'r') as file:
                data = json.load(file)
            
            # Sjekk om 'data'-feltet finnes i JSON
            if 'data' not in data:
                raise ValueError("JSON-filen inneholder ikke 'data'-feltet.")
            
            # Iterer gjennom 'data'-feltet og hent verdien for 'mean_k(air_temperature P1D)' og 'referenceTime'
            results = []
            for entry in data['data']:
                if 'referenceTime' in entry and 'observations' in entry:
                    for observation in entry['observations']:
                        if 'elementId' in observation and observation['elementId'] == 'mean_k(air_temperature P1D)':
                            if 'value' in observation:
                                results.append({
                                    "referenceTime": entry['referenceTime'],
                                    "value": observation['value']
                                })
                            else:
                                print(f"Advarsel: 'value' mangler i observasjonen: {observation}")
                else:
                    print(f"Advarsel: Manglende 'referenceTime' eller 'observations' i oppføringen: {entry}")
            
            # Returner listen med resultater
            return results

        except FileNotFoundError:
            print(f"Filen ble ikke funnet: {file_path}")
        except json.JSONDecodeError:
            print("JSON-filen har feil format eller er korrupt.")
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print(f"En uventet feil oppstod: {e}")
        return None

# Hovedprogram for testing
if __name__ == "__main__":
    hent_temp = HentTemp()

    # Test get_min_max_temperature
    csv_file_path = r'C:\anvendt_prog\Anvendt_prosjekt\data\bostonData2.csv'
    tmin_tmax_tavg = hent_temp.get_min_max_temperature(csv_file_path)
    if tmin_tmax_tavg is not None:
        print("Data fra CSV:")
        print(tmin_tmax_tavg)

    # Test get_temperatures_from_json
    json_file_path = r'C:\anvendt_prog\Anvendt_prosjekt\data\updated_london_weather.json'
    temperatures = hent_temp.get_temperatures_from_json(json_file_path)
    if temperatures is not None:
        print("Temperaturer fra JSON:")
        print(temperatures)

    # Test get_mean_air_temperature_and_reference_time
    observations_file_path = r'C:\anvendt_prog\Anvendt_prosjekt\data\observations_data.json'
    results = hent_temp.get_mean_air_temperature_and_reference_time(observations_file_path)
    if results:
        print("Resultater hentet:")
        for result in results:
            print(f"ReferenceTime: {result['referenceTime']}, Value: {result['value']}")
    else:
        print("Ingen data ble funnet.")

