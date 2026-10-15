
"""Core issue management service for OpenTrack."""

from . import validators


class IssueNotFound(KeyError):
    """Raised when an issue id does not exist."""


class IssueService:
    def __init__(self, storage):
        self.storage = storage
        data = self.storage.load()

        if "issues" in data and "next_id" in data:
            self.issues = data["issues"]
            self.next_id = data["next_id"]
        elif "issues" in data:
            self.issues = data["issues"]
            self.next_id = max(self.issues, default=0) + 1
        else:
            self.issues = data
            self.next_id = max(self.issues, default=0) + 1

    def _next_id(self):
        return self.next_id

    def _save(self):
        """Save issues using the storage interface available."""
        if hasattr(self.storage, "save_state"):
            self.storage.save_state(self.issues, self.next_id)
        else:
            self.storage.save(self.issues)

    def create(self, data):
        """Create a new issue and return it."""
        normalized = validators.validate_new_issue(data)

        issue_id = self._next_id()
        issue = {"id": issue_id}
        issue.update(normalized)

        self.issues[issue_id] = issue
        self.next_id += 1
        self._save()

        return dict(issue)

    def get(self, issue_id):
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")
        return dict(self.issues[issue_id])

    def list_all(self):
        return [dict(self.issues[key]) for key in sorted(self.issues)]

    def update(self, issue_id, changes):
        """Partially update an issue while preserving unchanged fields."""
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")

        updated = dict(self.issues[issue_id])
        updated.update(changes)
        updated["id"] = issue_id

        normalized = validators.validate_new_issue({
            "title": updated["title"],
            "priority": updated["priority"],
            "status": updated["status"],
        })

        updated.update(normalized)

        self.issues[issue_id] = updated
        self._save()

        return dict(updated)

    def delete(self, issue_id):
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")

        del self.issues[issue_id]
        self._save()

    def find(self, status=None, priority=None, title_contains=None):
        """Filter issues by status, priority, and title."""
        results = []

        for issue_id in sorted(self.issues):
            issue = self.issues[issue_id]

            if status is not None and issue["status"] != status:
                continue

            if priority is not None and issue["priority"] != priority:
                continue

            if (
                title_contains is not None
                and title_contains.casefold()
                not in issue["title"].casefold()
            ):
                continue

            results.append(dict(issue))

        return results