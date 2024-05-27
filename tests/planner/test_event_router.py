from unittest import mock

import pytest
import pytest_asyncio
from httpx import AsyncClient
from planner.application import app
from planner.containers import container
from planner.exceptions import EventNotFoundError
from planner.models import Event, User
from planner.repositories import EventRepository, UserRepository


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    yield AsyncClient(app=app, base_url="http://test")


@pytest.fixture
def access_token() -> str:
    jwt_handler = container.jwt_handler()
    return jwt_handler.create_access_token("test@example.com")


@pytest.mark.asyncio
async def test_get_events(client: AsyncClient) -> None:
    event_repository_mock = mock.AsyncMock(spec=EventRepository)
    event_repository_mock.get_all.return_value = [
        Event(
            id=1,
            title="Event 1",
            image="image1",
            description="description1",
            tags=["tag1"],
            location="location1",
        ),
        Event(
            id=2,
            title="Event 2",
            image="image2",
            description="description2",
            tags=["tag2"],
            location="location2",
        ),
    ]

    with app.container.event_repository.override(event_repository_mock):  # type: ignore[attr-defined]
        response = await client.get("/events")

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {
            "id": 1,
            "title": "Event 1",
            "image": "image1",
            "description": "description1",
            "tags": ["tag1"],
            "location": "location1",
        },
        {
            "id": 2,
            "title": "Event 2",
            "image": "image2",
            "description": "description2",
            "tags": ["tag2"],
            "location": "location2",
        },
    ]


@pytest.mark.asyncio
async def test_get_event_by_id(client: AsyncClient) -> None:
    event_repository_mock = mock.AsyncMock(spec=EventRepository)
    event_repository_mock.get_by_id.return_value = Event(
        id=1,
        title="Event 1",
        image="image1",
        description="description1",
        tags=["tag1"],
        location="location1",
    )

    with app.container.event_repository.override(event_repository_mock):  # type: ignore[attr-defined]
        response = await client.get("/events/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Event 1",
        "image": "image1",
        "description": "description1",
        "tags": ["tag1"],
        "location": "location1",
    }


@pytest.mark.asyncio
async def test_get_event_by_id_404(client: AsyncClient) -> None:
    event_repository_mock = mock.AsyncMock(spec=EventRepository)
    event_repository_mock.get_by_id.side_effect = EventNotFoundError(1)

    with app.container.event_repository.override(event_repository_mock):  # type: ignore[attr-defined]
        response = await client.get("/events/1")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_event(client: AsyncClient, access_token: str) -> None:
    event_repository_mock = mock.AsyncMock(spec=EventRepository)
    event_repository_mock.add.return_value = Event(
        id=1,
        title="Event 1",
        image="image1",
        description="description1",
        tags=["tag1"],
        location="location1",
    )

    user_repository_mock = mock.AsyncMock(spec=UserRepository)
    user_repository_mock.get_by_email.return_value = User(
        id=1,
        email="test@example.com",
        hashed_password="hashed_password",
        is_active=True,
    )

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}",
    }

    with (
        app.container.event_repository.override(event_repository_mock),  # type: ignore[attr-defined]
        app.container.user_repository.override(user_repository_mock),  # type: ignore[attr-defined]
    ):
        response = await client.post(
            "/events/",
            json={
                "id": 1,
                "title": "Event 1",
                "image": "image1",
                "description": "description1",
                "tags": ["tag1"],
                "location": "location1",
            },
            headers=headers,
        )

    assert response.status_code == 201
    data = response.json()
    assert data == {
        "id": 1,
        "title": "Event 1",
        "image": "image1",
        "description": "description1",
        "tags": ["tag1"],
        "location": "location1",
    }
    event_repository_mock.add.assert_called_once()


@pytest.mark.asyncio
async def test_remove_event(client: AsyncClient) -> None:
    event_repository_mock = mock.AsyncMock(spec=EventRepository)

    with app.container.event_repository.override(event_repository_mock):  # type: ignore[attr-defined]
        response = await client.delete("/events/1")

    assert response.status_code == 204
    event_repository_mock.delete_by_id.assert_called_once_with(1)


@pytest.mark.asyncio
async def test_remove_event_404(client: AsyncClient) -> None:
    event_repository_mock = mock.AsyncMock(spec=EventRepository)
    event_repository_mock.delete_by_id.side_effect = EventNotFoundError(1)

    with app.container.event_repository.override(event_repository_mock):  # type: ignore[attr-defined]
        response = await client.delete("/events/1")

    assert response.status_code == 404
