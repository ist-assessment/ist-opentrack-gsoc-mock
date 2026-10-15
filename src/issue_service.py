"""Core issue management service for OpenTrack."""

from . import validators


class IssueNotFound(KeyError):
    """Raised when an issue id does not exist."""


class IssueService:
    def __init__(self, storage):
        self.storage = storage
        self.issues = self.storage.load()

    def _next_id(self):
        if not self.issues:
            return 1
        return max(self.issues) + 1

    def create(self, data):
        """Create a new issue and return it."""
        normalized = validators.validate_new_issue(data)
        issue_id = self._next_id()
        issue = {"id": issue_id}
        issue.update(normalized)
        self.issues[issue_id] = issue
        self.storage.save(self.issues)
        return dict(issue)

    def get(self, issue_id):
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")
        return dict(self.issues[issue_id])

    def list_all(self):
        return [dict(self.issues[k]) for k in sorted(self.issues)]

    def update(self, issue_id, changes):

        # BUG_FIX: Merged structural update to prevent fallback parameters from wiping out omitted fields.
        # Also added the missing self.storage.save() call to prevent in-memory changes from being lost.


        """Partially update an issue. Only provided fields should change."""
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")
        
        # BUG FIX: Merged structural update to prevent fallback parameters from wiping out omitted fields.
        # Also added the missing self.storage.save() call to prevent in-memory changes from being lost.
        current_issue = self.issues[issue_id]
        updated_data = {
            "title": changes.get("title", current_issue["title"]),
            "priority": changes.get("priority", current_issue["priority"]),
            "status": changes.get("status", current_issue["status"]),
        }
        validated = validators.validate_new_issue(updated_data)
        current_issue.update(validated)
        
        self.storage.save(self.issues)
        return dict(current_issue)


    def delete(self, issue_id):
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")
        del self.issues[issue_id]
        self.storage.save(self.issues)

        def find(self, status=None, priority=None, title_contains=None):
            """Filter issues by status/priority and search titles.

            Not fully implemented yet — see issue tracker.
            """
            results = []  # <-- CHANGED
            for issue in self.issues.values():  # <-- CHANGED
                if status and issue.get("status") != status:  # <-- CHANGED
                    continue  # <-- CHANGED
                if priority and issue.get("priority") != priority:  # <-- CHANGED
                    continue  # <-- CHANGED
                if title_contains and title_contains.lower() not in issue.get("title", "").lower():  # <-- CHANGED
                    continue  # <-- CHANGED
                results.append(dict(issue))  # <-- CHANGED
            
            return results  # <-- CHANGED
