from src.ranking import rank_open_issues
#1st test#
def testzerolimit():
    issues = [{"id":1, "status":"open", "priority":"high"}]

    result = rank_open_issues(issues,0)
    assert result == []

#2nd test#
def testpriorityorder():
    issues = [{"id":3, "status":"open", "priority":"low"},
              {"id":2, "status":"open", "priority":"medium"},
              {"id":1, "status":"open", "priority":"high"}]

    result = rank_open_issues(issues,3)
    assert result == [1,2,3]


#3rd test#

def test_only_open_issues():
    issues = [
        {"id": 1, "status": "open", "priority": "high"},
        {"id": 2, "status": "in_progress", "priority": "high"},
        {"id": 3, "status": "closed", "priority": "medium"}
    ]

    result = rank_open_issues(issues, 3)
    assert result == [1]

#4th test#


def test_same_priority_order():
    issues = [
        {"id": 5, "status": "open", "priority": "high"},
        {"id": 2, "status": "open", "priority": "high"},
        {"id": 3, "status": "open", "priority": "high"}
    ]

    result = rank_open_issues(issues, 3)
    assert result == [2, 3, 5]
