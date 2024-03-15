from datetime import timedelta
from unittest.mock import Mock
from fastapi.testclient import TestClient
from todo_app.core.db import get_db
from todo_app.main import app  
from todo_app.models import User
from todo_app.core import security
from todo_app.core.mock_db import get_test_db, drop_tables



# Test cases for the todo app users with Correct DATA 

#Create a user in the database
def test_create_super_user():
    app.dependency_overrides[get_db] = get_test_db
    client = TestClient(app=app)
    response = client.post(
        "api/v1/super_users/",
        json={"username": "admin", "email": "admin@gmail.com","hashed_password": "adminpassword"},
    )
    assert response.status_code == 200

def test_create_user():
    app.dependency_overrides[get_db] = get_test_db
    mock_user = Mock(spec=User)
    mock_user.id = 1  # Set the id of the mock user
    mock_token = security.create_access_token(mock_user.id, timedelta(minutes=5))
    client = TestClient(app=app)
    response = client.post(
        "api/v1/users/",
        json={"username": "testuser", "email": "test@gmail.com","hashed_password": "testpassword"},
        headers={"Authorization": f"bearer {mock_token}"},
    )
    assert response.status_code == 200

    app.dependency_overrides = {}

#read all users from the database
def test_read_users():
    app.dependency_overrides[get_db] = get_test_db
    # Create a mock user
    mock_user = Mock(spec=User)
    mock_user.id = 2  # Set the id of the mock user
    mock_token = security.create_access_token(mock_user.id, timedelta(minutes=5))
    client = TestClient(app=app)
    response = client.get("/api/v1/users/?skip=0&limit=10",headers={"Authorization": f"bearer {mock_token}"})
    print(response.json())
    assert response.status_code == 200
    app.dependency_overrides = {}


#Update a user in the database
def test_update_user():
    app.dependency_overrides[get_db] = get_test_db
    mock_user = Mock(spec=User)
    mock_user.id = 1  # Set the id of the mock user
    mock_token = security.create_access_token(mock_user.id, timedelta(minutes=5))
    client = TestClient(app=app)

    response = client.put(
        "api/v1/users/1",
        json={"username": "testuser1"},
        headers={"Authorization": f"bearer {mock_token}"},
    )

    assert response.status_code == 200

    app.dependency_overrides = {}

#Delete a user in the database
def test_delete_user():
    app.dependency_overrides[get_db] = get_test_db
    mock_user = Mock(spec=User)
    mock_user.id = 1  # Set the id of the mock user
    mock_token = security.create_access_token(mock_user.id, timedelta(minutes=5))
    client = TestClient(app=app)

    response = client.delete(
        "api/v1/users/1",
        headers={"Authorization": f"bearer {mock_token}"},
    )

    assert response.status_code == 200

    app.dependency_overrides = {}


def test_drop_tables():
    db_dropped = drop_tables()
    assert db_dropped == "Tables dropped.."