import requests
import pandas as pd
import os
from dotenv import load_dotenv
import json

def hent_og_lagre_data():
    # Last inn miljøvariabler fra .env-filen
    env_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path=env_path)

    # Hent API-nøkkel
    api_key = os.getenv('API_KEY_FROST')

    if not api_key:
        print("API-nøkkelen ble ikke funnet i .env-filen.")
        exit(1)

    print("API-nøkkelen ble lastet inn!")

    # Endepunkt og parametere
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {
        'sources': 'SN18700',
        'elements': "mean_k(air_temperature P1D)",
        'referencetime': '2010-01-01/2020-01-01',
    }

    # API-kall
    r = requests.get(endpoint, params=parameters, auth=(api_key, ""))

    if r.status_code != 200:
        print(f'Error! Returned status code {r.status_code}')
        try:
            error_data = r.json()
            print('Message:', error_data['error']['message'])
            print('Reason:', error_data['error']['reason'])
        except json.JSONDecodeError:
            print("Kunne ikke lese feilmeldingen fra API-responsen.")
        exit(1)

    json_data = r.json()

    if 'data' not in json_data:
        print("JSON-responsen inneholder ikke 'data'-feltet.")
        exit(1)

    # Bygg DataFrame
    data = json_data['data']
    df = pd.DataFrame()

    for i, item in enumerate(data):
        if 'observations' in item and 'referenceTime' in item and 'sourceId' in item:
            row = pd.DataFrame(item['observations'])
            row['referenceTime'] = item['referenceTime']
            row['sourceId'] = item['sourceId']
            df = pd.concat([df, row], ignore_index=True)
        else:
            print(f"Advarsel: Manglende felt i oppføring {i}")

    df = df.reset_index()

    # Lagre JSON til fil
    os.makedirs('data', exist_ok=True)
    json_file_path = 'data/observations_data.json'
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"Data saved to '{json_file_path}'")

    return json_data  # gjør det lettere å teste

# Kjør kun når filen kjøres direkte, ikke ved import
if __name__ == "__main__":
    hent_og_lagre_data()
