import unittest
import json
import os
import numpy as np
import sys

# Sørg for at src-mappen er tilgjengelig for import
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))
from find_outliers import find_outliers_in_weather_data  # Filnavn og funksjon må være korrekt

class TestFindOutliers(unittest.TestCase):
    """
    Tester funksjonen find_outliers_in_weather_data som identifiserer uteliggere i værdata.
    """

    def setUp(self):
        """Lager en midlertidig testfil med sample værdata."""
        self.test_file = 'test_weather_data.json'
        self.sample_data_with_outliers = [
            {"max_temp": 25},
            {"max_temp": 30},
            {"max_temp": -55},  # uteligger
            {"max_temp": 60},   # uteligger
            {"max_temp": None}
        ]
        with open(self.test_file, 'w') as f:
            json.dump(self.sample_data_with_outliers, f)

    def tearDown(self):
        """Fjerner testfilen etter hver test."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_finner_uteliggere(self):
        """Sjekker at uteliggere blir korrekt identifisert."""
        outliers = find_outliers_in_weather_data(self.test_file, data_key='max_temp')
        self.assertIsNotNone(outliers, "Funksjonen burde returnere en liste med uteliggere.")
        self.assertIn(-55, outliers, "Uteliggeren -55 ble ikke funnet.")
        self.assertIn(60, outliers, "Uteliggeren 60 ble ikke funnet.")

    def test_returnerer_none_nar_ingen_uteliggere(self):
        """Sjekker at funksjonen returnerer None når ingen uteliggere finnes."""
        data = [{"max_temp": t} for t in [10, 15, 20, 25]]
        with open(self.test_file, 'w') as f:
            json.dump(data, f)
        outliers = find_outliers_in_weather_data(self.test_file, data_key='max_temp')
        self.assertIsNone(outliers, "Funksjonen skal returnere None når ingen uteliggere finnes.")

if __name__ == '__main__':
    unittest.main()
