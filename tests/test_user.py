import pytest
from fastapi import status
from fastapi.testclient import TestClient

from src.main import app  # Импортируем ваше приложение FastAPI

client = TestClient(app)  # Создаем тестовый клиент

def test_get_existed_user():
    # Предварительно создаем пользователя для теста
    test_email = "existed@example.com"
    test_name = "Existed User"
    db.create_user(test_name, test_email)
    
    response = client.get("/user", params={"email": test_email})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": db.get_user_by_email(test_email)["id"],
        "name": test_name,
        "email": test_email
    }

def test_get_not_existed_user():
    non_existent_email = "nonexistent@example.com"
    
    response = client.get("/user", params={"email": non_existent_email})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}

def test_create_user():
    test_email = "new@example.com"
    test_name = "New User"
    
    response = client.post(
        "/user",
        json={"name": test_name, "email": test_email}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert isinstance(response.json(), int)  # Проверяем что вернулся ID
    
    # Проверяем что пользователь действительно создан
    user = db.get_user_by_email(test_email)
    assert user is not None
    assert user["name"] == test_name
    assert user["email"] == test_email

def test_create_existed_user():
    # Сначала создаем пользователя
    test_email = "duplicate@example.com"
    test_name = "Duplicate User"
    db.create_user(test_name, test_email)
    
    # Пытаемся создать такого же пользователя
    response = client.post(
        "/user",
        json={"name": test_name, "email": test_email}
    )
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {"detail": "User with this email already exists"}

def test_delete_user():
    # Сначала создаем пользователя для удаления
    test_email = "todelete@example.com"
    test_name = "To Delete User"
    db.create_user(test_name, test_email)
    
    response = client.delete("/user", params={"email": test_email})
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Проверяем что пользователь действительно удален
    assert db.get_user_by_email(test_email) is None

def test_delete_not_existed_user():
    non_existent_email = "nonexistent@example.com"
    
    response = client.delete("/user", params={"email": non_existent_email})
    assert response.status_code == status.HTTP_204_NO_CONTENT