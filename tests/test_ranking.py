from src.ranking import rank_open_issues


def test_only_open_issues():
    issues = [
        {"id": 1, "status": "open", "priority": "high"},
        {"id": 2, "status": "closed", "priority": "high"},
        {"id": 3, "status": "in_progress", "priority": "high"},
    ]
    assert rank_open_issues(issues, 10) == [1]


def test_priority_order():
    issues = [
        {"id": 1, "status": "open", "priority": "low"},
        {"id": 2, "status": "open", "priority": "medium"},
        {"id": 3, "status": "open", "priority": "high"},
    ]
    assert rank_open_issues(issues, 3) == [3, 2, 1]


def test_ids_ascending():
    issues = [
        {"id": 9, "status": "open", "priority": "high"},
        {"id": 2, "status": "open", "priority": "high"},
        {"id": 5, "status": "open", "priority": "high"},
    ]
    assert rank_open_issues(issues, 3) == [2, 5, 9]


def test_zero_limit():
    issues = [{"id": 1, "status": "open", "priority": "high"}]
    assert rank_open_issues(issues, 0) == []


def test_result_limit():
    issues = [
        {"id": 1, "status": "open", "priority": "high"},
        {"id": 2, "status": "open", "priority": "medium"},
        {"id": 3, "status": "open", "priority": "low"},
    ]
    assert rank_open_issues(issues, 2) == [1, 2]


def test_original_list_unchanged():
    issues = [
        {"id": 3, "status": "open", "priority": "low"},
        {"id": 1, "status": "open", "priority": "high"},
    ]
    original = [issue.copy() for issue in issues]

    rank_open_issues(issues, 2)

    assert issues == original