
from datetime import datetime, timedelta

from fastapi.testclient import TestClient

from workflow_intelligence.main import app


client = TestClient(app)


def make_work_item():
    return {
        "title": "Automated Test Work Item",
        "description": "Work item created during automated testing",
        "category": "Support",
        "priority": "HIGH",
        "status": "BLOCKED",
        "estimated_hours": 20,
        "dependency_count": 3,
        "issue_count": 5,
        "hours_since_update": 50,
        "due_date": (
            datetime.utcnow() + timedelta(hours=48)
        ).isoformat()
    }


# -------------------------------------------------
# Test 1: Health Check
# -------------------------------------------------

def test_health_check():

    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


# -------------------------------------------------
# Test 2: Risk Prediction
# -------------------------------------------------

def test_risk_prediction():

    response = client.post(
        "/api/v1/risk/predict",
        json=make_work_item()
    )

    assert response.status_code == 200

    data = response.json()

    assert "risk_level" in data
    assert "risk_score" in data
    assert "top_factors" in data

    assert data["risk_level"] in [
        "LOW",
        "MEDIUM",
        "HIGH"
    ]

    assert isinstance(
        data["top_factors"],
        list
    )


# -------------------------------------------------
# Test 3: Create Work Item
# -------------------------------------------------

def test_create_work_item():

    response = client.post(
        "/api/v1/work-items",
        json=make_work_item()
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["title"] == "Automated Test Work Item"
    assert "risk_level" in data
    assert "risk_score" in data
    assert isinstance(data["top_factors"], list)


# -------------------------------------------------
# Test 4: Get Work Items
# -------------------------------------------------

def test_get_work_items():

    response = client.get(
        "/api/v1/work-items"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


# -------------------------------------------------
# Test 5: Get Nonexistent Work Item
# -------------------------------------------------

def test_work_item_not_found():

    response = client.get(
        "/api/v1/work-items/999999"
    )

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Work item not found"
    )


# -------------------------------------------------
# Test 6: Prioritized Work Items
# -------------------------------------------------

def test_prioritized_work_items():

    response = client.get(
        "/api/v1/work-items/prioritized"
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    if len(data) > 1:
        scores = [
            item["risk_score"]
            for item in data
        ]

        assert scores == sorted(
            scores,
            reverse=True
        )
