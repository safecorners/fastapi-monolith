from typing import List

from planner.models import Event
from planner.repositories import EventRepository, UserRepository
from planner.schemas.event import EventUpdate


class EventService:
    def __init__(
        self,
        event_repository: EventRepository,
        user_repository: UserRepository,
    ) -> None:
        self._event_repository = event_repository
        self._user_repository = user_repository

    async def get_events(self) -> List[Event]:
        return await self._event_repository.get_all()

    async def get_event_by_id(self, event_id: int) -> Event:
        return await self._event_repository.get_by_id(event_id)

    async def create_event(
        self,
        username: str,
        title: str,
        image: str,
        description: str,
        tags: List[str],
        location: str,
    ) -> Event:
        user = await self._user_repository.get_by_email(username)
        if user is None:
            raise Exception()

        return await self._event_repository.add(
            user_id=user.id,
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
