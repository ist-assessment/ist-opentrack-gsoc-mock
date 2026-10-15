"""JSON file persistence for OpenTrack."""

import json
import os


class JsonStorage:
    """Saves and loads issues from a JSON file."""

    def __init__(self, path):
        self.path = path

    def load(self):
        """Load issues from the file."""
        if not os.path.exists(self.path):
            return {}

        try:
            with open(self.path, "r", encoding="utf-8") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, OSError):
            return {}

        issues = raw.get("issues", {})
        return {int(k): v for k, v in issues.items()}

    def save(self, issues):
        """Save issues to the file."""
        payload = {"issues": {str(k): v for k, v in issues.items()}}

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
