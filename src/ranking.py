"""Ranking of open issues for the triage dashboard."""


def rank_open_issues(issues, limit):
    """Return issue ids ranked by priority and then by id."""

    priority_order = {"high": 1, "medium": 2, "low": 3}

    # Keep only open issues without changing the original list.
    candidates = [issue for issue in issues if issue["status"] == "open"]

    # Sort by priority first, then by ascending issue id.
    candidates.sort(
        key=lambda issue: (
            priority_order.get(issue["priority"], 4),
            issue["id"],
        )
    )

    # A limit of 0 or less returns an empty list.
    if limit <= 0:
        return []

    return [issue["id"] for issue in candidates[:limit]] 

