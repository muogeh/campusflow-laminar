import unittest

from campusflow.workflow import (
    assign_ticket,
    update_status,
    get_work_queue,
)


def make_ticket(
    ticket_id="T001",
    priority="medium",
    status="open",
    assigned_to=None,
):
    return {
        "id": ticket_id,
        "title": "Example issue",
        "category": "Software",
        "urgency": "medium",
        "affected_users": 3,
        "priority": priority,
        "status": status,
        "assigned_to": assigned_to,
    }


class TestTicketAssignment(unittest.TestCase):

    def test_assign_ticket(self):
        ticket = make_ticket()
        result = assign_ticket([ticket], "T001", "Ada")

        self.assertEqual(result["assigned_to"], "Ada")

    def test_blank_staff_name_is_rejected(self):
        ticket = make_ticket()

        with self.assertRaises(ValueError):
            assign_ticket([ticket], "T001", "  ")

        self.assertIsNone(ticket["assigned_to"])

    def test_unknown_ticket_is_rejected(self):
        with self.assertRaises(ValueError):
            assign_ticket([], "T999", "Ada")


class TestTicketWorkflow(unittest.TestCase):

    def test_unassigned_ticket_cannot_start(self):
        ticket = make_ticket()

        with self.assertRaises(ValueError):
            update_status([ticket], "T001", "in_progress")

        self.assertEqual(ticket["status"], "open")

    def test_assigned_ticket_completes_workflow(self):
        ticket = make_ticket(assigned_to="Ada")

        update_status([ticket], "T001", "in_progress")
        self.assertEqual(ticket["status"], "in_progress")

        update_status([ticket], "T001", "resolved")
        self.assertEqual(ticket["status"], "resolved")

    def test_resolved_ticket_must_be_reopened(self):
        ticket = make_ticket(
            status="resolved",
            assigned_to="Ada",
        )

        with self.assertRaises(ValueError):
            update_status([ticket], "T001", "in_progress")

        update_status([ticket], "T001", "open")
        self.assertEqual(ticket["status"], "open")

    def test_invalid_transition_does_not_change_status(self):
        ticket = make_ticket(assigned_to="Ada")

        with self.assertRaises(ValueError):
            update_status([ticket], "T001", "resolved")

        self.assertEqual(ticket["status"], "open")


class TestWorkQueue(unittest.TestCase):

    def test_queue_orders_priority_then_numeric_id(self):
        tickets = [
            make_ticket("T010", "high"),
            make_ticket("T002", "critical"),
            make_ticket("T001", "high"),
            make_ticket("T003", "low"),
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T001", "T010", "T003"],
        )

    def test_resolved_tickets_are_excluded(self):
        tickets = [
            make_ticket("T001", "critical", "resolved"),
            make_ticket("T002", "low", "open"),
        ]

        queue = get_work_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002"],
        )


if __name__ == "__main__":
    unittest.main()