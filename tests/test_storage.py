import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from campusflow.storage import StorageError, load_tickets, save_tickets
from campusflow.tickets import create_ticket, initialise_ticket_numbers


class TestStorage(unittest.TestCase):
    def setUp(self):
        self.temp_directory = TemporaryDirectory()
        self.addCleanup(self.temp_directory.cleanup)
        self.path = Path(self.temp_directory.name) / "data" / "tickets.json"

        initialise_ticket_numbers([])
        self.addCleanup(initialise_ticket_numbers, [])

    def test_save_and_reload_keeps_tickets(self):
        tickets = [
            create_ticket("Wi-Fi unavailable", "Network", "high", 12),
            create_ticket("Broken keyboard", "Hardware", "low", 1),
        ]

        save_tickets(tickets, self.path)
        loaded = load_tickets(self.path)

        self.assertEqual(loaded, tickets)

    def test_missing_file_returns_empty_list(self):
        self.assertEqual(load_tickets(self.path), [])
        self.assertFalse(self.path.exists())

    def test_new_ticket_after_reload_has_next_id(self):
        tickets = [
            create_ticket("First issue", "Network", "low", 1),
            create_ticket("Second issue", "Hardware", "low", 1),
            create_ticket("Third issue", "Software", "low", 1),
        ]
        save_tickets(tickets, self.path)

        # Simulate the counter restarting when the program starts again.
        initialise_ticket_numbers([])
        loaded = load_tickets(self.path)
        new_ticket = create_ticket("Fourth issue", "Other", "low", 1)

        self.assertEqual(new_ticket["id"], "T004")
        self.assertNotIn(
            new_ticket["id"],
            [ticket["id"] for ticket in loaded],
        )

    def test_reload_uses_highest_id_not_ticket_count(self):
        ticket = create_ticket("Existing issue", "Network", "low", 1)
        ticket["id"] = "T010"
        save_tickets([ticket], self.path)

        initialise_ticket_numbers([])
        load_tickets(self.path)
        new_ticket = create_ticket("New issue", "Other", "low", 1)

        self.assertEqual(new_ticket["id"], "T011")

    def test_malformed_json_raises_error_and_keeps_file(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        original = '{"broken":'
        self.path.write_text(original, encoding="utf-8")

        with self.assertRaisesRegex(StorageError, "invalid JSON"):
            load_tickets(self.path)

        self.assertEqual(
            self.path.read_text(encoding="utf-8"),
            original,
        )

    def test_duplicate_saved_ids_are_rejected(self):
        tickets = [
            create_ticket("First issue", "Network", "low", 1),
            create_ticket("Second issue", "Hardware", "low", 1),
        ]
        tickets[1]["id"] = tickets[0]["id"]
        save_tickets(tickets, self.path)
        original = self.path.read_text(encoding="utf-8")

        with self.assertRaisesRegex(StorageError, "duplicate IDs"):
            load_tickets(self.path)

        self.assertEqual(
            self.path.read_text(encoding="utf-8"),
            original,
        )


if __name__ == "__main__":
    unittest.main()