def visualiser_og_analyser_mangler(data_path=None):
    import pandas as pd
    import numpy as np
    import json
    import missingno as msno
    import matplotlib.pyplot as plt
    import pandasql as psql
    from pandas import json_normalize
    import os

    if data_path is None:
        data_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'london_weather.json')
    with open(data_path, 'r') as f:
        raw = json.load(f)
    df = json_normalize(raw)

    # Ikke rens dataen, kun visualiser og analyser mangler
    # Visualiser manglende verdier
    msno.matrix(df)
    plt.title('Visualisering av manglende verdier')
    plt.show()

    # Finn antall manglende verdier per kolonne
    missing_per_col = df.isnull().sum()
    print('Antall manglende verdier per kolonne:')
    print(missing_per_col)

    # Finn rader med minst én manglende verdi
    missing_rows = df[df.isnull().any(axis=1)]
    print(f'Antall rader med minst én manglende verdi: {len(missing_rows)}')
    if len(missing_rows) > 0:
        print('Eksempel på rader med mangler:')
        print(missing_rows.head())

    # For å vise hvor mangler finnes
    melted = pd.melt(df.reset_index(), id_vars=['index'])
    melted_missing = melted[melted['value'].isnull()]
    print('Melted view av manglende verdier:')
    print(melted_missing.head())

    # Finn antall manglende verdier i hver kolonne
    query = """
    SELECT variable, COUNT(*) as missing_count
    FROM melted_missing
    GROUP BY variable
    """
    result = psql.sqldf(query, locals())
    print('Oversikt over mangler:')
    print(result)
'''
if __name__ == "__main__":
    # Kjør funksjonen på både updated_london_weather.json og london_weather.json
    import os
    base_dir = os.path.dirname(__file__)
    data_files = [
        os.path.join(base_dir, '..', 'data', 'updated_london_weather.json'),
        os.path.join(base_dir, '..', 'data', 'london_weather.json')
    ]
    for data_path in data_files:
        print(f"\n--- Visualiserer mangler for: {os.path.basename(data_path)} ---")
        visualiser_og_analyser_mangler(data_path)

'''