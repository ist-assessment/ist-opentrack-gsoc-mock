"""Ranking of open issues for the triage dashboard."""


def rank_open_issues(issues, limit):
    """Return issue ids ranked by priority and then by id."""

    priority_order = {"high": 1, "medium": 2, "low": 3}
  
    candidates = [issue for issue in issues if issue["status"] == "open"]

    candidates.sort(
        key=lambda issue: (
            priority_order.get(issue["priority"], 4),
            issue["id"],
        )
    )

    if limit <= 0:
        return []

    return [issue["id"] for issue in candidates[:limit]]
