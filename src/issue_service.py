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
            
        issue = self.issues[issue_id]
        
        # FIX: Preserve existing fields instead of overwriting with defaults.
        if "title" in changes:
            issue["title"] = validators.validate_title(changes["title"])
        if "priority" in changes:
            issue["priority"] = validators.validate_priority(changes["priority"])
        if "status" in changes:
            issue["status"] = validators.validate_status(changes["status"])
            
        # FIX: Save the updated issues to storage so changes persist.
        self.storage.save(self.issues)
        
        return dict(issue)

    def delete(self, issue_id):
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")
        del self.issues[issue_id]
        self.storage.save(self.issues)

    def find(self, status=None, priority=None, title_contains=None):
        """Filter issues by status/priority and search titles."""
        results = []
        for issue_id in sorted(self.issues):
            issue = self.issues[issue_id]
            
            # Filter by exact status if provided
            if status is not None and issue.get("status") != status:
                continue
                
            # Filter by exact priority if provided
            if priority is not None and issue.get("priority") != priority:
                continue
                
            # Filter by title substring if provided (case-insensitive search is standard)
            if title_contains is not None and title_contains.lower() not in issue.get("title", "").lower():
                continue
                
            results.append(dict(issue))
            
        return results
