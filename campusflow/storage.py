import json
from pathlib import Path

from campusflow.tickets import initialise_ticket_numbers


DEFAULT_PATH = Path("data/tickets.json")


class StorageError(Exception):
    """Raised when saved ticket data cannot be loaded safely."""


def save_tickets(tickets, path=DEFAULT_PATH):
    path = Path(path)
    contents = json.dumps(tickets, indent=4)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contents, encoding="utf-8")


def load_tickets(path=DEFAULT_PATH):
    path = Path(path)

    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except FileNotFoundError:
        initialise_ticket_numbers([])
        return []
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise StorageError(
            f"Cannot load tickets from {path}: invalid JSON or encoding. "
            "The existing file has not been changed."
        ) from error

    if not isinstance(tickets, list) or any(
        not isinstance(ticket, dict) for ticket in tickets
    ):
        raise StorageError(
            f"Cannot load tickets from {path}: expected a list of ticket objects. "
            "The existing file has not been changed."
        )

    try:
        initialise_ticket_numbers(tickets)
    except ValueError as error:
        raise StorageError(
            f"Cannot load tickets from {path}: {error} "
            "The existing file has not been changed."
        ) from error

    return tickets
