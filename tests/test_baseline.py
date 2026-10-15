"""Public starter tests — baseline behavior that already works.

These are NOT the full assessment tests. They verify the starter project
runs from a fresh clone. Add your own tests as you fix issues.
"""

import unittest

from src.issue_service import IssueNotFound, IssueService
from src.validators import ValidationError
from src.algorithms import first_unique_index


class MemoryStorage:
    """In-memory stand-in for JsonStorage used by the public tests."""

    def __init__(self):
        self.data = {}

    def load(self):
        return dict(self.data)

    def save(self, issues):
        self.data = dict(issues)


class TestBaseline(unittest.TestCase):
    def setUp(self):
        self.service = IssueService(MemoryStorage())

    def test_create_assigns_id_and_defaults(self):
        issue = self.service.create({"title": "First bug"})
        self.assertEqual(issue["id"], 1)
        self.assertEqual(issue["status"], "open")
        self.assertEqual(issue["priority"], "medium")

    def test_ids_increase(self):
        a = self.service.create({"title": "Issue A"})
        b = self.service.create({"title": "Issue B"})
        self.assertEqual((a["id"], b["id"]), (1, 2))

    def test_get_returns_created_issue(self):
        created = self.service.create({"title": "Readable title", "priority": "high"})
        fetched = self.service.get(created["id"])
        self.assertEqual(fetched["title"], "Readable title")
        self.assertEqual(fetched["priority"], "high")

    def test_get_missing_raises(self):
        with self.assertRaises(IssueNotFound):
            self.service.get(42)

    def test_list_sorted_by_id(self):
        for name in ("one", "two", "three"):
            self.service.create({"title": f"issue {name}"})
        ids = [i["id"] for i in self.service.list_all()]
        self.assertEqual(ids, [1, 2, 3])

    def test_invalid_title_rejected(self):
        with self.assertRaises(ValidationError):
            self.service.create({"title": "ab"})

    def test_invalid_priority_rejected(self):
        with self.assertRaises(ValidationError):
            self.service.create({"title": "valid title", "priority": "urgent"})

    def test_delete_removes_issue(self):
        issue = self.service.create({"title": "to be removed"})
        self.service.delete(issue["id"])
        with self.assertRaises(IssueNotFound):
            self.service.get(issue["id"])

    

if __name__ == "__main__":
    unittest.main()
