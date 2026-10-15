"""Ranking of open issues for the triage dashboard."""


def rank_open_issues(issues, limit):
    """Return up to `limit` issue ids for triage.

    Intended behavior: consider only issues whose status is exactly "open",
    order by priority (high, then medium, then low) and by ascending id
    within the same priority. A limit of 0 yields an empty list. The input
    collection must not be modified.

    Each issue is a dict with keys: id, status, priority.
    """
    """issues.sort(key=lambda i: (i["priority"], -i["id"]))
    candidates = [i for i in issues if i["status"] != "closed"]
    if not limit:
        return [i["id"] for i in candidates]
    return [i["id"] for i in candidates[:limit]]"""
#my fix- in list if there are strings it sorts it alphabeticlly, so the default priority wil be hight because of "h
# " then low because after h comes "l" and then "m" for medium, and -i[id] folllows negetive indexting so last id comes first
#but now, i assigned value 0 1 2 for high medium low so now it goes by number as desired priority
#also it says not equal to close, which means in progress with be included, so i fixed it by ristricting it to only work when == open
 priority_order = {"high": 0, "medium": 1, "low": 2}
    issues.sort(key=lambda i: (priority_order[i["priority"]], i["id"]))
    candidates = [i for i in issues if i["status"] == "open"]
    if not limit:
        return [i["id"] for i in candidates]
    return [i["id"] for i in candidates[:limit]]
