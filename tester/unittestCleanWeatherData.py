# kode som tester:
# at funksjonen fungerer
# at alle NULL verdier og uteliggeren 100.0 er fjernet
# at alle temperaturdata ligger i et realistisk temperaturområde
# at gjennomsnittet brukes til å erstatte uteliggeren

import unittest
import json
import os
import pandas as pd
import sys

# Legg til src-mappen i importstien
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from clean_weather_data import load_json_to_dataframe, clean_weather_dataframe

class TestCleanWeatherData(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_weather_data.json'
        self.keys = ['max_temp']
        test_data = [
            {"max_temp": 10},
            {"max_temp": 12},
            {"max_temp": None},   # manglende verdi
            {"max_temp": 100},    # uteligger
            {"max_temp": 11},
        ]
        with open(self.test_file, 'w') as f:
            json.dump(test_data, f)

    def tearDown(self):
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_outliers_and_nulls_replaced(self):
        df = load_json_to_dataframe(self.test_file)
        df_cleaned = clean_weather_dataframe(df, self.keys)

        self.assertIsNotNone(df_cleaned)

        # Ingen nullverdier igjen
        self.assertFalse(df_cleaned['max_temp'].isnull().any())

        # Uteliggeren 100.0 skal være erstattet
        self.assertNotIn(100.0, df_cleaned['max_temp'].values)

        # Alle verdier er i rimelig temperaturskala (eksempelvis -50 til 60)
        self.assertTrue((df_cleaned['max_temp'] >= -50).all() and (df_cleaned['max_temp'] <= 60).all())

        # Gjennomsnittet brukes til erstatning – test at det finnes i dataen
        mean_val = round(pd.Series([10, 12, 11]).mean(), 2)
        self.assertIn(mean_val, df_cleaned['max_temp'].values)

if __name__ == '__main__':
    unittest.main()
