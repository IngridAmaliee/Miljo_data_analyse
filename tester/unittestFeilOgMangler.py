# kode som tester:
# interpolering mellom tall
# Median fylling
# Forward fill
# Backward fill
# ugyldig metode gir ValueError
# andre kolonner blir ikke fylt

import pandas as pd
import numpy as np

def handle_missing_data(df, method='mean', numeric_only=True):
    if numeric_only:
        df_target = df.select_dtypes(include=[np.number])
    else:
        df_target = df

    if method == 'mean':
        df_filled = df_target.interpolate(method='linear', limit_direction='both')

    elif method == 'median':
        if numeric_only:
            df_filled = df_target.fillna(df_target.median())
        else:
            df_filled = df_target.copy()
            numeric_cols = df_target.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                median = df_target[col].median()
                df_filled[col] = df_filled[col].fillna(median)

    elif method == 'ffill':
        df_filled = df_target.ffill()

    elif method == 'bfill':
        df_filled = df_target.bfill()

    else:
        raise ValueError("Ugyldig metode. Bruk 'mean', 'median', 'ffill' eller 'bfill'.")

    df.update(df_filled)
    return df

# Eksempelbruk:
# data = pd.DataFrame({'date': pd.date_range(start='2025-01-01', periods=10), 'temperature': [5, np.nan, 6, 7, np.nan, 8, 9, np.nan, 10, 11]})
# cleaned_data = handle_missing_data(data, method='mean')
# print(cleaned_data)
