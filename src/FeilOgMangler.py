#Eksempelbruk 

import pandas as pd
import numpy as np

def handle_missing_data(df, method='mean', numeric_only=True):
    """
    Håndterer manglende verdier i et datasett.

    Parametere:
    df (pd.DataFrame): Datasettet som skal behandles.
    method (str): Metode for å fylle inn manglende verdier.
                  Valgmuligheter: 'mean', 'median', 'ffill', 'bfill'.
    numeric_only (bool): Om kun numeriske kolonner skal behandles.

    Retur:
    pd.DataFrame: Ny DataFrame med manglende verdier håndtert.
    """

    # --- Parameterverifisering ---
    if not isinstance(df, pd.DataFrame):
        raise TypeError("df må være en pandas DataFrame.")
    if not isinstance(method, str):
        raise TypeError("method må være en streng.")
    if method not in ['mean', 'median', 'ffill', 'bfill']:
        raise ValueError("Ugyldig metode. Bruk 'mean', 'median', 'ffill' eller 'bfill'.")
    if not isinstance(numeric_only, bool):
        raise TypeError("numeric_only må være en boolsk verdi.")

    # --- Velg kolonner ---
    df_copy = df.copy()
    if numeric_only:
        cols_to_fill = df_copy.select_dtypes(include=[np.number]).columns
    else:
        cols_to_fill = df_copy.columns

    # --- Håndter manglende verdier ---
    if method == 'mean':
        df_copy[cols_to_fill] = df_copy[cols_to_fill].interpolate(method='linear', limit_direction='both')
    elif method == 'median':
        median_values = df_copy[cols_to_fill].median(numeric_only=numeric_only)
        df_copy[cols_to_fill] = df_copy[cols_to_fill].fillna(median_values)
    elif method in ['ffill', 'bfill']:
        df_copy[cols_to_fill] = df_copy[cols_to_fill].fillna(method=method)

    return df_copy

#eksempelbruk
if __name__ == "__main__":
    data = pd.DataFrame({
        'date': pd.date_range(start='2025-01-01', periods=10),
        'temperature': [5, np.nan, 6, 7, np.nan, 8, 9, np.nan, 10, 11]
    })

    cleaned_data = handle_missing_data(data, method='mean')
    print(cleaned_data)
