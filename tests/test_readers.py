import pytest
from fastapi import status

def test_create_reader(client, auth_headers):
    print("\n[STEP] Create reader")
    response = client.post("/readers/", json={"name": "Reader1", "email": "reader1@example.com"}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "Reader1"
    assert data["email"] == "reader1@example.com"

def test_create_reader_duplicate_email(client, auth_headers):
    client.post("/readers/", json={"name": "Reader2", "email": "reader2@example.com"}, headers=auth_headers)
    response = client.post("/readers/", json={"name": "Reader3", "email": "reader2@example.com"}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 400
    assert "Email already exists" in response.json()["detail"]

def test_read_readers(client, auth_headers):
    client.post("/readers/", json={"name": "Reader4", "email": "reader4@example.com"}, headers=auth_headers)
    response = client.get("/readers/", headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_reader(client, auth_headers):
    resp = client.post("/readers/", json={"name": "Reader5", "email": "reader5@example.com"}, headers=auth_headers)
    reader_id = resp.json()["id"]
    response = client.put(f"/readers/{reader_id}", json={"name": "Reader5 Updated"}, headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["name"] == "Reader5 Updated"

def test_delete_reader(client, auth_headers):
    resp = client.post("/readers/", json={"name": "Reader6", "email": "reader6@example.com"}, headers=auth_headers)
    reader_id = resp.json()["id"]
    response = client.delete(f"/readers/{reader_id}", headers=auth_headers)
    print("[DATA] Response:", response.status_code, response.json())
    assert response.status_code == 200
    assert response.json()["id"] == reader_id 