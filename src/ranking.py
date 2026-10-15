"""Ranking of open issues for the triage dashboard."""


def rank_open_issues(issues, limit):
    """Return up to `limit` issue ids for triage.

    Intended behavior: consider only issues whose status is exactly "open",
    order by priority (high, then medium, then low) and by ascending id
    within the same priority. A limit of 0 yields an empty list. The input
    collection must not be modified.

    Each issue is a dict with keys: id, status, priority.
    """
    # FIX: A limit of 0 yields an empty list.
    if limit <= 0:
        return []

    # FIX: Consider only issues whose status is exactly "open".
    # This also naturally avoids modifying the input collection by creating a new list.
    candidates = [i for i in issues if i["status"] == "open"]

    # Map priorities to numeric values to enforce correct sorting order.
    priority_rank = {"high": 1, "medium": 2, "low": 3}

    # FIX: Use sorted() to not modify input. Sort by mapped priority, then ascending ID.
    sorted_candidates = sorted(
        candidates, 
        key=lambda i: (priority_rank.get(i["priority"], 4), i["id"])
    )

    return [i["id"] for i in sorted_candidates[:limit]]
