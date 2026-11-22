import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from synthetic_trial_metrics import Subject, summarize


class TrialMetricsTests(unittest.TestCase):
    def test_grouping(self):
        data = [Subject("a", "A", "enrolled"), Subject("b", "A", "screened"),
                Subject("c", "B", "enrolled")]
        self.assertEqual(summarize(data)["A"], {"enrolled": 1, "screened": 1})
        self.assertEqual(summarize(data)["B"], {"enrolled": 1})

    def test_empty(self):
        self.assertEqual(summarize([]), {})


if __name__ == "__main__":
    unittest.main()
