from itertools import count


_ticket_numbers = count(1)

_VALID_CATEGORIES = {
    "network": "Network",
    "hardware": "Hardware",
    "software": "Software",
    "other": "Other",
}

_VALID_URGENCIES = {"low", "medium", "high"}


def calculate_priority(urgency, affected_users):
    urgency = urgency.strip().lower()

    if urgency == "high" and affected_users >= 10:
        return "critical"

    if urgency == "high" or affected_users >= 10:
        return "high"

    if urgency == "medium" or affected_users >= 3:
        return "medium"

    return "low"


def create_ticket(title, category, urgency, affected_users):
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Title must not be blank.")

    if not isinstance(category, str):
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    category_key = category.strip().lower()

    if category_key not in _VALID_CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")

    urgency_value = urgency.strip().lower()

    if urgency_value not in _VALID_URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")

    if type(affected_users) is not int or affected_users <= 0:
        raise ValueError("Affected users must be a positive whole number.")

    priority = calculate_priority(urgency_value, affected_users)
    ticket_id = f"T{next(_ticket_numbers):03d}"

    return {
            "id": ticket_id,
            "title": title.strip(),
            "category": _VALID_CATEGORIES[category_key],
            "urgency": urgency_value,
            "affected_users": affected_users,
            "priority": priority,
            "status": "open",
            "assigned_to": None,
        }