import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import unittest
from unittest.mock import mock_open, patch
import json
import numpy as np
from DataPreperation import find_outliers_in_weather_data  #dette er feil filnavn, men skal forandres


class TestFindOutliers(unittest.TestCase):

    def setUp(self):
        # Dette er eksempeldata med én uteligger (60) og noen vanlige verdier
        self.mock_data = json.dumps([
            {"max_temp": 20},
            {"max_temp": 25},
            {"max_temp": -55},  # uteligger
            {"max_temp": 15},
            {"max_temp": None},
            {"max_temp": 60}   # uteligger
        ])

    @patch("builtins.open", new_callable=mock_open)
    def test_finds_outliers_correctly(self, mock_file):
        # Gi mocken det json-innholdet vi har laget
        mock_file.return_value.read.return_value = self.mock_data

        with patch("json.load", return_value=json.loads(self.mock_data)):
            result = find_outliers_in_weather_data("dummy_path.json", data_key='max_temp')
            expected = np.array([-55, 60])
            np.testing.assert_array_equal(result, expected)

    @patch("builtins.open", new_callable=mock_open)
    def test_returns_none_when_no_outliers(self, mock_file):
        # Ingen uteliggere i dette datasettet
        data_without_outliers = json.dumps([
            {"max_temp": 10},
            {"max_temp": 0},
            {"max_temp": 30}
        ])
        mock_file.return_value.read.return_value = data_without_outliers

        with patch("json.load", return_value=json.loads(data_without_outliers)):
            result = find_outliers_in_weather_data("dummy_path.json", data_key='max_temp')
            self.assertIsNone(result)

    @patch("builtins.open", new_callable=mock_open)
    def test_returns_none_on_invalid_key(self, mock_file):
        # Data mangler nøkkelen vi spør etter
        invalid_data = json.dumps([
            {"min_temp": 10},
            {"min_temp": 5}
        ])
        mock_file.return_value.read.return_value = invalid_data

        with patch("json.load", return_value=json.loads(invalid_data)):
            result = find_outliers_in_weather_data("dummy_path.json", data_key='max_temp')
            self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()
