import unittest
import pandas as pd
import numpy as np
import sys
import os

# Legg til src-sti hvis funksjonen ligger der
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))
from FeilOgMangler import handle_missing_data  # oppdater filnavn hvis nødvendig

class TestHandleMissingData(unittest.TestCase):
    """
    Tester funksjonen handle_missing_data for ulike strategier for utfylling av manglende verdier.
    """

    def setUp(self):
        # Eksempeldata med manglende verdier
        self.df = pd.DataFrame({
            'temp': [10, np.nan, 12, np.nan, 14],
            'city': ['A', 'B', 'C', 'D', 'E']
        })

    def test_mean_interpolation(self):
        """Tester lineær interpolasjon ('mean')"""
        result = handle_missing_data(self.df.copy(), method='mean')
        self.assertFalse(result['temp'].isnull().any())

    def test_median_fill(self):
        """Tester median-utfylling"""
        result = handle_missing_data(self.df.copy(), method='median')
        median = self.df['temp'].median()
        self.assertTrue((result['temp'] == median).sum() >= 1)

    def test_forward_fill(self):
        """Tester forward fill (ffill)"""
        result = handle_missing_data(self.df.copy(), method='ffill')
        self.assertEqual(result['temp'].iloc[1], 10)

    def test_backward_fill(self):
        """Tester backward fill (bfill)"""
        result = handle_missing_data(self.df.copy(), method='bfill')
        self.assertEqual(result['temp'].iloc[1], 12)

    def test_invalid_method(self):
        """Tester at ugyldig metode kaster ValueError"""
        with self.assertRaises(ValueError):
            handle_missing_data(self.df.copy(), method='ugyldig')

    def test_non_numeric_not_filled(self):
        """Tester at ikke-numeriske kolonner ikke blir fylt når numeric_only=True"""
        result = handle_missing_data(self.df.copy(), method='mean', numeric_only=True)
        self.assertTrue(result['city'].equals(self.df['city']))

if __name__ == '__main__':
    unittest.main()
