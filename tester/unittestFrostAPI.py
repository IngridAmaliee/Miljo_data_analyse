# kode som tester:
# at API-kallene fungerer (ved bruka av mock)
# suksess og failure
# verifisering av filskriving 
# ryyder opp --> fjerner testfilen

import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys

# Legg til src-mappen i import-søkestien
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
import dataSettApi

class TestFrostAPI(unittest.TestCase):

    @patch('requests.get')
    @patch.dict(os.environ, {"API_KEY_FROST": "fake_key"})
    def test_api_success(self, mock_get):
        """Tester at API-kall returnerer gyldig respons og lagrer JSON-filen"""

        fake_response = {
            "data": [
                {
                    "referenceTime": "2010-01-01T00:00:00Z",
                    "sourceId": "SN18700",
                    "observations": [{"value": 1.2, "unit": "degC"}]
                }
            ]
        }

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = fake_response
        mock_get.return_value = mock_resp

        result = dataSettApi.hent_og_lagre_data()

        expected_file = 'data/observations_data.json'
        self.assertTrue(os.path.exists(expected_file))

        with open(expected_file, 'r') as f:
            saved_data = json.load(f)
            self.assertEqual(saved_data, fake_response)

        os.remove(expected_file)

    @patch('requests.get')
    @patch.dict(os.environ, {"API_KEY_FROST": "fake_key"})
    def test_api_failure(self, mock_get):
        mock_resp = MagicMock()
        mock_resp.status_code = 401
        mock_resp.json.return_value = {
            "error": {"message": "Unauthorized", "reason": "Invalid API key"}
        }
        mock_get.return_value = mock_resp

        with self.assertRaises(SystemExit) as cm:
            dataSettApi.hent_og_lagre_data()

        self.assertEqual(cm.exception.code, 1)

if __name__ == '__main__':
    unittest.main()
