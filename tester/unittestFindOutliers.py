# kode som tester:
# at koden leser værdata fra en JSON-fil   
# at den finner uteliggere
# at den håndterer manglende verdier 
# sørger for at ingen falske uteliggere blir rapportert

import unittest
import json
import os
import numpy as np
import sys

# Sørg for at src-mappen kan importeres
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from find_outliers import find_outliers_in_weather_data

class TestFindOutliers(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_weather_data.json'
        sample_data = [
            {"max_temp": 25},
            {"max_temp": 30},
            {"max_temp": -55},  # uteligger
            {"max_temp": 60},   # uteligger
            {"max_temp": None},
        ]
        with open(self.test_file, 'w') as f:
            json.dump(sample_data, f)

    def tearDown(self):
        os.remove(self.test_file)

    def test_finner_uteliggere(self):
        outliers = find_outliers_in_weather_data(self.test_file, data_key='max_temp')
        self.assertIsNotNone(outliers)
        self.assertTrue(-55 in outliers or 60 in outliers)
    
    def test_returnerer_none_nar_ingen_uteliggere(self):
        data = [{"max_temp": t} for t in [10, 15, 20, 25]]
        with open(self.test_file, 'w') as f:
            json.dump(data, f)
        outliers = find_outliers_in_weather_data(self.test_file, data_key='max_temp')
        self.assertIsNone(outliers)

if __name__ == '__main__':
    unittest.main()
