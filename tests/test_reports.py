import unittest

from campusflow.reports import generate_report


class TestReports(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {"id": "T001", "status": "open", "priority": "critical"},
            {"id": "T002", "status": "in_progress", "priority": "high"},
            {"id": "T003", "status": "resolved", "priority": "medium"},
            {"id": "T004", "status": "open", "priority": "low"},
        ]

    def test_total(self):
        self.assertEqual(generate_report(self.tickets)["total"], 4)

    def test_status_breakdown(self):
        self.assertEqual(
            generate_report(self.tickets)["by_status"],
            {"open": 2, "in_progress": 1, "resolved": 1},
        )

    def test_priority_breakdown(self):
        self.assertEqual(
            generate_report(self.tickets)["by_priority"],
            {"critical": 1, "high": 1, "medium": 1, "low": 1},
        )

    def test_empty_report(self):
        report = generate_report([])
        self.assertEqual(report["total"], 0)
        self.assertTrue(all(v == 0 for v in report["by_status"].values()))
        self.assertTrue(all(v == 0 for v in report["by_priority"].values()))

    def test_invalid_status(self):
        with self.assertRaises(ValueError):
            generate_report([
                {"id": "T001", "status": "waiting", "priority": "low"}
            ])

    def test_invalid_priority(self):
        with self.assertRaises(ValueError):
            generate_report([
                {"id": "T001", "status": "open", "priority": "urgent"}
            ])


if __name__ == "__main__":
    unittest.main()
