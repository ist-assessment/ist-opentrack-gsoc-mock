
"""Tests to make sure issues are saved correctly."""

import json

import pytest

from src.issue_service import IssueService
from src.storage import JsonStorage


def test_empty_storage(tmp_path):
    storage = JsonStorage(str(tmp_path / "issues.json"))
    service = IssueService(storage)

    assert service.list_all() == []


def test_created_issue_is_saved(tmp_path):
    path = str(tmp_path / "issues.json")

    service = IssueService(JsonStorage(path))
    issue = service.create({"title": "First issue"})

    restarted_service = IssueService(JsonStorage(path))

    assert restarted_service.get(issue["id"]) == issue


def test_updated_issue_is_saved(tmp_path):
    path = str(tmp_path / "issues.json")

    service = IssueService(JsonStorage(path))
    issue = service.create({"title": "Old title"})

    service.update(issue["id"], {"title": "New title"})

    restarted_service = IssueService(JsonStorage(path))

    assert restarted_service.get(issue["id"])["title"] == "New title"


def test_deleted_issue_stays_deleted(tmp_path):
    path = str(tmp_path / "issues.json")

    service = IssueService(JsonStorage(path))
    issue = service.create({"title": "Temporary issue"})

    service.delete(issue["id"])

    restarted_service = IssueService(JsonStorage(path))

    assert restarted_service.list_all() == []


def test_id_does_not_get_reused_after_restart(tmp_path):
    path = str(tmp_path / "issues.json")

    service = IssueService(JsonStorage(path))
    service.create({"title": "First issue"})
    second_issue = service.create({"title": "Second issue"})

    service.delete(second_issue["id"])

    restarted_service = IssueService(JsonStorage(path))
    new_issue = restarted_service.create({"title": "Third issue"})

    assert new_issue["id"] > second_issue["id"]


def test_invalid_issue_does_not_change_file(tmp_path):
    path = str(tmp_path / "issues.json")

    service = IssueService(JsonStorage(path))
    service.create({"title": "Valid issue"})

    with open(path, "rb") as file:
        original_data = file.read()

    with pytest.raises((ValueError, TypeError)):
        service.create({
            "title": "Invalid issue",
            "priority": "urgent",
        })

    with open(path, "rb") as file:
        saved_data = file.read()

    assert saved_data == original_data


def test_next_id_is_saved(tmp_path):
    path = str(tmp_path / "issues.json")

    service = IssueService(JsonStorage(path))
    service.create({"title": "First issue"})

    with open(path, "r", encoding="utf-8") as file:
        data = json.load(file)

    assert data["next_id"] == 2
