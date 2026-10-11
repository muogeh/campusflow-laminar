import unittest

from campusflow.tickets import calculate_priority


class TestPriority(unittest.TestCase):
    def test_high_urgency_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_few_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_urgency_four_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 4), "medium")

    def test_low_urgency_one_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

    def test_high_urgency_ten_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 10), "critical")


if __name__ == "__main__":
    unittest.main()