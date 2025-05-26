import requests
import pandas as pd
import os
import json
from dotenv import load_dotenv

def hent_og_lagre_data(output_path=None):
    """
    Henter observasjonsdata fra Frost API og lagrer som JSON.
    Returnerer data som Python-objekt.
    """
    # Finn og last .env
    candidate_paths = [
        os.path.join(os.getcwd(), '.env'),
        os.path.join(os.getcwd(), '..', '.env'),
        os.path.join(os.path.dirname(__file__), '..', '.env'),
        os.path.join(os.path.dirname(__file__), '.env'),
    ]

    env_path = next((path for path in candidate_paths if os.path.exists(path)), None)
    if not env_path:
        raise FileNotFoundError("Fant ikke .env-fil i vanlige kataloger.")

    load_dotenv(dotenv_path=env_path)

    api_key = os.getenv('API_KEY_FROST')
    if not api_key:
        raise EnvironmentError("API-nøkkelen 'API_KEY_FROST' mangler i .env-filen.")

    print("API-nøkkel funnet. Starter nedlasting fra Frost API...")

    # Bygg forespørsel
    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    parameters = {
        'sources': 'SN18700',
        'elements': "mean_k(air_temperature P1D)",
        'referencetime': '2010-01-01/2020-01-01',
    }

    try:
        response = requests.get(endpoint, params=parameters, auth=(api_key, ""))
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API-forespørsel feilet: {e}")

    json_data = response.json()
    if 'data' not in json_data:
        raise ValueError("JSON-responsen mangler 'data'-feltet.")

    # Bygg DataFrame
    raw_data = json_data['data']
    df = pd.DataFrame()

    for i, item in enumerate(raw_data):
        if 'observations' in item and 'referenceTime' in item and 'sourceId' in item:
            row = pd.DataFrame(item['observations'])
            row['referenceTime'] = item['referenceTime']
            row['sourceId'] = item['sourceId']
            df = pd.concat([df, row], ignore_index=True)
        else:
            print(f"⚠️ Advarsel: Manglende felt i datapunkt {i}")

    df.reset_index(drop=True, inplace=True)

    # Lagre JSON
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)

    json_file_path = output_path or os.path.join(data_dir, 'observations_data.json')
    with open(json_file_path, 'w') as json_file:
        json.dump(json_data, json_file, indent=4)

    print(f"Data lagret til: {json_file_path}")
    return json_data

if __name__ == "__main__":
    try:
        hent_og_lagre_data()
    except Exception as e:
        print(f"Noe gikk galt: {e}")
