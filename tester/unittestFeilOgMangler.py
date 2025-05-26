import unittest
import pandas as pd
import numpy as np
import sys
import os

# Legg til src-mappen i sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Importér funksjonen du tester – oppdater filnavn ved behov
from FeilOgMangler import handle_missing_data  # <-- Endre dette til riktig modulnavn om nødvendig

class TestHandleMissingData(unittest.TestCase):
    """
    Tester funksjonen handle_missing_data for ulike strategier for å fylle inn manglende verdier.
    """

    def setUp(self):
        """Setter opp en test-DataFrame med både numeriske og ikke-numeriske kolonner."""
        self.df = pd.DataFrame({
            'temp': [10, np.nan, 12, np.nan, 14],
            'city': ['A', 'B', 'C', 'D', 'E']
        })

    def test_mean_interpolation(self):
        """Tester lineær interpolasjon ('mean')."""
        result = handle_missing_data(self.df.copy(), method='mean')
        self.assertFalse(result['temp'].isnull().any(), "Det finnes fortsatt NaN etter 'mean'-metode.")

    def test_median_fill(self):
        """Tester at median-verdien brukes ved 'median'-metode."""
        result = handle_missing_data(self.df.copy(), method='median')
        median = self.df['temp'].median()
        # Test at minst én NaN er erstattet med median
        self.assertIn(median, result['temp'].values, "Medianverdi ble ikke brukt ved fylling.")

    def test_forward_fill(self):
        """Tester at forward fill (ffill) fungerer korrekt."""
        result = handle_missing_data(self.df.copy(), method='ffill')
        self.assertEqual(result['temp'].iloc[1], 10, "Forward fill fylte ikke ut riktig verdi.")

    def test_backward_fill(self):
        """Tester at backward fill (bfill) fungerer korrekt."""
        result = handle_missing_data(self.df.copy(), method='bfill')
        self.assertEqual(result['temp'].iloc[1], 12, "Backward fill fylte ikke ut riktig verdi.")

    def test_invalid_method_raises(self):
        """Tester at en ugyldig metode gir ValueError."""
        with self.assertRaises(ValueError):
            handle_missing_data(self.df.copy(), method='feilMetode')

    def test_non_numeric_unchanged(self):
        """Tester at ikke-numeriske kolonner ikke endres når numeric_only=True."""
        result = handle_missing_data(self.df.copy(), method='mean', numeric_only=True)
        self.assertTrue(result['city'].equals(self.df['city']), "Ikke-numeriske kolonner skal ikke endres.")

if __name__ == '__main__':
    unittest.main()
