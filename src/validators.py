"""Validation rules for OpenTrack issues."""

VALID_PRIORITIES = ("low", "medium", "high")
VALID_STATUSES = ("open", "in_progress", "closed")

TITLE_MIN = 3
TITLE_MAX = 80


class ValidationError(ValueError):
    """Raised when user-supplied issue data is invalid."""


def validate_title(title):
    if not isinstance(title, str):
        raise ValidationError("title must be a string")

    title = title.strip()

    if not (TITLE_MIN <= len(title) <= TITLE_MAX):
        raise ValidationError(
            f"title must be between {TITLE_MIN} and {TITLE_MAX} characters after trimming"
        )

    return title


def validate_priority(priority):
    if not isinstance(priority, str) or priority not in VALID_PRIORITIES:
        raise ValidationError(f"priority must be one of {VALID_PRIORITIES}")

    return priority


def validate_status(status):
    if not isinstance(status, str) or status not in VALID_STATUSES:
        raise ValidationError(f"status must be one of {VALID_STATUSES}")

    return status


def validate_new_issue(data):
    """Validate issue data and return a normalized dictionary."""
    if not isinstance(data, dict):
        raise ValidationError("issue payload must be a dict")

    title = validate_title(data.get("title"))
    priority = validate_priority(data.get("priority", "medium"))
    status = validate_status(data.get("status", "open"))

    return {
        "title": title,
        "priority": priority,
        "status": status,
    }
