def login(client, email, password):
    response = client.post(
        "/api/v1/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_signup_and_login(client):
    response = client.post(
        "/api/v1/auth/signup",
        json={"name": "New User", "email": "new@example.com", "password": "New123!"},
    )
    assert response.status_code == 200

    token = login(client, "new@example.com", "New123!")
    assert token


def test_list_menu(client):
    response = client.get("/api/v1/menu/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_menu_create_requires_auth(client):
    response = client.post(
        "/api/v1/menu/",
        json={"name": "Unauthorized", "description": "Nope", "price": 5.0},
    )
    assert response.status_code in {401, 403}


def test_menu_create_admin(client):
    token = login(client, "admin@example.com", "Admin123!")
    response = client.post(
        "/api/v1/menu/",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": "Authorized", "description": "Yep", "price": 11.0},
    )
    assert response.status_code == 200


def test_guest_reservation(client):
    response = client.post(
        "/api/v1/reservations/",
        json={
            "party_size": 2,
            "reserved_for": "2030-01-01T18:00:00Z",
            "guest_name": "Guest",
            "guest_email": "guest@example.com",
            "guest_phone": "555-0101",
        },
    )
    assert response.status_code == 200


def test_customer_reservation(client):
    token = login(client, "customer@example.com", "Cust123!")
    response = client.post(
        "/api/v1/reservations/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "party_size": 4,
            "reserved_for": "2030-01-02T19:00:00Z",
        },
    )
    assert response.status_code == 200
