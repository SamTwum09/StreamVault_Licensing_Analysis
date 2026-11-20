"""
Unit Tests for StreamVault Licensing Analysis.
Validates core helpers, data transformations, and reconciliation math using Python standard unittest.
"""

import sys
import unittest
from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "src"))

from utils import coerce_boolean_franchise


class TestBasics(unittest.TestCase):

    def test_coerce_boolean_franchise(self):
        """Test coerce_boolean_franchise accurately converts various truthy and falsy representations."""
        test_series = pd.Series([True, False, "True", "false", "1", "0", "TRUE", "unknown"])
        result = coerce_boolean_franchise(test_series)
        expected = pd.Series([True, False, True, False, True, False, True, False])
        pd.testing.assert_series_equal(result, expected)

    def test_no_duplicate_film_ids_after_transform(self):
        """Verify that there are no duplicate movie_ids in the transformed films dataset."""
        films_path = PROJECT_ROOT / "data" / "processed" / "films.csv"
        self.assertTrue(films_path.exists(), "films.csv does not exist. Run pipeline or transformation first.")
        films = pd.read_csv(films_path)
        self.assertTrue(films["movie_id"].is_unique, "Duplicate movie_ids found in films.csv")

    def test_reconciliation_rows_add_up_to_candidate_list_size(self):
        """Verify that the rows in the reconciliation report equal the total candidate source rows."""
        candidates_path = PROJECT_ROOT / "data" / "id_list.csv"
        reconciliation_path = PROJECT_ROOT / "outputs" / "reconciliation" / "acquisition_reconciliation.csv"

        self.assertTrue(candidates_path.exists(), "id_list.csv missing.")
        self.assertTrue(reconciliation_path.exists(), "acquisition_reconciliation.csv missing.")

        candidates = pd.read_csv(
            candidates_path,
            keep_default_na=False,
            skip_blank_lines=False
        )
        reconciliation = pd.read_csv(reconciliation_path)

        self.assertEqual(
            len(reconciliation),
            len(candidates),
            f"Reconciliation count ({len(reconciliation)}) does not match candidate source rows ({len(candidates)})"
        )


if __name__ == "__main__":
    unittest.main()
