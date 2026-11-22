import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "clinical"))
from quality import Enrollment, read_enrollments, site_summary, monthly_consents
from report import create_report


class ClinicalQualityTests(unittest.TestCase):
    def test_site_counts(self):
        records = [Enrollment("X", "A", "enrolled", date(2026, 1, 1)),
                   Enrollment("Y", "A", "screen_failed", date(2026, 2, 1))]
        result = site_summary(records)
        self.assertEqual(result[0]["subjects"], 2)
        self.assertEqual(result[0]["enrollment_fraction"], .5)

    def test_monthly_counts(self):
        records = [Enrollment("X", "A", "enrolled", date(2026, 1, 1)),
                   Enrollment("Y", "A", "enrolled", date(2026, 1, 15))]
        self.assertEqual(monthly_consents(records), [{"month": "2026-01", "consents": 2}])

    def test_invalid_status(self):
        with self.assertRaises(ValueError):
            Enrollment("X", "A", "unknown", date(2026, 1, 1))

    def test_duplicate_subjects(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("subject_id,site_id,status,consent_date\nX,A,enrolled,2026-01-01\nX,B,enrolled,2026-01-02\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                read_enrollments(path)

    def test_report_end_to_end(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.csv"
            path.write_text("subject_id,site_id,status,consent_date\nX,A,enrolled,2026-01-01\n", encoding="utf-8")
            result = create_report(path)
            self.assertEqual(result["subject_count"], 1)
            self.assertEqual(result["site_metrics"][0]["enrolled"], 1)


if __name__ == "__main__":
    unittest.main()
