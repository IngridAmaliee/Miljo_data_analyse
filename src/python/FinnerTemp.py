import pandas as pd
import json
import os

class HentTemp:
    def __init__(self):
        pass

    def get_min_max_temperature(self, file_path):
        """
        Leser CSV-fil og returnerer kolonnene time, tmin, tmax og tavg.
        """
        if not isinstance(file_path, str) or not os.path.exists(file_path):
            raise FileNotFoundError(f"Filen finnes ikke: {file_path}")
        
        try:
            df = pd.read_csv(file_path, on_bad_lines='skip')

            required_cols = {'time', 'tmin', 'tmax', 'tavg'}
            if not required_cols.issubset(df.columns):
                raise ValueError(f"CSV mangler en eller flere av kolonnene: {required_cols}")

            return df[['time', 'tmin', 'tmax', 'tavg']]

        except Exception as e:
            print(f"Feil ved innlasting av CSV-fil: {e}")
            return None

    def get_temperatures_from_json(self, file_path):
        """
        Leser JSON-fil og returnerer temperaturverdier (max, mean, min).
        """
        if not isinstance(file_path, str) or not os.path.exists(file_path):
            raise FileNotFoundError(f"Filen finnes ikke: {file_path}")

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            if isinstance(data, list):
                temperatures = []
                for entry in data:
                    temp_data = {
                        "max_temp": entry.get("max_temp"),
                        "mean_temp": entry.get("mean_temp"),
                        "min_temp": entry.get("min_temp")
                    }
                    temperatures.append(temp_data)
            elif isinstance(data, dict):
                temperatures = {
                    "max_temp": data.get("max_temp"),
                    "mean_temp": data.get("mean_temp"),
                    "min_temp": data.get("min_temp")
                }
            else:
                raise ValueError("JSON-formatet er ukjent.")

            return temperatures

        except json.JSONDecodeError:
            print("JSON-filen har feil format eller er korrupt.")
        except Exception as e:
            print(f"Feil ved lesing av JSON: {e}")
        return None

    def get_mean_air_temperature_and_reference_time(self, file_path):
        """
        Henter 'mean_k(air_temperature P1D)' og 'referenceTime' fra observations-data.
        """
        if not isinstance(file_path, str) or not os.path.exists(file_path):
            raise FileNotFoundError(f"Filen finnes ikke: {file_path}")

        try:
            with open(file_path, 'r') as file:
                data = json.load(file)

            if 'data' not in data:
                raise ValueError("JSON-filen inneholder ikke 'data'-feltet.")

            results = []
            for entry in data['data']:
                if 'referenceTime' in entry and 'observations' in entry:
                    for obs in entry['observations']:
                        if obs.get('elementId') == 'mean_k(air_temperature P1D)':
                            value = obs.get('value')
                            if value is not None:
                                results.append({
                                    "referenceTime": entry['referenceTime'],
                                    "value": value
                                })
                            else:
                                print(f"⚠️ Advarsel: 'value' mangler i observasjonen: {obs}")
                else:
                    print(f"⚠️ Advarsel: Manglende 'referenceTime' eller 'observations' i oppføringen.")

            return results

        except json.JSONDecodeError:
            print("JSON-filen har feil format eller er korrupt.")
        except ValueError as ve:
            print(f"{ve}")
        except Exception as e:
            print(f"En uventet feil oppstod: {e}")
        return None

if __name__ == "__main__":
    hent_temp = HentTemp()

    # Test 1 – CSV
    csv_file_path = "data/csv/bostonData2.csv"
    print(f"\n🔍 Leser temperaturdata fra CSV: {csv_file_path}")
    tmin_tmax_tavg = hent_temp.get_min_max_temperature(csv_file_path)
    if tmin_tmax_tavg is not None:
        print("CSV-data funnet:")
        print(tmin_tmax_tavg.head())
    else:
        print("Fant ikke gyldige CSV-data.")

    # Test 2 – Temperaturer fra JSON
    json_file_path = "data/json/updated_london_weather.json"
    print(f"\nLeser temperaturer fra JSON: {json_file_path}")
    temperatures = hent_temp.get_temperatures_from_json(json_file_path)
    if temperatures is not None:
        print("Temperaturer fra JSON:")
        print(temperatures[:3] if isinstance(temperatures, list) else temperatures)
    else:
        print("Fant ikke gyldige temperaturer i JSON.")

    # Test 3 – Observasjoner
    observations_file_path = "data/json/observations_data.json"
    print(f"\nLeser observasjoner fra: {observations_file_path}")
    results = hent_temp.get_mean_air_temperature_and_reference_time(observations_file_path)
    if results:
        print(f"{len(results)} observasjoner funnet:")
        for result in results[:5]:  # skriv ut de første 5
            print(f"ReferenceTime: {result['referenceTime']}, Value: {result['value']}")
    else:
        print("Fant ingen observasjoner.")
