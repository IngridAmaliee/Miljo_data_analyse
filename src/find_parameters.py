import requests

def find_parameters(sources, elements=None):
    """
    Denne funksjonen finner tilgjengelige parametere for frost.met.no basert på spesifiserte kilder og elementer.
    
    :param sources: En kommaseparert streng med kildene, f.eks. 'SN18700,SN90450'.
    :param elements: Valgfritt - En kommaseparert streng med ønskede elementer (f.eks. 'mean(air_temperature P1D)')
    
    :return: En liste med tilgjengelige parametere for kildene og elementene
    """
    
    # Endpoint for tilgjengelige tidsserier
    available_endpoint = 'https://frost.met.no/observations/availableTimeSeries/v0.jsonld'

    # Sette opp parameterne
    params = {
        'sources': sources,
    }
    
    # Hvis elementer er spesifisert, legg dem til i parameterne
    if elements:
        params['elements'] = elements

    # Utfør HTTP GET forespørsel
    r = requests.get(available_endpoint, params, auth=("f9d56ccf-fe79-45ff-970e-959f8e0de1e5", ""))
    
    # Sjekk om forespørselen var vellykket
    if r.status_code == 200:
        json = r.json()
        if 'data' in json:
            return json['data']
        else:
            print("Ingen data funnet for de angitte parameterne.")
            return None
    else:
        print(f"Feil! Statuskode: {r.status_code}")
        print(f"Feilmelding: {r.json().get('error', {}).get('message', 'Ingen feilmelding tilgjengelig')}")
        return None


# Test funksjonen
sources = 'SN18700,SN90450'
elements = 'mean(air_temperature P1D),sum(precipitation_amount P1D)'  # Kan være valgfritt

parameters = find_parameters(sources, elements)

if parameters:
    print(parameters)
