"""Ticket assignment and lifecycle management for CampusFlow."""


def _find_ticket(tickets, ticket_id):
    """Return a ticket by ID or raise an error if it does not exist."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id!r} does not exist.")


def assign_ticket(tickets, ticket_id, staff_name):
    """Assign an existing, unresolved ticket to a staff member."""
    if not isinstance(staff_name, str) or not staff_name.strip():
        raise ValueError("Staff name must not be blank.")

    ticket = _find_ticket(tickets, ticket_id)

    if ticket["status"] == "resolved":
        raise ValueError("Reopen the ticket before modifying it.")

    ticket["assigned_to"] = staff_name.strip()
    return ticket


def update_status(tickets, ticket_id, new_status):
    """Apply an explicitly permitted ticket status transition."""
    if not isinstance(new_status, str):
        raise ValueError("Status must be a string.")

    new_status = new_status.strip().lower()
    allowed_statuses = {"open", "in_progress", "resolved"}

    if new_status not in allowed_statuses:
        raise ValueError(f"Invalid status: {new_status!r}.")

    ticket = _find_ticket(tickets, ticket_id)
    current_status = ticket["status"]

    if current_status == "resolved":
        if new_status != "open":
            raise ValueError(
                "A resolved ticket must be explicitly reopened to open first."
            )

    elif current_status == "open":
        if new_status != "in_progress":
            raise ValueError("An open ticket can only move to in_progress.")

        if not ticket["assigned_to"]:
            raise ValueError(
                "Assign the ticket to a staff member before starting work."
            )

    elif current_status == "in_progress":
        if new_status != "resolved":
            raise ValueError(
                "A ticket in progress can only move to resolved."
            )

    ticket["status"] = new_status
    return ticket


def get_work_queue(tickets):
    """Return unresolved tickets ordered by priority and numeric ticket ID."""
    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    unresolved = [
        ticket for ticket in tickets
        if ticket["status"] != "resolved"
    ]

    def sort_key(ticket):
        ticket_id = ticket["id"]

        if not isinstance(ticket_id, str) or not ticket_id.startswith("T"):
            raise ValueError(f"Invalid ticket ID: {ticket_id!r}.")

        try:
            number = int(ticket_id[1:])
        except ValueError as exc:
            raise ValueError(
                f"Invalid ticket ID: {ticket_id!r}."
            ) from exc

        priority = ticket["priority"]

        if priority not in priority_order:
            raise ValueError(f"Invalid priority: {priority!r}.")

        return priority_order[priority], number

    return sorted(unresolved, key=sort_key)