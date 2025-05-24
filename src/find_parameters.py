'''import requests

# Frost API-endepunkt for kilder
endpoint = 'https://frost.met.no/sources/v0.jsonld'

# Utfør HTTP GET-forespørsel
r = requests.get(endpoint, auth=("f9d56ccf-fe79-45ff-970e-959f8e0de1e5", ""))

# Sjekk om forespørselen var vellykket og hent JSON-data
if r.status_code == 200:
    json = r.json()
    sources = json['data']  # Listen over kilder
    for source in sources:
        print(source['id'], source['name'])  # Utskrift av kildenavn og ID
else:
    print(f"Error! Returned status code {r.status_code}")
'''

#Funksjon som finner paramterer til bruk i frost api


import requests
import os
from dotenv import load_dotenv

# Last inn .env fra src-mappen
src_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(src_dir, '.env')
load_dotenv(dotenv_path)
API_KEY_FROST = os.getenv('API_KEY_FROST')
# Frost API-endepunkt for kilder
endpoint = 'https://frost.met.no/sources/v0.jsonld'

# Utfør HTTP GET-forespørsel
r = requests.get(endpoint, auth=(API_KEY_FROST, ""))



# Sjekk om forespørselen var vellykket og hent JSON-data
if r.status_code == 200:
    json = r.json()
    sources = json['data']  # Listen over kilder
    # Filtrer kildene for å finne de som har "oslo" i navnet
    for source in sources:
        source_name = source.get('name', '').lower()  # Hent kildens navn og gjør det til små bokstaver
        if 'oslo' in source_name:  # Sjekk om "oslo" er i kildens navn
            print(f"Source ID: {source['id']}, Source Name: {source['name']}")
else:
    print(f"Error! Returned status code {r.status_code}")


'''
import requests

# Frost API-endepunkt for observasjoner
endpoint = 'https://frost.met.no/observations/v0.jsonld'

# Parametre for forespørselen
params = {
    'sources': 'SN68173',  # Kilde-ID for værstasjonen SN68173
    'elements': 'air_temperature,precipitation_amount',  # Eksempel på elementer
    'referencetime': '2020-01-01/2020-12-31'  # Tidsperiode for observasjoner
}

# Utfør HTTP GET-forespørsel
r = requests.get(endpoint, params=params, auth=("f9d56ccf-fe79-45ff-970e-959f8e0de1e5", ""))

# Sjekk om forespørselen var vellykket og hent JSON-data
if r.status_code == 200:
    json = r.json()
    if 'data' in json:
        data = json['data']
        print(f"Elementer for værstasjon {params['sources']}:")
        for item in data:
            # Vis alle tilgjengelige observasjoner
            for observation in item.get('observations', []):
                print(f"Element ID: {observation['elementId']}, Value: {observation['value']}")
    else:
        print("Ingen data funnet for denne værstasjonen.")
else:
    print(f"Error! Returned status code {r.status_code}")
    print(r.text)  # Utskrift av feilmelding for ytterligere feilsøking
'''
