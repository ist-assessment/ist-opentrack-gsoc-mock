
"""JSON file persistence for OpenTrack."""

import json
import os


class JsonStorage:
    """Persists issues to a single JSON file."""

    def __init__(self, path):
        self.path = path

    def load(self):
        """Load issues and the next ID from disk."""
        if not os.path.exists(self.path):
            return {"issues": {}, "next_id": 1}

        with open(self.path, "r", encoding="utf-8") as file:
            raw = json.load(file)

        issues = {
            int(key): value
            for key, value in raw.get("issues", {}).items()
        }

        next_id = max(
            raw.get("next_id", 1),
            max(issues, default=0) + 1,
        )

        return {
            "issues": issues,
            "next_id": next_id,
        }

    def save(self, issues, next_id=None):
        """Write issues and the next ID to disk."""
        if next_id is None:
            next_id = max(issues, default=0) + 1

        next_id = max(
            next_id,
            max(issues, default=0) + 1,
        )

        payload = {
            "issues": {
                str(key): value
                for key, value in issues.items()
            },
            "next_id": next_id,
        }

        directory = os.path.dirname(os.path.abspath(self.path))
        os.makedirs(directory, exist_ok=True)

        temp_path = self.path + ".tmp"

        try:
            with open(temp_path, "w", encoding="utf-8") as file:
                json.dump(payload, file, indent=2)
                file.flush()
                os.fsync(file.fileno())

            os.replace(temp_path, self.path)
        finally:
            if os.path.exists(temp_path):
                os.remove(temp_path)

    def save_state(self, issues, next_id):
        """Save issues together with the next ID."""
        self.save(issues, next_id)
