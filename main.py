"""CampusFlow: a command-line helpdesk ticket manager.

Run from the top project folder with:  python main.py

This file is the ONLY place that uses input() and print().
All the real work is done by functions in the campusflow/ package.
"""

from campusflow.tickets import create_ticket, initialise_ticket_numbers
from campusflow.storage import load_tickets, save_tickets
#from campusflow.workflow import assign_ticket, change_status, reopen_ticket
#from campusflow.reports import get_work_queue, build_report


def print_ticket(ticket):
    """Show one ticket in a readable way."""
    print("ID:", ticket["id"])
    print("Title:", ticket["title"])
    print("Category:", ticket["category"])
    print("Urgency:", ticket["urgency"])
    print("Affected users:", ticket["affected_users"])
    print("Priority:", ticket["priority"])
    print("Status:", ticket["status"])
    print("Assigned to:", ticket["assigned_to"])
    print()


def ask_ticket_id():
    """Ask for a ticket ID and tidy it up, so 't001' becomes 'T001'."""
    return input("Enter ticket ID (for example T001): ").strip().upper()


def handle_create(tickets):
    print("\n--- CREATE TICKET ---")
    title = input("Title: ")
    category = input("Category (Network, Hardware, Software, Other): ")
    urgency = input("Urgency (low, medium, high): ")
    affected_users_text = input("Number of affected users: ")

    try:
        affected_users = int(affected_users_text)
    except ValueError:
        raise ValueError("Affected users must be a positive whole number.")

    ticket = create_ticket(title, category, urgency, affected_users)
    tickets.append(ticket)
    save_tickets(tickets)

    print("Ticket created successfully!")
    print_ticket(ticket)


def handle_list(tickets):
    print("\n--- ALL TICKETS ---")

    if not tickets:
        print("No tickets yet.")
        return

    for ticket in tickets:
        print_ticket(ticket)


def handle_view(tickets):
    print("\n--- VIEW ONE TICKET ---")
    ticket_id = ask_ticket_id()

    for ticket in tickets:
        if ticket["id"] == ticket_id:
            print_ticket(ticket)
            return

    print("Ticket not found:", ticket_id)


def handle_assign(tickets):
    print("\n--- ASSIGN TICKET ---")
    ticket_id = ask_ticket_id()
    staff_name = input("Staff member name: ")

    ticket = assign_ticket(tickets, ticket_id, staff_name)
    save_tickets(tickets)

    print("Ticket assigned successfully!")
    print_ticket(ticket)


def handle_change_status(tickets):
    print("\n--- CHANGE STATUS ---")
    ticket_id = ask_ticket_id()
    new_status = input("New status (in_progress, resolved): ").strip().lower()

    ticket = change_status(tickets, ticket_id, new_status)
    save_tickets(tickets)

    print("Status updated successfully!")
    print_ticket(ticket)


def handle_reopen(tickets):
    print("\n--- REOPEN TICKET ---")
    ticket_id = ask_ticket_id()

    ticket = reopen_ticket(tickets, ticket_id)
    save_tickets(tickets)

    print("Ticket reopened successfully!")
    print_ticket(ticket)


def handle_queue(tickets):
    print("\n--- WORK QUEUE (most urgent first) ---")
    queue = get_work_queue(tickets)

    if not queue:
        print("The queue is empty.")
        return

    for number, ticket in enumerate(queue, start=1):
        print(number, ".", ticket["id"], "-", ticket["priority"], "-", ticket["title"])


def handle_report(tickets):
    print("\n--- REPORT ---")
    report = build_report(tickets)

    print("Total tickets:", report["total"])

    print("\nBy status:")
    for status, count in report["by_status"].items():
        print(" ", status, ":", count)

    print("\nBy priority:")
    for priority, count in report["by_priority"].items():
        print(" ", priority, ":", count)


def main():
    # Load saved tickets. If the file is damaged, stop WITHOUT saving,
    # so we never erase the user's data by accident.
    try:
        tickets = load_tickets()
        initialise_ticket_numbers(tickets)
    except ValueError as error:
        print("Could not load tickets:", error)
        print("Fix or move data/tickets.json, then run the program again.")
        print("Nothing was changed.")
        return

    while True:
        print("\n===== CAMPUSFLOW HELPDESK =====")
        print("1. Create ticket")
        print("2. List all tickets")
        print("3. View one ticket")
        print("4. Assign ticket")
        print("5. Change ticket status")
        print("6. Reopen resolved ticket")
        print("7. Work queue")
        print("8. Reports")
        print("9. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "9":
            print("Goodbye!")
            break

        try:
            if choice == "1":
                handle_create(tickets)
            elif choice == "2":
                handle_list(tickets)
            elif choice == "3":
                handle_view(tickets)
            elif choice == "4":
                handle_assign(tickets)
            elif choice == "5":
                handle_change_status(tickets)
            elif choice == "6":
                handle_reopen(tickets)
            elif choice == "7":
                handle_queue(tickets)
            elif choice == "8":
                handle_report(tickets)
            else:
                print("Invalid choice. Please enter a number from 1 to 9.")
        except ValueError as error:
            # Bad input from the user: show the message and keep running.
            print("Error:", error)


if __name__ == "__main__":
    main()