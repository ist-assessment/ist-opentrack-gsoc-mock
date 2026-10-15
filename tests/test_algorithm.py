import unittest
from src.algorithms import first_unique_index
from src.algorithms import merge_intervals

from src.issue_service import IssueNotFound, IssueService
from src.validators import ValidationError

class TestFirstUniqueIndex(unittest.TestCase):
    def test_case_sensitive_characters(self):
        self.assertEqual(first_unique_index("aA"), 0)


class TestFirstMergeIntervals(unittest.TestCase):
    def test_unsorted_intervals(self):
        self.assertEqual(merge_intervals([[3, 4], [1, 2]]), [[1, 2], [3, 4]])

    def test_touching_intervals(self):
        self.assertEqual(merge_intervals([[1, 2], [2, 3]]), [[1, 3]])

    def test_negative_intervals(self):
        self.assertEqual(merge_intervals([[-3, -1], [-2, 0]]), [[-3, 0]])

    def test_zero_length_intervals(self):
        self.assertEqual(merge_intervals([[2, 2]]), [[2, 2]])

    def test_duplicate_intervals(self):
        self.assertEqual(merge_intervals([[1, 3], [1, 3]]), [[1, 3]])

    def test_empty_intervals(self):
        self.assertEqual(merge_intervals([]), [])

    class TestIssueUpdates(unittest.TestCase):
    def setUp(self):
    self.issue_service = IssueService(MemoryStorage())

    def test_partial_update(self):
        # Create an issue
        issue = self.issue_service.create({
            "title": "Test Issue",
            "priority": "high",
            "status": "open"
        })
        issue_id = issue["id"]

        # Update only its status to "closed"
        updated_issue = self.issue_service.update(issue_id, {"status": "closed"})

        # Check that its original title and priority remain unchanged
        self.assertEqual(updated_issue["title"], "Test Issue")
        self.assertEqual(updated_issue["priority"], "high")
        self.assertEqual(updated_issue["status"], "closed")

    def test_invalid_status(self):
        # Create an issue
        issue = self.issue_service.create({
            "title": "Test Issue",
            "priority": "high",
            "status": "open"
        })
        issue_id = issue["id"]

        # Try updating the status to "wrong" and assert that validators.ValidationError is raised
        with self.assertRaises(ValidationError):
            self.issue_service.update(issue_id, {"status": "wrong"})

    def test_unknown_field(self):
        # Create an issue
        issue = self.issue_service.create({
            "title": "Test Issue",
            "priority": "high",
            "status": "open"
        })
        issue_id = issue["id"]

        # Try updating a field such as "colour" and assert that validators.ValidationError is raised
        with self.assertRaises(ValidationError):
            self.issue_service.update(issue_id, {"colour": "blue"})