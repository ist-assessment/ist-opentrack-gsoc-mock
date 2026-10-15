
"""Tests for issue filtering and title search."""

from src.issue_service import IssueService


class MemoryStorage:
    def __init__(self):
        self.issues = {}

    def load(self):
        return self.issues

    def save(self, issues):
        self.issues = dict(issues)


def make_service():
    service = IssueService(MemoryStorage())

    service.create({
        "title": "Fix Login Bug",
        "priority": "high",
        "status": "open",
    })
    service.create({
        "title": "Update homepage",
        "priority": "low",
        "status": "closed",
    })
    service.create({
        "title": "Improve login security",
        "priority": "high",
        "status": "open",
    })
    service.create({
        "title": "Write documentation",
        "priority": "medium",
        "status": "open",
    })

    return service


def test_find_without_filters_returns_all_in_id_order():
    service = make_service()

    results = service.find()

    assert [issue["id"] for issue in results] == [1, 2, 3, 4]


def test_find_by_status():
    service = make_service()

    results = service.find(status="open")

    assert [issue["id"] for issue in results] == [1, 3, 4]


def test_find_by_priority():
    service = make_service()

    results = service.find(priority="high")

    assert [issue["id"] for issue in results] == [1, 3]


def test_title_search_ignores_case():
    service = make_service()

    results = service.find(title_contains="LOGIN")

    assert [issue["id"] for issue in results] == [1, 3]


def test_filters_work_together():
    service = make_service()

    results = service.find(
        status="open",
        priority="high",
        title_contains="login",
    )

    assert [issue["id"] for issue in results] == [1, 3]


def test_no_matching_results():
    service = make_service()

    assert service.find(title_contains="does not exist") == []


def test_empty_title_search_matches_all():
    service = make_service()

    assert len(service.find(title_contains="")) == 4


def test_find_does_not_change_stored_issues():
    service = make_service()
    original = service.list_all()

    service.find(status="open", priority="high")

    assert service.list_all() == original


def test_changing_result_does_not_change_stored_issue():
    service = make_service()

    results = service.find()
    results[0]["title"] = "Changed title"

    assert service.get(1)["title"] == "Fix Login Bug"