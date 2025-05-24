def hent_boston_data_csv(filnavn='BostonData2.csv', start_aar=2013, slutt_aar=2023):
    from datetime import datetime
    from meteostat import Daily
    import pandas as pd
    import os
    # Sett tidsperiode
    start = datetime(start_aar, 3, 1)
    end = datetime(slutt_aar, 3, 1)
    # Hent daglige data
    data = Daily('72509', start, end)
    data = data.fetch().reset_index()
    # Velg kolonner eksplisitt etter navn
    ønskede_kolonner = ['time', 'tavg', 'tmin', 'tmax', 'prcp', 'wdir', 'wspd', 'snow']
    data = data[ønskede_kolonner]
    # Lagre i ../data-mappen
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(project_root, 'data')
    os.makedirs(data_dir, exist_ok=True)
    filsti = os.path.join(data_dir, filnavn)
    data.to_csv(filsti, index=False)
    print(f"Boston-data er hentet og lagret i data-mappen!")

