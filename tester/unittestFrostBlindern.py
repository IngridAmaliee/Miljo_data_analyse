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
import FrostBlindern

class TestFrostAPI(unittest.TestCase):
   
    @patch('requests.get')
    @patch.dict(os.environ, {"API_KEY_FROST": "fake_key"})
    def test_api_success(self, mock_get):
        """Tester at API-kall returnerer gyldig respons og lagrer JSON-filen uten å påvirke produksjonsdata"""

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

        # Midlertidig overstyr filstien i FrostBlindern før kall
        original_path = 'data/observations_data.json'
        test_path = 'data/test_observations_data.json'

        # Patch lagring midlertidig i modulen
        with patch('FrostBlindern.open', create=True) as mock_open:
            real_open = open  # referanse til ekte open-funksjon
            mock_open.side_effect = lambda file, mode='r', *args, **kwargs: real_open(
                test_path if file == original_path else file, mode, *args, **kwargs
            )

            result = FrostBlindern.hent_og_lagre_data()

            # Verifiser at testfilen ble laget med riktig innhold
            self.assertTrue(os.path.exists(test_path))
            with open(test_path, 'r') as f:
                saved_data = json.load(f)
                self.assertEqual(saved_data, fake_response)

            # Rydd opp testfilen
            os.remove(test_path)
