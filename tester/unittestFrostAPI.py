import unittest
from unittest.mock import patch, MagicMock
import requests
import os
import json
import pandas as pd

# Importer funksjonene fra koden din
from dataSettApi import fetch_and_process_data

class TestFetchAndProcessData(unittest.TestCase):

    @patch('requests.get')
    @patch('os.path.exists')
    @patch('os.makedirs')
    @patch('builtins.open')
    def test_fetch_and_process_data_success(self, mock_open, mock_makedirs, mock_exists, mock_get):
        """
        Test at API-kallet og filprosessen fungerer som forventet når alt går bra.
        """
        # Mocking API responsen
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'data': [
                {
                    'observations': [{'value': 10, 'referenceTime': '2020-01-01', 'sourceId': 'SN18700'}],
                    'referenceTime': '2020-01-01',
                    'sourceId': 'SN18700'
                }
            ]
        }
        
        mock_get.return_value = mock_response
        
        # Mocking os.path.exists for å alltid returnere False (for å simulere at mappen ikke finnes)
        mock_exists.return_value = False
        
        # Mocking open for å simulere at vi kan skrive til en fil
        mock_open.return_value.__enter__.return_value.write = MagicMock()
        
        # Kjør funksjonen
        fetch_and_process_data()
        
        # Sjekk at API-kallet ble gjort med riktig URL og parametre
        mock_get.assert_called_with(
            'https://frost.met.no/observations/v0.jsonld', 
            {'sources': 'SN18700', 'elements': "mean_k(air_temperature P1D)", 'referencetime': '2010-01-01/2020-01-01'},
            auth=('mock_api_key', '')
        )
        
        # Sjekk at mappen 'data' ble opprettet
        mock_makedirs.assert_called_with('data')

        # Sjekk at filen ble skrevet til
        mock_open.assert_called_with('data/observations_data.json', 'w')
        
        # Bekreft at json.dump ble kalt for å lagre data til fil
        mock_open.return_value.__enter__.return_value.write.assert_called_once()

    @patch('requests.get')
    def test_fetch_and_process_data_api_error(self, mock_get):
        """
        Test at API-kallet håndterer feil svar (ikke 200 OK).
        """
        # Mocking en feilsituasjon med API-respons
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {'error': {'message': 'Bad Request', 'reason': 'Invalid parameters'}}
        
        mock_get.return_value = mock_response
        
        # Kjør funksjonen
        fetch_and_process_data()
        
        # Bekreft at feilmeldingen ble skrevet ut
        mock_get.assert_called()
        print_output = "Error! Returned status code 400"
        self.assertIn(print_output, self._get_stdout())

    @patch('requests.get')
    def test_invalid_api_key(self, mock_get):
        """
        Test at funksjonen håndterer manglende eller ugyldig API-nøkkel.
        """
        # Mocking en API-respons med manglende API-nøkkel
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {'error': {'message': 'Unauthorized', 'reason': 'Invalid API key'}}
        
        mock_get.return_value = mock_response
        
        # Kjør funksjonen
        fetch_and_process_data()
        
        # Bekreft at feilmeldingen ble skrevet ut
        mock_get.assert_called()
        print_output = "Error! Returned status code 401"
        self.assertIn(print_output, self._get_stdout())
        
    def _get_stdout(self):
        """ Hjelpefunksjon for å fange opp print-output under testing """
        return self._stdout.getvalue()

if __name__ == '__main__':
    unittest.main()
