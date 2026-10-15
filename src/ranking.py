"""Ranking of open issues for the triage dashboard."""


def rank_open_issues(issues, limit):
    """Return up to `limit` open issue ids for triage.

    Issues are ordered by priority (high, medium, low), then by
    ascending ID. The input collection is never modified.
    """
    if limit <= 0:
        return []

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    candidates = [
        issue for issue in issues
        if issue["status"] == "open"
    ]

    ranked = sorted(
        candidates,
        key=lambda issue: (
            priority_order.get(issue["priority"], len(priority_order)),
            issue["id"],
        ),
    )

    return [issue["id"] for issue in ranked[:limit]]