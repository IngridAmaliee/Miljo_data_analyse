import requests
import pandas as pd
import os
from dotenv import load_dotenv
import json

# Spesifiser stien til .env-filen (hvis den ligger i hovedmappen "anvendt_prosjekt")
load_dotenv(dotenv_path=os.path.join(os.getcwd(), 'anvendt_prosjekt', '.env'))

# Hent API-nøkkelen fra miljøvariablene
api_key = os.getenv('API_KEY_FROST')

# Sjekk om API-nøkkelen ble lastet inn
if api_key:
    print("API-nøkkelen ble lastet inn!")
else:
    print("API-nøkkelen ble ikke funnet i .env-filen.")

# Endepunkt for API-et
endpoint = 'https://frost.met.no/observations/v0.jsonld'

parameters = {
    'sources': 'SN18700', #blindern oslo
    'elements': "mean_k(air_temperature P1D)",
    'referencetime': '2010-01-01/2020-01-01',
}

# Utfør HTTP GET-forespørsel
r = requests.get(endpoint, parameters, auth=(api_key, ""))

# Sjekk om forespørselen fungerte, og skriv ut eventuelle feil
if r.status_code == 200:
    json_data = r.json()
    print('Data retrieved from frost.met.no!')
else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json_data['error']['message'])
    print('Reason: %s' % json_data['error']['reason'])

# Opprett DataFrame fra JSON-data
data = json_data['data']
df = pd.DataFrame()

for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    row['sourceId'] = data[i]['sourceId']
    df = pd.concat([df, row], ignore_index=True)

# Tilbakestill indeksen på DataFrame
df = df.reset_index()

# Sjekk om mappen "data" finnes, hvis ikke opprett den
if not os.path.exists('data'):
    os.makedirs('data')

# Lagre JSON-data i en fil i mappen "data"
json_file_path = 'data/observations_data.json'

# Lagre data til fil
with open(json_file_path, 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print(f"Data saved to '{json_file_path}'")
