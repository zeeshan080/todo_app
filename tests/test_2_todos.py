from collections.abc import Generator
from datetime import timedelta
from unittest.mock import Mock
from fastapi.testclient import TestClient
from todo_app.main import app  
from sqlalchemy import create_engine
from sqlmodel import SQLModel
from sqlalchemy.orm import Session
from todo_app.api.deps import CurrentUser, SessionDep
from todo_app.models import User
from todo_app.settings import DATABASE_URL_TEST
from todo_app.core import security
from todo_app.core.mock_db import get_test_db, create_db_and_tables



def test_create_db():
    db_created = create_db_and_tables()
    assert db_created == "Tables created.."

# Test cases for the todo app with Correct DATA 
def test_read_todos():
    app.dependency_overrides[SessionDep] = get_test_db
    # Create a mock user
    mock_user = Mock(spec=User)
    mock_user.id = 1  # Set the id of the mock user
    mock_token = security.create_access_token(mock_user.id, timedelta(minutes=30))
    app.dependency_overrides[CurrentUser] = lambda: mock_user
    client = TestClient(app=app)
    # Make the request
    response = client.get("/api/v1/todos/", headers={"Authorization": f"bearer {mock_token}"})

    # Check the response
    assert response.status_code == 200

    # Reset the dependency overrides
    app.dependency_overrides = {}

# Create a todo in the database
def test_create_todo():
    app.dependency_overrides[SessionDep] = get_test_db
    # Create a mock user
    mock_user = Mock(spec=User)
    mock_user.id = 1  # Set the id of the mock user
    mock_token = security.create_access_token(mock_user.id, timedelta(minutes=30))
    app.dependency_overrides[CurrentUser] = lambda: mock_user
    client = TestClient(app=app)
    # Make the request
    response = client.post("/api/v1/todos/", json={"title": "Test todo","completed": False},
                           headers={"Authorization": f"bearer {mock_token}"})
    print(response.json())
    # Check the response
    assert response.status_code == 200

    # Reset the dependency overrides
    app.dependency_overrides = {}

# update a todo in the database
def test_update_todo():
    app.dependency_overrides[SessionDep] = get_test_db
    # Create a mock user
    mock_user = Mock(spec=User)
    mock_user.id = 1  # Set the id of the mock user
    mock_token = security.create_access_token(mock_user.id, timedelta(minutes=30))
    app.dependency_overrides[CurrentUser] = lambda: mock_user
    client = TestClient(app=app)
    # Make the request
    response = client.put("/api/v1/todos/1", json={"title": "Test todo updated","completed": True},
                          headers={"Authorization": f"bearer {mock_token}"})

    # Check the response
    assert response.status_code == 200

    # Reset the dependency overrides
    app.dependency_overrides = {}

# delete a todo in the database
def test_delete_todo():
    app.dependency_overrides[SessionDep] = get_test_db
    # Create a mock user
    mock_user = Mock(spec=User)
    mock_user.id = 1  # Set the id of the mock user
    mock_token = security.create_access_token(mock_user.id, timedelta(minutes=30))
    app.dependency_overrides[CurrentUser] = lambda: mock_user
    client = TestClient(app=app)
    # Make the request
    response = client.delete("/api/v1/todos/1", headers={"Authorization": f"bearer {mock_token}"})

    # Check the response
    assert response.status_code == 200

    # Reset the dependency overrides
    app.dependency_overrides = {}