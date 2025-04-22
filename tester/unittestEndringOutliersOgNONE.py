import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import json
import numpy as np

# Importere funksjonene som skal testes
from DataPreperation import find_outliers_and_handle_missing, save_to_json

class TestFindOutliersAndHandleMissing(unittest.TestCase):

    @patch('builtins.open')
    @patch('pandas.DataFrame')
    def test_handle_null_values_and_outliers(self, MockDataFrame, mock_open):
        """
        Test at NULL-verdier og uteliggere håndteres korrekt.
        """

        # Simulere JSON-data
        mock_data = [
            {'cloud_cover': 10, 'sunshine': None, 'global_radiation': 20},
            {'cloud_cover': 110, 'sunshine': 100, 'global_radiation': None},
            {'cloud_cover': 15, 'sunshine': 25, 'global_radiation': 40},
        ]
        
        # Mock åpning og lasting av JSON
        mock_open.return_value.__enter__.return_value.read.return_value = json.dumps(mock_data)
        
        # Simulere pandas DataFrame
        df_mock = MagicMock(spec=pd.DataFrame)
        MockDataFrame.return_value = df_mock
        df_mock.__getitem__.side_effect = lambda x: [10, 110, 15] if x == 'cloud_cover' else [None, 100, 25]
        df_mock.dropna.return_value = [10, 15]
        df_mock.mean.return_value = np.mean([10, 15])
        df_mock.std.return_value = np.std([10, 15])
        df_mock.quantile.return_value = 15  # Mock quantile values
        
        # Kjør funksjonen for å teste håndtering av NULL-verdier og uteliggere
        df_cleaned = find_outliers_and_handle_missing('mock_file_path.json', ['cloud_cover'])
        
        # Bekrefte at NULL-verdier ble erstattet med gjennomsnitt
        df_mock.loc.assert_called_with([1], 'cloud_cover')  # Forventet oppdatering av den andre raden
        
        # Bekrefte at uteliggere ble håndtert
        df_mock.loc.assert_called_with([1], 'cloud_cover')  # Forventet oppdatering av uteliggere
    
    def test_invalid_file_path(self):
        """
        Test at funksjonen gir en feil når filen ikke finnes.
        """
        with self.assertRaises(FileNotFoundError):
            find_outliers_and_handle_missing('invalid_path.json', ['cloud_cover'])

    @patch('builtins.open')
    def test_invalid_json_format(self, mock_open):
        """
        Test at funksjonen gir en feil ved ugyldig JSON-format.
        """
        mock_open.return_value.__enter__.return_value.read.return_value = '{invalid_json}'
        
        with self.assertRaises(json.JSONDecodeError):
            find_outliers_and_handle_missing('mock_file_path.json', ['cloud_cover'])


class TestSaveToJson(unittest.TestCase):

    @patch('builtins.open', new_callable=MagicMock)
    def test_save_to_json(self, mock_open):
        """
        Test at DataFrame lagres til en JSON-fil.
        """
        mock_data = [
            {'cloud_cover': 10, 'sunshine': 20, 'global_radiation': 30},
            {'cloud_cover': 15, 'sunshine': 25, 'global_radiation': 40},
        ]
        
        df_mock = pd.DataFrame(mock_data)
        
        # Kjør funksjonen for å lagre til JSON
        save_to_json(df_mock, 'mock_output.json')
        
        # Bekreft at json.dump ble kalt for å lagre DataFrame
        mock_open.assert_called_with('mock_output.json', 'w')
        mock_open.return_value.write.assert_called_once()


if __name__ == '__main__':
    unittest.main()
