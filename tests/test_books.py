import pytest
from fastapi import status

def get_auth_headers(client):
    client.post("/auth/register", json={"email": "testuser@example.com", "password": "string123"})
    login_resp = client.post("/auth/login", data={"username": "testuser@example.com", "password": "string123"})
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_book(client, auth_headers):
    print("\n[STEP] Create book")
    response = client.post("/books/", json={"title": "Book1", "author": "Author1", "year": 2020, "isbn": "1234567890", "count": 2}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["title"] == "Book1"
    assert data["isbn"] == "1234567890"
    assert data["count"] == 2

def test_create_book_duplicate_isbn(client, auth_headers):
    client.post("/books/", json={"title": "Book1", "author": "Author1", "year": 2020, "isbn": "1234567890", "count": 2}, headers=auth_headers)
    response = client.post("/books/", json={"title": "Book2", "author": "Author2", "year": 2021, "isbn": "1234567890", "count": 1}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 400
    assert "ISBN already exists" in response.json()["detail"]

def test_create_book_negative_count(client, auth_headers):
    response = client.post("/books/", json={"title": "Book3", "author": "Author3", "year": 2022, "isbn": "0987654321", "count": -1}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code in (400, 422)

def test_read_books(client, auth_headers):
    client.post("/books/", json={"title": "Book4", "author": "Author4", "year": 2023, "isbn": "1111111111", "count": 1}, headers=auth_headers)
    response = client.get("/books/", headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_book(client, auth_headers):
    resp = client.post("/books/", json={"title": "Book5", "author": "Author5", "year": 2024, "isbn": "2222222222", "count": 1}, headers=auth_headers)
    book_id = resp.json()["id"]
    response = client.put(f"/books/{book_id}", json={"title": "Book5 Updated", "count": 3}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["title"] == "Book5 Updated"
    assert response.json()["count"] == 3

def test_delete_book(client, auth_headers):
    resp = client.post("/books/", json={"title": "Book6", "author": "Author6", "year": 2025, "isbn": "3333333333", "count": 1}, headers=auth_headers)
    book_id = resp.json()["id"]
    response = client.delete(f"/books/{book_id}", headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["id"] == book_id 