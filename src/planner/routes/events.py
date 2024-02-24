from typing import Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlmodel import Session, select

from planner.database.connection import get_session
from planner.models.events import Event
from planner.schemas.events import Event as EventSchema
from planner.schemas.events import EventUpdate as EventUpdateSchema

event_router = APIRouter(tags=["Events"])


@event_router.get("/", response_model=List[EventSchema])
async def retrieve_all_events(session: Session = Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return list(events)


@event_router.get("/{event_id}", response_model=EventSchema)
async def retrieve_event(
    event_id: int,
    session: Session = Depends(get_session),
) -> Event:
    event = session.get(Event, event_id)
    if event:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.post("/new")
async def create_event(
    new_event: EventSchema = Body(...), session: Session = Depends(get_session)
) -> Dict[str, str]:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return {"message": "Event created successfully"}


@event_router.patch("/{event_id}", response_model=EventSchema)
async def update_event(
    event_id: int, new_data: EventUpdateSchema, session: Session = Depends(get_session)
) -> Event:
    event = session.get(Event, event_id)
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        session.commit()
        session.refresh(event)
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.delete("/{event_id}")
async def delete_event(
    event_id: int, session: Session = Depends(get_session)
) -> Dict[str, str]:
    event = session.get(Event, event_id)
    if event:
        session.delete(event)
        session.commit()
        return {"message": "Event deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID doeest not exist",
    )
