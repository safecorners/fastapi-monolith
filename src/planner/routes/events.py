from typing import Any, Callable, Dict, List, Union, cast

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status
from sqlmodel import Session, select

from planner.database.connection import get_session
from planner.models.events import Event, EventUpdate

event_router = APIRouter(tags=["Events"])

events: List[Event] = []


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events(session: Session = Depends(get_session)) -> List[Event]:
    statement = select(Event)
    events = session.exec(statement).all()
    return list(events)


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int, session: Session = Depends(get_session)) -> Event:
    event = session.get(Event, id)
    if event:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.post("/new")
async def create_event(
    new_event: Event = Body(...), session: Session = Depends(get_session)
) -> Dict[str, str]:
    session.add(new_event)
    session.commit()
    session.refresh(new_event)

    return {"message": "Event created successfully"}


@event_router.put("/edit/{id}", response_model=Event)
async def update_event(
    id: int, new_data: EventUpdate, session: Session = Depends(get_session)
) -> Event:
    event = session.get(Event, id)
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


@event_router.delete("/{id}")
async def delete_event(
    id: int, session: Session = Depends(get_session)
) -> Dict[str, str]:
    event = session.get(Event, id)
    if event:
        session.delete(event)
        session.commit()
        return {"message": "Event deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID doeest not exist",
    )


@event_router.delete("/")
async def delete_all_events() -> Dict[str, str]:
    events.clear()
    return {"message": "Events deleted successfully"}
