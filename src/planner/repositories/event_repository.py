from typing import List

from sqlalchemy import select

from planner.database import SessionFactory
from planner.exceptions import EventNotFoundError
from planner.models import Event


class EventRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    async def get_all(self) -> List[Event]:
        async with self._session_factory() as session:
            stmt = select(Event)
            result = await session.execute(stmt)
            events = list(result.scalars().all())
            return events

    async def get_by_id(self, event_id: int) -> Event:
        async with self._session_factory() as session:
            stmt = select(Event).where(Event.id == event_id)
            result = await session.execute(stmt)
            event = result.scalars().first()
            if event is None:
                raise EventNotFoundError(event_id)
            return event

    async def add(
        self,
        user_id: int,
        title: str,
        image: str,
        description: str,
        tags: List[str],
        location: str,
    ) -> Event:
        async with self._session_factory() as session:
            event = Event(
                user_id=user_id,
                title=title,
                image=image,
                description=description,
                tags=tags,
                location=location,
            )
            session.add(event)
            await session.commit()
            await session.refresh(event)

        return event

    async def update_event(self, event: Event) -> Event:
        async with self._session_factory() as session:
            session.add(event)
            await session.commit()
            await session.refresh(event)
        return event

    async def delete_by_id(self, event_id: int) -> None:
        async with self._session_factory() as session:
            stmt = select(Event).where(Event.id == event_id)
            result = await session.execute(stmt)
            foundEvent = result.scalars().first()
            if foundEvent is None:
                raise EventNotFoundError(event_id)
            await session.delete(foundEvent)
            await session.commit()
