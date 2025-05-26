import requests

def get_frost_sources(client_id, filter_name=None):
    """
    Henter en liste over værkilder fra Frost API.

    Parametere:
    - client_id (str): API-nøkkel fra frost.met.no
    - filter_name (str | None): Del av stedsnavn for filtrering (eks: 'oslo')

    Retur:
    - list av dict: Liste over kilder
    """
    if not isinstance(client_id, str) or not client_id:
        raise ValueError("client_id må være en ikke-tom streng.")

    endpoint = 'https://frost.met.no/sources/v0.jsonld'
    try:
        response = requests.get(endpoint, auth=(client_id, ""))
        response.raise_for_status()
        sources = response.json().get('data', [])

        if filter_name:
            filter_name = filter_name.lower()
            sources = [
                s for s in sources
                if filter_name in s.get('name', '').lower()
            ]
        return sources

    except requests.exceptions.RequestException as e:
        print(f"Feil ved henting av kilder: {e}")
        return []

def get_frost_observations(client_id, source_id, elements, referencetime):
    """
    Henter observasjonsdata fra Frost API.

    Parametere:
    - client_id (str): API-nøkkel
    - source_id (str): Kilde-ID (f.eks. 'SN68173')
    - elements (str): Komma-separert liste over elementer (f.eks. 'air_temperature')
    - referencetime (str): Datoområde (f.eks. '2020-01-01/2020-12-31')

    Retur:
    - list av dict: Observasjonsdata
    """
    if not all(isinstance(arg, str) and arg for arg in [client_id, source_id, elements, referencetime]):
        raise ValueError("Alle parametere må være ikke-tomme strenger.")

    endpoint = 'https://frost.met.no/observations/v0.jsonld'
    params = {
        'sources': source_id,
        'elements': elements,
        'referencetime': referencetime
    }

    try:
        response = requests.get(endpoint, params=params, auth=(client_id, ""))
        response.raise_for_status()
        return response.json().get('data', [])
    except requests.exceptions.RequestException as e:
        print(f"❌ Feil ved henting av observasjoner: {e}")
        return []

def print_sources(sources):
    """
    Skriver ut ID og navn for hver kilde.
    """
    if not sources:
        print("Ingen kilder funnet.")
        return
    for s in sources:
        print(f"Source ID: {s.get('id')}, Source Name: {s.get('name')}")

def print_observations(data, source_id):
    """
    Skriver ut observasjoner for gitt kilde.
    """
    if not data:
        print(f"Ingen observasjoner funnet for {source_id}.")
        return

    print(f"\nObservasjoner fra {source_id}:")
    for item in data:
        for obs in item.get('observations', []):
            print(f"Element ID: {obs.get('elementId')}, Value: {obs.get('value')}")

if __name__ == "__main__":
    CLIENT_ID = "f9d56ccf-fe79-45ff-970e-959f8e0de1e5"

    print("Starter forespørsel til Frost API for å hente kilder som inneholder 'oslo'...")
    sources = get_frost_sources(CLIENT_ID, filter_name="oslo")

    if sources:
        print("Vellykket! Skriver ut relevante kilder:\n")
        print_sources(sources)
    else:
        print("Ingen kilder funnet eller noe gikk galt.")
