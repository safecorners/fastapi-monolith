import pytest
from httpx import AsyncClient
from planner.application import create_app
from planner.containers import create_container


@pytest.fixture(scope="module")
def access_token() -> str:
    container = create_container()
    jwt_handler = container.jwt_handler()
    return jwt_handler.create_access_token("test@example.com")


@pytest.fixture
def client() -> AsyncClient:
    app = create_app()
    return AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_authenticate_with_jwt_token(
    client: AsyncClient, access_token: str
) -> None:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    response = await client.get("/protected", headers=headers)

    assert response.status_code == 200
    assert response.json()["username"] == "test@example.com"


@pytest.mark.asyncio
async def test_authenticate_without_token(client: AsyncClient) -> None:
    response = await client.get("/protected")
    assert response.status_code == 401
