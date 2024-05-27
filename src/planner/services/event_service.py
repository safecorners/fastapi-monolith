from typing import List

from planner.models import Event
from planner.repositories import EventRepository
from planner.schemas.event import EventUpdate


class EventService:
    def __init__(self, event_repository: EventRepository) -> None:
        self._event_repository = event_repository

    async def get_events(self) -> List[Event]:
        return await self._event_repository.get_all()

    async def get_event_by_id(self, event_id: int) -> Event:
        return await self._event_repository.get_by_id(event_id)

    async def create_event(
        self,
        user_id: int,
        title: str,
        image: str,
        description: str,
        tags: List[str],
        location: str,
    ) -> Event:
        return await self._event_repository.add(
            user_id=user_id,
            title=title,
            image=image,
            description=description,
            tags=tags,
            location=location,
        )

    async def update_event(self, event_id: int, payload: EventUpdate) -> Event:
        event = await self._event_repository.get_by_id(event_id)
        payload.dict(exclude_unset=True)
        for key, value in payload:
            setattr(event, key, value)
        return await self._event_repository.update_event(event)

    async def delete_event_by_id(self, event_id: int) -> None:
        return await self._event_repository.delete_by_id(event_id)
