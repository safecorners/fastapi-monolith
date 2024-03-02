from typing import List

from planner.models import Event
from planner.repositories import EventRepository


class EventService:
    def __init__(self, event_repository: EventRepository) -> None:
        self._event_repository = event_repository

    def get_events(self) -> List[Event]:
        return self._event_repository.get_all()

    def get_event_by_id(self, event_id: int) -> Event:
        return self._event_repository.get_by_id(event_id)

    def create_event(self) -> Event:
        raise NotImplementedError

    def delete_event_by_id(self, event_id: int) -> None:
        return self._event_repository.delete_by_id(event_id)
