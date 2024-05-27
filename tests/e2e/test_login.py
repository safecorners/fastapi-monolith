import pytest
from httpx import AsyncClient
from planner.application import create_app


@pytest.fixture
def client() -> AsyncClient:
    app = create_app()
    client = AsyncClient(app=app, base_url="http://test")
    yield client


@pytest.mark.asyncio
async def test_sign_up_new_user(client: AsyncClient) -> None:
    payload = {
        "email": "test@planner.com",
        "password": "test-password",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    expect_response = {"message": "User created successfully."}

    response = await client.post("/signup", json=payload, headers=headers)

    assert response.status_code == 200
    assert response.json() == expect_response


@pytest.mark.asyncio
async def test_sign_user_in(client: AsyncClient) -> None:
    payload = {
        "email": "test@planner.com",
        "password": "test-password",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = await client.post("/signin", data=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"


@pytest.mark.asyncio
async def test_sign_wrong_user_in(client: AsyncClient) -> None:
    payload = {
        "email": "wronguser@planner.com",
        "password": "test-password",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = await client.post("/signin", data=payload, headers=headers)

    assert response.status_code == 404
