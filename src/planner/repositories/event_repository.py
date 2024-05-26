from typing import List

from sqlalchemy import select

from planner.database import SessionFactory
from planner.exceptions import EventNotFoundError
from planner.models import Event


class EventRepository:
    def __init__(self, session_factory: SessionFactory) -> None:
        self._session_factory = session_factory

    def get_all(self) -> List[Event]:
        with self._session_factory() as session:
            stmt = select(Event)
            result = session.execute(stmt)
            events = list(result.scalars().all())
            return events

    def get_by_id(self, event_id: int) -> Event:
        with self._session_factory() as session:
            stmt = select(Event).where(Event.id == event_id)
            result = session.execute(stmt)
            event = result.scalars().first()
            if event is None:
                raise EventNotFoundError(event_id)
            return event

    def add(
        self,
        user_id: int,
        title: str,
        image: str,
        description: str,
        tags: List[str],
        location: str,
    ) -> Event:
        with self._session_factory() as session:
            event = Event(
                user_id=user_id,
                title=title,
                image=image,
                description=description,
                tags=tags,
                location=location,
            )
            session.add(event)
            session.commit()
            session.refresh(event)

        return event

    def delete_by_id(self, event_id: int) -> None:
        with self._session_factory() as session:
            stmt = select(Event).where(Event.id == event_id)
            result = session.execute(stmt)
            foundEvent = result.scalars().first()
            if foundEvent is None:
                raise EventNotFoundError(event_id)
            session.delete(foundEvent)
            session.commit()
