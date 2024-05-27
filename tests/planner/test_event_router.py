from unittest import mock

import pytest
from httpx import AsyncClient
from planner.application import app
from planner.exceptions import EventNotFoundError
from planner.models import Event
from planner.repositories import EventRepository


@pytest.fixture
def client() -> AsyncClient:
    yield AsyncClient(app=app, base_url="http://test")


@pytest.mark.asyncio
async def test_get_events(client: AsyncClient) -> None:
    event_repository_mock = mock.Mock(spec=EventRepository)
    event_repository_mock.get_all.return_value = []

    with app.container.event_repository.override(event_repository_mock):  # type: ignore[attr-defined]
        response = await client.get("/events")

    assert response.status_code == 200
    data = response.json()
    assert data == []

    raise NotImplementedError


@pytest.mark.asyncio
async def test_get_event_by_id(client: AsyncClient) -> None:
    event_repository_mock = mock.Mock(spec=EventRepository)
    event_repository_mock.get_by_id.return_value = Event()

    with app.container.event_repository.override(event_repository_mock):  # type: ignore[attr-defined]
        response = await client.get("")

    assert response.status_code == 200
    raise NotImplementedError


@pytest.mark.asyncio
async def test_get_event_by_id_404(client: AsyncClient) -> None:
    event_repository_mock = mock.Mock(spec=EventRepository)
    event_repository_mock.get_by_id.side_effect = EventNotFoundError(1)

    with app.container.event_repository.override(event_repository_mock):  # type: ignore[attr-defined]
        response = await client.get("/events/1")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_add_event(client: AsyncClient) -> None:
    event_repository_mock = mock.Mock(spec=EventRepository)
    event_repository_mock.add.return_value = Event()

    with app.container.event_repository.override(event_repository_mock):  # type: ignore[attr-defined]
        response = await client.post("/events")

    assert response.status_code == 201
    data = response.json()
    assert data == {}
    event_repository_mock.add.assert_called_once()
    raise NotImplementedError


@pytest.mark.skip
@pytest.mark.asyncio
async def test_remove_event(client: AsyncClient) -> None:
    raise NotImplementedError


@pytest.mark.asyncio
async def test_remove_event_404(client: AsyncClient) -> None:
    event_repository_mock = mock.Mock(spec=EventRepository)
    event_repository_mock.delete_by_id.side_effect = EventNotFoundError(1)

    with app.container.event_repository.override(event_repository_mock):  # type: ignore[attr-defined]
        response = await client.delete("/users/1")

    assert response.status_code == 404
