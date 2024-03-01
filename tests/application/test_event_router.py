from unittest import mock

import pytest
from fastapi.testclient import TestClient

from application.application import app
from application.exceptions import EventNotFoundError
from application.models import Event, User
from application.repositories import EventRepository, UserRepository


@pytest.fixture
def client() -> TestClient:
    yield TestClient(app)

def test_get_events(client: TestClient) -> None:
    event_repository_mock = mock.Mock(spec=EventRepository)
    event_repository_mock.get_all.return_value = []

    with app.container.event_repository.override(event_repository_mock):
        response = client.get("/events")

    assert response.status_code == 200
    data = response.json()
    assert data == []
    
    raise NotImplementedError

def test_get_event_by_id(client: TestClient) -> None:
    event_repository_mock = mock.Mock(spec=EventRepository)
    event_repository_mock.get_by_id.return_value = Event()

    with app.container.event_repository.override(event_repository_mock):
        response = client.get("")
    
    raise NotImplementedError

def test_get_event_by_id_404(client: TestClient) -> None:
    event_repository_mock = mock.Mock(spec=EventRepository)
    event_repository_mock.get_by_id.side_effect = EventNotFoundError(1)

    with app.container.event_repository.override(event_repository_mock):
        response = client.get("/events/1")

    assert response.status_code == 404

def test_add_event(client: TestClient) -> None:
    event_repository_mock = mock.Mock(spec=EventRepository)
    event_repository_mock.add.return_value = Event()

    with app.container.event_repository.override(event_repository_mock):
        response = client.post("/events")

    assert response.status_code == 201
    data = response.json()
    assert data == {}
    event_repository_mock.add.assert_called_once()
    raise NotImplementedError

def test_remove_event(client: TestClient) -> None:
    raise NotImplementedError

def test_remove_event_404(client: TestClient) -> None:
    event_repository_mock = mock.Mock(spec=EventRepository)

    
    