import unittest

from campusflow.tickets import calculate_priority, create_ticket


class TestPriority(unittest.TestCase):
    def test_priority_rules(self):
        cases = [
            ("high", 12, "critical"),
            ("high", 10, "critical"),
            ("high", 9, "high"),
            ("high", 2, "high"),
            ("low", 10, "high"),
            ("medium", 10, "high"),
            ("medium", 1, "medium"),
            ("low", 4, "medium"),
            ("low", 3, "medium"),
            ("low", 2, "low"),
            ("low", 1, "low"),
            ("HIGH", 10, "critical"),
        ]

        for urgency, affected_users, expected in cases:
            with self.subTest(
                urgency=urgency,
                affected_users=affected_users,
            ):
                self.assertEqual(
                    calculate_priority(urgency, affected_users),
                    expected,
                )


class TestTicketCreation(unittest.TestCase):
    def test_create_ticket_with_valid_data(self):
        ticket = create_ticket("Wi-Fi unavailable", "Network", "high", 12)

    def test_create_ticket_with_valid_data(self):
        ticket = create_ticket("Wi-Fi unavailable", "Network", "high", 12)

        self.assertEqual(ticket["title"], "Wi-Fi unavailable")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 12)
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])
        self.assertRegex(ticket["id"], r"^T\d{3,}$")

    def test_ids_are_automatic_unique_and_sequential(self):
        tickets = [
            create_ticket("First issue", "Network", "low", 1),
            create_ticket("Second issue", "Hardware", "low", 1),
            create_ticket("Third issue", "Software", "low", 1),
        ]

        ids = [ticket["id"] for ticket in tickets]
        numbers = [int(ticket_id[1:]) for ticket_id in ids]

        self.assertEqual(len(set(ids)), 3)
        self.assertEqual(
            numbers,
            [numbers[0], numbers[0] + 1, numbers[0] + 2],
        )

        for ticket_id, number in zip(ids, numbers):
            self.assertEqual(ticket_id, f"T{number:03d}")

    def test_reject_blank_titles(self):
        for title in ["", " ", "\t\n"]:
            with self.subTest(title=title):
                with self.assertRaises(ValueError):
                    create_ticket(title, "Network", "low", 1)

    def test_reject_invalid_affected_users(self):
        for affected_users in [0, -1, 1.5, 2.0, "3", "text", True, None]:
            with self.subTest(affected_users=affected_users):
                with self.assertRaises(ValueError):
                    create_ticket(
                        "Example issue",
                        "Network",
                        "low",
                        affected_users,
                    )

    def test_accept_all_valid_categories(self):
        for category in ["Network", "Hardware", "Software", "Other"]:
            with self.subTest(category=category):
                ticket = create_ticket("Example issue", category, "low", 1)
                self.assertEqual(ticket["category"], category)

    def test_reject_invalid_categories(self):
        for category in ["Invalid", "", " ", None, 123]:
            with self.subTest(category=category):
                with self.assertRaises(ValueError):
                    create_ticket("Example issue", category, "low", 1)

    def test_accept_all_valid_urgencies(self):
        expected_priorities = {
            "low": "low",
            "medium": "medium",
            "high": "high",
        }

        for urgency, expected in expected_priorities.items():
            with self.subTest(urgency=urgency):
                ticket = create_ticket("Example issue", "Network", urgency, 1)
                self.assertEqual(ticket["urgency"], urgency)
                self.assertEqual(ticket["priority"], expected)

    def test_reject_invalid_urgencies(self):
        for urgency in ["urgent", "critical", "", " ", None, 123]:
            with self.subTest(urgency=urgency):
                with self.assertRaises(ValueError):
                    create_ticket("Example issue", "Network", urgency, 1)

    def test_accept_case_variations(self):
        cases = [
            ("network", "HIGH", "Network", "high"),
            ("HARDWARE", "Medium", "Hardware", "medium"),
            ("sOfTwArE", "LOW", "Software", "low"),
            ("OTHER", "hIgH", "Other", "high"),
        ]

        for category, urgency, expected_category, expected_urgency in cases:
            with self.subTest(category=category, urgency=urgency):
                ticket = create_ticket("Example issue", category, urgency, 1)
                self.assertEqual(ticket["category"], expected_category)
                self.assertEqual(ticket["urgency"], expected_urgency)

    def test_ticket_priority_matches_rules(self):
        cases = [
            ("high", 10, "critical"),
            ("high", 1, "high"),
            ("low", 10, "high"),
            ("medium", 10, "high"),
            ("medium", 1, "medium"),
            ("low", 3, "medium"),
            ("low", 1, "low"),
        ]

        for urgency, affected_users, expected in cases:
            with self.subTest(
                urgency=urgency,
                affected_users=affected_users,
            ):
                ticket = create_ticket(
                    "Example issue",
                    "Network",
                    urgency,
                    affected_users,
                )
                self.assertEqual(ticket["priority"], expected)

    def test_invalid_ticket_does_not_consume_id(self):
        first = create_ticket("First issue", "Network", "low", 1)

        with self.assertRaises(ValueError):
            create_ticket("", "Network", "low", 1)

        second = create_ticket("Second issue", "Network", "low", 1)

        self.assertEqual(
            int(second["id"][1:]),
            int(first["id"][1:]) + 1,
        )


if __name__ == "__main__":
    unittest.main()