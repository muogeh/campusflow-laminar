import unittest

from campusflow.ticket_views import list_tickets, get_ticket


class TestTicketViews(unittest.TestCase):
    def setUp(self):
        self.tickets = [
            {
                "id": "T001",
                "title": "Network failure",
                "status": "open",
            },
            {
                "id": "T002",
                "title": "Broken computer",
                "status": "in_progress",
            },
        ]

    def test_list_tickets_returns_all_tickets(self):
        self.assertEqual(list_tickets(self.tickets), self.tickets)

    def test_list_tickets_returns_empty_list(self):
        self.assertEqual(list_tickets([]), [])

    def test_get_ticket_returns_matching_ticket(self):
        ticket = get_ticket(self.tickets, "T002")
        self.assertEqual(ticket["title"], "Broken computer")

    def test_get_ticket_rejects_unknown_id(self):
        with self.assertRaises(ValueError):
            get_ticket(self.tickets, "T999")


if __name__ == "__main__":
    unittest.main()