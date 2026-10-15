"""Ranking of open issues for the triage dashboard."""


def rank_open_issues(issues, limit):
    """Return up to `limit` issue ids for triage.

    Intended behavior: consider only issues whose status is exactly "open",
    order by priority (high, then medium, then low) and by ascending id
    within the same priority. A limit of 0 yields an empty list. The input
    collection must not be modified.

    Each issue is a dict with keys: id, status, priority.
    """

    # BUG_FIX: Switched from inline .sort() to a non-destructive operation.
    # Modifying the original list reference mutated state variables inside the active issue service.


    priority_weights = {"high": 0, "medium": 1, "low": 2}  # <-- CHANGED

    # BUG_FIX: Introduced explicit weight mapping to rank priority levels correctly (high -> medium -> low).
    # Replaced the negative ID marker to restore ascending tie-breaker order as outlined in the specifications.


    sorted_issues = sorted(  # <-- CHANGED
        
        # BUG_FIX: Isolated matches strictly matching the 'open' criteria.
        # The previous inequality check mistakenly swept in intermediate statuses like 'in_progress'.


        issues,  # <-- CHANGED

        # BUG_FIX: Refactored indexing fallback logic. 
        # A limit parameter value of 0 previously forced a dump of all entries instead of an empty list.


        key=lambda i: (priority_weights.get(i["priority"], 3), i["id"])  # <-- CHANGED
    )  # <-- CHANGED

    candidates = [i for i in sorted_issues if i["status"] == "open"]  # <-- CHANGED

    return [i["id"] for i in candidates[:limit]]  # <-- CHANGED
