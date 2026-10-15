"""Core issue management service for OpenTrack."""
from . import validators


class IssueNotFound(KeyError):
    """Raised when an issue id does not exist."""


class IssueService:
    def __init__(self, storage):
        self.storage = storage
        # load existing issues into our dictionary
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

        # Get the old issue data from memory
        old_issue_data = self.issues[issue_id]

        # Create a copy and update it with the new incoming changes
        updated_dict = old_issue_data.copy()
        updated_dict.update(changes)

        # Validate the dictionary structure using the validator function
        validated_output = validators.validate_new_issue(updated_dict)

        # Ensure the original issue ID stays intact
        validated_output["id"] = issue_id

        # Save back into local memory dictionary and persist to file storage
        self.issues[issue_id] = validated_output
        self.storage.save(self.issues)

        return validated_output

    def delete(self, issue_id):
        if issue_id not in self.issues:
            raise IssueNotFound(f"no issue with id {issue_id}")
        del self.issues[issue_id]
        self.storage.save(self.issues)

    def find(self, status=None, priority=None, title_contains=None):
        """Filter issues by status/priority and search titles."""
        matched_results = []

        # Look through all keys in order
        all_keys = sorted(self.issues)
        for current_key in all_keys:
            single_issue = self.issues[current_key]

            # Check if status filter is applied and matches
            if status is not None:
                if single_issue.get("status") != status:
                    continue

            # Check if priority filter is applied and matches
            if priority is not None:
                if single_issue.get("priority") != priority:
                    continue

            # Check if title contains the search substring (case-insensitive)
            if title_contains is not None:
                current_title = single_issue.get("title", "")
                # Convert both strings to lower case for comparison
                if title_contains.lower() not in current_title.lower():
                    continue

            # Make a clean copy and append it to our final list
            clean_copy = single_issue.copy()
            matched_results.append(clean_copy)

        return matched_results
