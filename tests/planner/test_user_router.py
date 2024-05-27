from unittest import mock

import pytest
import pytest_asyncio
from httpx import AsyncClient
from planner.application import app
from planner.exceptions import UserNotFoundError
from planner.models import User
from planner.repositories import UserRepository


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    yield AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_get_list(client: AsyncClient) -> None:
    repository_mock = mock.AsyncMock(spec=UserRepository)
    repository_mock.get_all.return_value = [
        User(id=1, email="test1@email.com", hashed_password="pwd", is_active=True),
        User(id=2, email="test2@email.com", hashed_password="pwd", is_active=False),
    ]

    with app.container.user_repository.override(repository_mock):  # type: ignore[attr-defined]
        response = await client.get("/users")

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {
            "id": 1,
            "email": "test1@email.com",
            "hashed_password": "pwd",
            "is_active": True,
        },
        {
            "id": 2,
            "email": "test2@email.com",
            "hashed_password": "pwd",
            "is_active": False,
        },
    ]


@pytest.mark.asyncio
async def test_get_by_id(client: AsyncClient) -> None:
    repository_mock = mock.AsyncMock(spec=UserRepository)
    repository_mock.get_by_id.return_value = User(
        id=1,
        email="xyz@email.com",
        hashed_password="pwd",
        is_active=True,
    )

    with app.container.user_repository.override(repository_mock):  # type: ignore[attr-defined]
        response = await client.get("/users/1")

    assert response.status_code == 200
    data = response.json()
    assert data == {
        "id": 1,
        "email": "xyz@email.com",
        "hashed_password": "pwd",
        "is_active": True,
    }
    repository_mock.get_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_get_by_id_404(client: AsyncClient) -> None:
    repository_mock = mock.AsyncMock(spec=UserRepository)
    repository_mock.get_by_id.side_effect = UserNotFoundError(1)

    with app.container.user_repository.override(repository_mock):  # type: ignore[attr-defined]
        response = await client.get("/users/1")

    assert response.status_code == 404


@pytest.mark.asyncio
@mock.patch("planner.services.user_service.uuid4", return_value="xyz")
async def test_add(_, client: AsyncClient) -> None:  # type: ignore[no-untyped-def]
    repository_mock = mock.AsyncMock(spec=UserRepository)
    repository_mock.add.return_value = User(
        id=1,
        email="xyz@email.com",
        hashed_password="pwd",
        is_active=True,
    )

    with app.container.user_repository.override(repository_mock):  # type: ignore[attr-defined]
        response = await client.post("/users")

    assert response.status_code == 201
    data = response.json()
    assert data == {
        "id": 1,
        "email": "xyz@email.com",
        "hashed_password": "pwd",
        "is_active": True,
    }
    repository_mock.add.assert_called_once_with(email="xyz@email.com", password="pwd")


@pytest.mark.asyncio
async def test_remove(client: AsyncClient) -> None:
    repository_mock = mock.AsyncMock(spec=UserRepository)

    with app.container.user_repository.override(repository_mock):  # type: ignore[attr-defined]
        response = await client.delete("/users/1")

    assert response.status_code == 204
    repository_mock.delete_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_remove_404(client: AsyncClient) -> None:
    repository_mock = mock.AsyncMock(spec=UserRepository)
    repository_mock.delete_by_id.side_effect = UserNotFoundError(1)

    with app.container.user_repository.override(repository_mock):  # type: ignore[attr-defined]
        response = await client.delete("/users/1")

    assert response.status_code == 404
