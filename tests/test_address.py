from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def create_test_address(name: str = "Test Home"):
    """Helper function to create an address for tests."""
    payload = {
        "name": name,
        "street": "MG Road",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "zipcode": "560001",
        "latitude": 12.9716,
        "longitude": 77.5946,
    }

    response = client.post("/addresses", json=payload)
    assert response.status_code == 201
    return response.json()


def test_health_check():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_address():
    payload = {
        "name": "My Home",
        "street": "MG Road",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "zipcode": "560001",
        "latitude": 12.9716,
        "longitude": 77.5946,
    }

    response = client.post("/addresses", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["name"] == payload["name"]
    assert data["city"] == payload["city"]


def test_create_address_invalid_latitude():
    payload = {
        "name": "Invalid",
        "street": "Test",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "zipcode": "560001",
        "latitude": 100,
        "longitude": 77.5946,
    }

    response = client.post("/addresses", json=payload)

    assert response.status_code == 422


def test_create_address_invalid_longitude():
    payload = {
        "name": "Invalid",
        "street": "Test",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "zipcode": "560001",
        "latitude": 12.9716,
        "longitude": 190,
    }

    response = client.post("/addresses", json=payload)

    assert response.status_code == 422


def test_create_address_missing_required_field():
    payload = {
        "street": "MG Road",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "zipcode": "560001",
        "latitude": 12.9716,
        "longitude": 77.5946,
    }

    response = client.post("/addresses", json=payload)

    assert response.status_code == 422


def test_get_all_addresses():
    create_test_address("List Test")

    response = client.get("/addresses")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_address_by_id():
    created = create_test_address("Fetch Test")

    response = client.get(f"/addresses/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_non_existing_address():
    response = client.get("/addresses/999999")

    assert response.status_code == 404


def test_update_address():
    created = create_test_address("Before Update")

    payload = {
        "name": "After Update",
        "street": "Updated Street",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "zipcode": "560001",
        "latitude": 12.9716,
        "longitude": 77.5946,
    }

    response = client.put(
        f"/addresses/{created['id']}",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "After Update"


def test_update_non_existing_address():
    payload = {
        "name": "Updated",
        "street": "Street",
        "city": "Bengaluru",
        "state": "Karnataka",
        "country": "India",
        "zipcode": "560001",
        "latitude": 12.9716,
        "longitude": 77.5946,
    }

    response = client.put("/addresses/999999", json=payload)

    assert response.status_code == 404


def test_delete_address():
    created = create_test_address("Delete Me")

    response = client.delete(f"/addresses/{created['id']}")

    assert response.status_code in (200, 204)


def test_delete_non_existing_address():
    response = client.delete("/addresses/999999")

    assert response.status_code == 404


def test_nearby_search_success():
    create_test_address("Nearby Home")

    response = client.get(
        "/addresses/search/nearby",
        params={
            "latitude": 12.9716,
            "longitude": 77.5946,
            "radius_km": 5,
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_nearby_search_zero_radius():
    response = client.get(
        "/addresses/search/nearby",
        params={
            "latitude": 12.9716,
            "longitude": 77.5946,
            "radius_km": 0,
        },
    )

    assert response.status_code == 422


def test_nearby_search_negative_radius():
    response = client.get(
        "/addresses/search/nearby",
        params={
            "latitude": 12.9716,
            "longitude": 77.5946,
            "radius_km": -5,
        },
    )

    assert response.status_code == 422


def test_nearby_search_invalid_latitude():
    response = client.get(
        "/addresses/search/nearby",
        params={
            "latitude": 100,
            "longitude": 77.5946,
            "radius_km": 5,
        },
    )

    assert response.status_code == 422


def test_nearby_search_invalid_longitude():
    response = client.get(
        "/addresses/search/nearby",
        params={
            "latitude": 12.9716,
            "longitude": 200,
            "radius_km": 5,
        },
    )

    assert response.status_code == 422


def test_nearby_search_missing_parameters():
    response = client.get("/addresses/search/nearby")

    assert response.status_code == 422


def test_nearby_search_no_results():
    response = client.get(
        "/addresses/search/nearby",
        params={
            "latitude": 40.7128,
            "longitude": -74.0060,
            "radius_km": 1,
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)