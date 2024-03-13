from fastapi.testclient import TestClient
from todo_app.main import app  

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_read_todos():
    response = client.get("/todos/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_todo():
    response = client.post(
        "/todos/",
        json={"title": "Test", "completed": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["completed"] == False

def test_update_todo():
    response = client.post(
        "/todos/",
        json={"title": "Test", "completed": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["completed"] == False
    response = client.put(
        f"/todos/{data['id']}",
        json={"title": "Test updated", "completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test updated"
    assert data["completed"] == True

def test_delete_todo():
    response = client.post(
        "/todos/",
        json={"title": "Test", "completed": False}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["completed"] == False
    response = client.delete(
        f"/todos/{data['id']}"
    )
    assert response.status_code == 200
    data = response.json()
    assert data == {"message": "Todo deleted successfully"}