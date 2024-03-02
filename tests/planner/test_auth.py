import pytest
from fastapi.testclient import TestClient

from planner.application import create_app
from planner.containers import create_container


@pytest.fixture(scope="module")
def access_token() -> str:
    container = create_container()
    jwt_handler = container.jwt_handler()
    return jwt_handler.create_access_token("test@example.com")

@pytest.fixture
def client() -> TestClient:
    app = create_app()
    return TestClient(app=app)


def test_authenticate_with_jwt_token(client: TestClient, access_token : str) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization" : f"Bearer {access_token}"

    }
    
    response = client.get("/protected", headers=headers)

    assert response.status_code == 200
    assert response.json()["username"] == "test@example.com"
    

def test_authenticate_without_token(client: TestClient) -> None:
    response = client.get("/protected")
    assert response.status_code == 401