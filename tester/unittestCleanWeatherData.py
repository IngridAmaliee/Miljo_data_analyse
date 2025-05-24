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
    Tester renselogikken i clean_weather_data.py, spesielt:
    - Håndtering av manglende verdier (None)
    - Håndtering av uteliggere
    - Bruk av eksplisitte grenser (bounds)
    - Riktig bruk av gjennomsnitt ved erstatning
    """

    def setUp(self):
        """Oppretter en midlertidig testfil med testdata."""
        self.test_file = 'test_weather_data.json'
        self.keys = ['max_temp']
        self.bounds = {'max_temp': (5, 20)}  # Tvinger 100 til å bli uteligger
        test_data = [
            {"max_temp": 10},
            {"max_temp": 12},
            {"max_temp": None},   # Manglende verdi
            {"max_temp": 100},    # Uteligger
            {"max_temp": 11},
        ]
        with open(self.test_file, 'w') as f:
            json.dump(test_data, f)

    def tearDown(self):
        """Sletter testfilen etter at testen er ferdig."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_outliers_and_nulls_replaced(self):
        """Tester at NULL og uteliggere blir korrekt erstattet med gjennomsnitt."""
        df = load_json_to_dataframe(self.test_file)
        df_cleaned = clean_weather_dataframe(df, self.keys, bounds=self.bounds)

        self.assertIsNotNone(df_cleaned, "Returnert DataFrame skal ikke være None")

        # Ingen nullverdier igjen
        self.assertFalse(df_cleaned['max_temp'].isnull().any(), "DataFrame inneholder fortsatt NULL-verdier")

        # Uteliggeren 100.0 skal være erstattet
        self.assertNotIn(100.0, df_cleaned['max_temp'].values, "Uteliggeren 100.0 ble ikke fjernet")

        # Alle verdier er i rimelig temperaturskala
        self.assertTrue((df_cleaned['max_temp'] >= -50).all() and (df_cleaned['max_temp'] <= 60).all(),
                        "Noen temperaturer er utenfor akseptabelt intervall")

        # Verifiser at gjennomsnittet brukes (fra 10, 12, 11)
        expected_mean = round(pd.Series([10, 12, 11]).mean(), 2)
        self.assertIn(expected_mean, df_cleaned['max_temp'].values,
                      f"Gjennomsnittet {expected_mean} ble ikke brukt som erstatning")

if __name__ == '__main__':
    unittest.main()

