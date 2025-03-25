import pandas as pd
import numpy as np

def handle_missing_data(df, method='mean', numeric_only=True):
    """
    Håndterer manglende verdier i et datasett.
    
    Parametere:
    df (pd.DataFrame): Datasettet hentet fra en API.
    method (str): Metode for å fylle inn manglende verdier. Valgmuligheter: 'mean', 'median', 'ffill', 'bfill'.
    numeric_only (bool): Om kun numeriske kolonner skal behandles.
    
    Retur:
    pd.DataFrame: Renset datasett med utfylte verdier.
    """
    if numeric_only:
        df_numeric = df.select_dtypes(include=[np.number])
    else:
        df_numeric = df
    
    if method == 'mean':
        df_filled = df_numeric.interpolate(method='linear', limit_direction='both')
    elif method == 'median':
        df_filled = df_numeric.fillna(df_numeric.median())
    elif method == 'ffill':
        df_filled = df_numeric.fillna(method='ffill')
    elif method == 'bfill':
        df_filled = df_numeric.fillna(method='bfill')
    else:
        raise ValueError("Ugyldig metode. Bruk 'mean', 'median', 'ffill' eller 'bfill'.")
    
    df.update(df_filled)
    return df

# Eksempelbruk:
# Anta at 'data' er hentet fra en API
# data = pd.DataFrame({'date': pd.date_range(start='2025-01-01', periods=10), 'temperature': [5, np.nan, 6, 7, np.nan, 8, 9, np.nan, 10, 11]})
# cleaned_data = handle_missing_data(data, method='mean')
# print(cleaned_data)
