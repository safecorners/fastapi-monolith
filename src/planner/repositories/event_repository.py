from contextlib import AbstractContextManager
from typing import Callable, List, Optional

from sqlalchemy.orm import Session

from planner.exceptions import EventNotFoundError
from planner.models import Event


class EventRepository:
    def __init__(
        self, session_factory: Callable[..., AbstractContextManager[Session]]
    ) -> None:
        self._session_factory = session_factory

    def get_all(self) -> List[Event]:
        with self._session_factory() as session:
            return session.query(Event).all()

    def get_by_id(self, event_id: int) -> Event:
        with self._session_factory() as session:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
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
            foundEvent: Optional[Event] = (
                session.query(Event).filter(Event.id == event_id).first()
            )
            if not foundEvent:
                raise EventNotFoundError(event_id)
            session.delete(foundEvent)
            session.commit()
