import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_and_list():
    payload = {
        "flight_id": 99999,
        "flight_number": "TEST-99999",
        "origin": "THR",
        "destination": "JED",
        "departure_time": "2025-12-01T10:00:00",
        "arrival_time": "2025-12-01T12:00:00",
        "duration_minutes": 120,
        "aircraft_type": "A320",
        "seats_total": 150,
        "seats_available": 150,
        "status": "scheduled",
        "created_at": "2025-11-01T10:00:00",
        "updated_at": "2025-12-01T10:00:00",
        "process_id": "P-TEST"
    }
    r = client.post("/flights", json=payload)
    assert r.status_code == 201

    r2 = client.get("/flights", params={"origin":"THR","page":1,"size":10})
    assert r2.status_code == 200
    body = r2.json()
    assert "items" in body
    assert any(item["flight_number"] == "TEST-99999" for item in body["items"])
