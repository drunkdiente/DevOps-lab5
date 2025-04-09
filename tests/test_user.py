import sys
import os
import pytest

# Добавляем корень проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import app
from src.fake_db import db
from fastapi import status
from fastapi.testclient import TestClient

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_db():
    """Фикстура для сброса базы данных перед каждым тестом"""
    db._users = [
        {'id': 1, 'name': 'Ivan Ivanov', 'email': 'i.i.ivanov@mail.com'},
        {'id': 2, 'name': 'Petr Petrov', 'email': 'p.p.petrov@mail.com'}
    ]
    db._id = 2
    yield

def test_get_existed_user():
    response = client.get("/api/user", params={"email": "i.i.ivanov@mail.com"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "name": "Ivan Ivanov",
        "email": "i.i.ivanov@mail.com"
    }

def test_get_not_existed_user():
    response = client.get("/api/user", params={"email": "nonexistent@example.com"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}

def test_create_user():
    response = client.post(
        "/api/user",
        json={"name": "New User", "email": "new@example.com"}
    )
    assert response.status_code == status.HTTP_201_CREATED

def test_create_existed_user():
    response = client.post(
        "/api/user",
        json={"name": "Duplicate", "email": "i.i.ivanov@mail.com"}
    )
    assert response.status_code == status.HTTP_409_CONFLICT

def test_delete_user():
    response = client.delete("/api/user", params={"email": "i.i.ivanov@mail.com"})
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_delete_not_existed_user():
    response = client.delete("/api/user", params={"email": "nonexistent@example.com"})
    assert response.status_code == status.HTTP_204_NO_CONTENT