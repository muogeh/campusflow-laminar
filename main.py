from campusflow.storage import StorageError, load_tickets, save_tickets
from campusflow.tickets import create_ticket


def add_ticket(tickets):
    title = input("Title: ")
    category = input("Category (Network, Hardware, Software, Other): ")
    urgency = input("Urgency (low, medium, high): ")

    try:
        affected_users = int(input("Number of affected users: "))
    except ValueError:
        print("Affected users must be a positive whole number.")
        return

    try:
        ticket = create_ticket(title, category, urgency, affected_users)
    except ValueError as error:
        print(f"Cannot create ticket: {error}")
        return

    tickets.append(ticket)
    print(
        f"Created {ticket['id']} with priority {ticket['priority']}. "
        "Choose Save or Exit to save your changes."
    )


def display_tickets(tickets):
    if not tickets:
        print("No tickets yet.")
        return

    for ticket in tickets:
        print(
            f"{ticket['id']} | {ticket['title']} | "
            f"Category: {ticket['category']} | "
            f"Priority: {ticket['priority']} | "
            f"Status: {ticket['status']} | "
            f"Assigned to: {ticket['assigned_to']}"
        )


def save_changes(tickets):
    try:
        save_tickets(tickets)
    except OSError as error:
        print(f"Could not save tickets: {error}")
        return False

    print("Tickets saved to data/tickets.json.")
    return True


def main():
    try:
        tickets = load_tickets()
    except (StorageError, OSError) as error:
        print(f"Startup error: {error}")
        print(
            "The menu will not start, to avoid overwriting "
            "data that could not be loaded."
        )
        return

    print(f"CampusFlow: loaded {len(tickets)} ticket(s).")

    while True:
        print("\nCampusFlow menu")
        print("1. Create ticket")
        print("2. List tickets")
        print("3. Save tickets")
        print("0. Save and Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_ticket(tickets)
        elif choice == "2":
            display_tickets(tickets)
        elif choice == "3":
            save_changes(tickets)
        elif choice == "0":
            if save_changes(tickets):
                print("Goodbye!")
                break
            print("Exit cancelled because saving failed. Please try again.")
        else:
            print("Invalid option. Choose 1, 2, 3, or 0.")


if __name__ == "__main__":
    main()