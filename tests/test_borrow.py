import pytest
from fastapi import status

def register_reader(client, name, email, headers):
    return client.post("/readers/", json={"name": name, "email": email}, headers=headers)

def create_book(client, title, isbn, count, headers):
    return client.post("/books/", json={"title": title, "author": "Author", "year": 2020, "isbn": isbn, "count": count}, headers=headers)

def test_borrow_book_success(client, auth_headers):
    reader = register_reader(client, "Reader1", "r1@example.com", auth_headers).json()
    book = create_book(client, "Book1", "isbn1", 2, auth_headers).json()
    response = client.post(f"/borrow/", json={"reader_id": reader["id"], "book_id": book["id"]}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 201
    assert response.json()["book_id"] == book["id"]
    assert response.json()["reader_id"] == reader["id"]

def test_borrow_book_no_copies(client, auth_headers):
    reader = register_reader(client, "Reader2", "r2@example.com", auth_headers).json()
    book = create_book(client, "Book2", "isbn2", 0, auth_headers).json()
    response = client.post(f"/borrow/", json={"reader_id": reader["id"], "book_id": book["id"]}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 400
    assert "No available copies" in response.json()["detail"]

def test_borrow_book_limit(client, auth_headers):
    reader = register_reader(client, "Reader3", "r3@example.com", auth_headers).json()
    for i in range(3):
        book = create_book(client, f"BookL{i}", f"isbnL{i}", 1, auth_headers).json()
        client.post(f"/borrow/", json={"reader_id": reader["id"], "book_id": book["id"]}, headers=auth_headers)
    book4 = create_book(client, "BookL4", "isbnL4", 1, auth_headers).json()
    response = client.post(f"/borrow/", json={"reader_id": reader["id"], "book_id": book4["id"]}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 400
    assert "Borrow limit reached" in response.json()["detail"]

def test_return_book_success(client, auth_headers):
    reader = register_reader(client, "Reader4", "r4@example.com", auth_headers).json()
    book = create_book(client, "BookR", "isbnR", 1, auth_headers).json()
    borrow = client.post(f"/borrow/", json={"reader_id": reader["id"], "book_id": book["id"]}, headers=auth_headers).json()
    response = client.post(f"/return/", json={"reader_id": reader["id"], "book_id": book["id"]}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["return_date"] is not None

def test_return_book_not_borrowed(client, auth_headers):
    reader = register_reader(client, "Reader5", "r5@example.com", auth_headers).json()
    book = create_book(client, "BookNR", "isbnNR", 1, auth_headers).json()
    response = client.post(f"/return/", json={"reader_id": reader["id"], "book_id": book["id"]}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 400
    assert "No active borrow found" in response.json()["detail"]

def test_return_book_already_returned(client, auth_headers):
    reader = register_reader(client, "Reader6", "r6@example.com", auth_headers).json()
    book = create_book(client, "BookAR", "isbnAR", 1, auth_headers).json()
    borrow = client.post(f"/borrow/", json={"reader_id": reader["id"], "book_id": book["id"]}, headers=auth_headers).json()
    client.post(f"/return/", json={"reader_id": reader["id"], "book_id": book["id"]}, headers=auth_headers)
    response = client.post(f"/return/", json={"reader_id": reader["id"], "book_id": book["id"]}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 400
    assert "No active borrow found" in response.json()["detail"] 