"""Functions for listing and viewing CampusFlow tickets."""


def list_tickets(tickets):
    """Return all tickets."""
    return list(tickets)


def get_ticket(tickets, ticket_id):
    """Return a ticket by ID or raise an error."""
    for ticket in tickets:
        if ticket["id"] == ticket_id:
            return ticket

    raise ValueError(f"Ticket {ticket_id!r} does not exist.")