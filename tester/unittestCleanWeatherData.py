import unittest
import json
import os
import pandas as pd
import sys

# Legg til src-mappen i importstien slik at vi kan importere funksjonene som skal testes
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from clean_weather_data import load_json_to_dataframe, clean_weather_dataframe

class TestCleanWeatherData(unittest.TestCase):
    """
    Tester renselogikken i clean_weather_data.py:
    - Håndtering av manglende verdier (None)
    - Håndtering av uteliggere
    - Bruk av eksplisitte grenser (bounds)
    - Korrekt bruk av gjennomsnitt
    """

    def setUp(self):
        """Oppretter en midlertidig testfil med testdata."""
        self.test_file = 'test_weather_data.json'
        self.keys = ['max_temp']
        self.bounds = {'max_temp': (5, 20)}  # Tvinger 100 til å bli uteligger

        self.test_data = [
            {"max_temp": 10},
            {"max_temp": 12},
            {"max_temp": None},   # Manglende verdi
            {"max_temp": 100},    # Uteligger
            {"max_temp": 11},
        ]

        with open(self.test_file, 'w') as f:
            json.dump(self.test_data, f)

    def tearDown(self):
        """Sletter testfilen etter at testen er ferdig."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_outliers_and_nulls_replaced(self):
        """Tester at NULL og uteliggere blir korrekt erstattet med gjennomsnitt."""
        df = load_json_to_dataframe(self.test_file)
        df_cleaned = clean_weather_dataframe(df, self.keys, bounds=self.bounds)

        self.assertIsNotNone(df_cleaned, "DataFrame som returneres skal ikke være None.")
        self.assertIn('max_temp', df_cleaned.columns, "Kolonnen 'max_temp' mangler i resultatet.")

        # 1. Ingen NaN igjen
        self.assertFalse(df_cleaned['max_temp'].isnull().any(), "Det finnes fortsatt NaN-verdier i kolonnen.")

        # 2. Uteligger (100) skal være fjernet
        self.assertNotIn(100.0, df_cleaned['max_temp'].values, "Uteliggeren 100.0 ble ikke erstattet.")

        # 3. Alle verdier er innen et rimelig temperaturintervall
        self.assertTrue((df_cleaned['max_temp'] >= -50).all() and (df_cleaned['max_temp'] <= 60).all(),
                        "En eller flere verdier er utenfor akseptabelt temperaturintervall.")

        # 4. Verifiser at gjennomsnittet av de gyldige verdiene ble brukt
        expected_mean = round(pd.Series([10, 12, 11]).mean(), 2)
        replacements = df_cleaned['max_temp'].tolist().count(expected_mean)

        self.assertGreaterEqual(replacements, 2, f"Gjennomsnittet {expected_mean} ble ikke brukt minst to ganger som forventet.")

if __name__ == '__main__':
    unittest.main()
