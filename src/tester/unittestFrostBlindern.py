import unittest
from unittest.mock import patch, MagicMock
import json
import os
import sys
from requests.exceptions import RequestException

# Legg til src-mappen i import-søkestien
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'python')))
import FrostBlindern

class TestFrostAPI(unittest.TestCase):
    """
    Tester hent_og_lagre_data fra FrostBlindern:
    - Mocker API-kall
    - Skriver til test_observations_data.json
    - Sletter kun testfilen etterpå
    """

    def setUp(self):
        self.test_filename = 'test_observations_data.json'
        self.test_file_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..', 'data', self.test_filename)
        )
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def tearDown(self):
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    @patch('requests.get')
    @patch.dict(os.environ, {"API_KEY_FROST": "fake_key"})
    def test_api_success_and_file_write(self, mock_get):
        """Tester at API-kall lykkes og testfil skrives korrekt."""
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

        # ✅ Her gir vi testfilen som output path
        result = FrostBlindern.hent_og_lagre_data(output_path=self.test_file_path)

        self.assertTrue(os.path.exists(self.test_file_path), "❌ Testfilen ble ikke opprettet.")

        with open(self.test_file_path, 'r') as f:
            saved_data = json.load(f)

        self.assertEqual(saved_data, fake_response, "❌ Innholdet i testfilen er ikke som forventet.")


    @patch('requests.get')
    @patch.dict(os.environ, {"API_KEY_FROST": "fake_key"})
    def test_api_failure_raises(self, mock_get):
        """Tester at API-feil håndteres riktig og kaster ConnectionError."""
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_resp.raise_for_status.side_effect = RequestException("Fake API-feil")
        mock_get.return_value = mock_resp

        with self.assertRaises(ConnectionError):
            FrostBlindern.hent_og_lagre_data()

if __name__ == '__main__':
    unittest.main(verbosity=2)
