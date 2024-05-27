import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from planner.application import app
from planner.containers import container
from planner.repositories.user_repository import UserRepository
from planner.services.user_service import UserService


@pytest_asyncio.fixture(scope="function")
async def test_app() -> LifespanManager:
    async with LifespanManager(app) as manager:
        yield manager.app


@pytest_asyncio.fixture
async def client(test_app: FastAPI) -> AsyncClient:
    client = AsyncClient(app=test_app, base_url="http://test")
    yield client


@pytest_asyncio.fixture
async def user_repository() -> UserRepository:
    repository = container.user_repository()

    yield repository


@pytest_asyncio.fixture
async def user_service() -> UserService:
    service = container.user_service()

    yield service


@pytest.mark.asyncio
async def test_sign_up(client: AsyncClient, user_repository: UserRepository) -> None:
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

    user = await user_repository.get_by_email("test@planner.com")
    if user is not None:
        await user_repository.delete_by_id(user.id)


@pytest.mark.asyncio
async def test_sign_in(client: AsyncClient, user_service: UserService) -> None:
    payload = {
        "username": "test@planner.com",
        "password": "test-password",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    user = await user_service.sign_up(payload["username"], payload["password"])

    response = await client.post("/signin", data=payload, headers=headers)

    assert response.status_code == 200
    assert response.json()["token_type"] == "Bearer"

    await user_service.delete_user_by_id(user.id)


@pytest.mark.asyncio
async def test_sign_wrong_user_in(client: AsyncClient) -> None:
    payload = {
        "username": "wronguser@planner.com",
        "password": "test-password",
    }
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    response = await client.post("/signin", data=payload, headers=headers)

    assert response.status_code == 403
