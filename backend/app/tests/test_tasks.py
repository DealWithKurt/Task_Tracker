from fastapi.testclient import TestClient
from datetime import date, timedelta
import pytest

def test_create_task(client: TestClient, auth_headers):
    future_date = (date.today() + timedelta(days=5)).isoformat()
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Test Task",
            "description": "Test Description",
            "status": "new",
            "priority": "high",
            "deadline": future_date
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_get_tasks(client: TestClient, auth_headers):
    response = client.get("/tasks", headers=auth_headers)
    assert response.status_code == 200
    assert "items" in response.json()
    assert "total" in response.json()

def test_get_task_by_id(client: TestClient, auth_headers):
    # First create a task
    future_date = (date.today() + timedelta(days=5)).isoformat()
    create_response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Test Task ID",
            "deadline": future_date
        }
    )
    task_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task ID"

def test_update_task(client: TestClient, auth_headers):
    future_date = (date.today() + timedelta(days=5)).isoformat()
    create_response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Task to Update",
            "deadline": future_date
        }
    )
    task_id = create_response.json()["id"]
    
    response = client.put(
        f"/tasks/{task_id}",
        headers=auth_headers,
        json={"title": "Updated Title"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Title"

def test_delete_task(client: TestClient, auth_headers):
    future_date = (date.today() + timedelta(days=5)).isoformat()
    create_response = client.post(
        "/tasks",
        headers=auth_headers,
        json={
            "title": "Task to Delete",
            "deadline": future_date
        }
    )
    task_id = create_response.json()["id"]
    
    response = client.delete(f"/tasks/{task_id}", headers=auth_headers)
    assert response.status_code == 200
    
    # Verify it's gone
    get_response = client.get(f"/tasks/{task_id}", headers=auth_headers)
    assert get_response.status_code == 404

def test_filter_by_status(client: TestClient, auth_headers):
    response = client.get("/tasks?status=new", headers=auth_headers)
    assert response.status_code == 200
    for task in response.json()["items"]:
        assert task["status"] == "new"

def test_filter_by_priority(client: TestClient, auth_headers):
    response = client.get("/tasks?priority=high", headers=auth_headers)
    assert response.status_code == 200
    for task in response.json()["items"]:
        assert task["priority"] == "high"

def test_search_by_title(client: TestClient, auth_headers):
    # First create a specific task
    future_date = (date.today() + timedelta(days=5)).isoformat()
    client.post("/tasks", headers=auth_headers, json={"title": "UniqueSearchTitle123", "deadline": future_date})
    
    response = client.get("/tasks?search=UniqueSearchTitle123", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) >= 1

def test_task_not_found(client: TestClient, auth_headers):
    response = client.get("/tasks/99999", headers=auth_headers)
    assert response.status_code == 404

def test_validation_error(client: TestClient, auth_headers):
    # Title too short
    future_date = (date.today() + timedelta(days=5)).isoformat()
    response = client.post(
        "/tasks",
        headers=auth_headers,
        json={"title": "Ab", "deadline": future_date}
    )
    assert response.status_code == 422

def test_pagination(client: TestClient, auth_headers):
    response = client.get("/tasks?page=1&limit=2", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()["items"]) <= 2
    assert response.json()["limit"] == 2
