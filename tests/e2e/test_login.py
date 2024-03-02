import pytest
from fastapi.testclient import TestClient
from planner.application import create_app


@pytest.fixture
def client() -> TestClient:
    app = create_app()
    client = TestClient(app=app)
    yield client

def test_sign_up_new_user(client: TestClient) -> None:
    payload = {
        "email": "test@planner.com",
        "password": "test-password",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    expect_response = {
        "message": "User created successfully."
    }

    response = client.post("/signup", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == expect_response


def test_sign_user_in(client: TestClient) -> None:
    payload = {
        "email": "test@planner.com",
        "password": "test-password",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = client.post("/signin", data=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"


def test_sign_wrong_user_in(client: TestClient) -> None:
    payload = {
        "email": "wronguser@planner.com",
        "password": "test-password",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = client.post("/signin", data=payload, headers=headers)

    assert response.status_code == 404
