# tests/test_app.py
import json
import pytest
from app import app, tasks

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_tasks(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "tasks" in data

def test_create_task(client):
    new_task = {"title": "Test task", "done": False}
    response = client.post("/tasks", json=new_task)
    assert response.status_code == 201
    data = json.loads(response.data)
    assert "task" in data
    assert data["task"]["title"] == new_task["title"]

def test_update_task(client):
    updated_task = {"title": "Updated task", "done": True}
    task_id = tasks[0]["id"]
    response = client.put(f"/tasks/{task_id}", json=updated_task)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "task" in data
    assert data["task"]["title"] == updated_task["title"]
    assert data["task"]["done"] == updated_task["done"]

def test_delete_task(client):
    task_id = tasks[0]["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "result" in data
    assert data["result"] is True

def test_get_nonexistent_task(client):
    nonexistent_task_id = max(task["id"] for task in tasks) + 1
    response = client.get(f"/tasks/{nonexistent_task_id}")
    assert response.status_code == 404
    data = json.loads(response.data)
    assert "error" in data
