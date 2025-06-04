import pytest
from fastapi import status
from app.core.config import settings

def test_register_user(client):
    print("\n[STEP] Register user")
    response = client.post("/auth/register", json={"email": "user@example.com", "password": "string123"})
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "user@example.com"
    assert "id" in data

def test_login_user(client):
    print("\n[STEP] Register user for login")
    client.post("/auth/register", json={"email": "user@example.com", "password": "string123"})
    print("[STEP] Login user")
    response = client.post("/auth/login", data={"username": "user@example.com", "password": "string123"})
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_protected_endpoint_requires_auth(client):
    print("\n[STEP] Access protected endpoint without token")
    response = client.get("/readers/")
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_register_user_twice(client):
    print("\n[STEP] Register user first time")
    client.post("/auth/register", json={"email": "user2@example.com", "password": "string123"})
    print("[STEP] Register user second time (should fail)")
    response = client.post("/auth/register", json={"email": "user2@example.com", "password": "string123"})
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_login_wrong_password(client):
    print("\n[STEP] Register user for wrong password test")
    client.post("/auth/register", json={"email": "user3@example.com", "password": "string123"})
    print("[STEP] Login with wrong password")
    response = client.post("/auth/login", data={"username": "user3@example.com", "password": "wrongpass"})
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_nonexistent_user(client):
    print("\n[STEP] Login with nonexistent user")
    response = client.post("/auth/login", data={"username": "nouser@example.com", "password": "string123"})
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_protected_endpoint_with_invalid_token(client):
    print("\n[STEP] Access protected endpoint with invalid token")
    headers = {"Authorization": "Bearer invalidtoken"}
    response = client.get("/readers/", headers=headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 401
    assert response.json()["detail"] == "Could not validate credentials"

def test_register_invalid_email(client):
    print("\n[STEP] Register with invalid email")
    response = client.post("/auth/register", json={"email": "not-an-email", "password": "string123"})
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code in (400, 422) 