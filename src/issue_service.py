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
        """Partially update an issue. Only provided fields should change."""
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")
        merged = {"id": issue_id}
        merged.update(validators.validate_new_issue(
            {
                "title": changes.get("title", "untitled issue"),
                "priority": changes.get("priority", "medium"),
                "status": changes.get("status", "open"),
            }
        ))
        self.issues[issue_id] = merged
        return dict(merged)

    def delete(self, issue_id):
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")
        del self.issues[issue_id]
        self.storage.save(self.issues)

    def find(self, status=None, priority=None, title_contains=None):
        """Find issues by status, priority, or title."""
        results = []

        for issue_id in sorted(self.issues):
            issue = self.issues[issue_id]

            if status is not None and issue.get("status") != status:
                continue

            if priority is not None and issue.get("priority") != priority:
                continue

            if title_contains is not None:
                title = issue.get("title", "")

                if title_contains.lower() not in title.lower():
                    continue

            results.append(dict(issue))

        return results
