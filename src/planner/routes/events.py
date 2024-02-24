from typing import Dict, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from planner.database import get_db_session
from planner.models.events import Event
from planner.schemas.events import Event as EventSchema
from planner.schemas.events import EventUpdate as EventUpdateSchema

event_router = APIRouter(tags=["Events"])


@event_router.get("/", response_model=List[EventSchema])
async def retrieve_all_events(
    session: AsyncSession = Depends(get_db_session),
) -> List[Event]:
    stmt = select(Event)
    result = await session.execute(stmt)
    events = result.scalars().all()
    return list(events)


@event_router.get("/{event_id}", response_model=EventSchema)
async def retrieve_event(
    event_id: int,
    session: AsyncSession = Depends(get_db_session),
) -> Event:
    stmt = select(Event).where(Event.id == event_id)
    result = await session.execute(stmt)
    event = result.scalar()
    if event:
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.post("/")
async def create_event(
    event_data: EventSchema = Body(...), session: AsyncSession = Depends(get_db_session)
) -> Dict[str, str]:
    new_event = Event(**event_data.dict())
    session.add(new_event)
    await session.commit()
    await session.refresh(new_event)

    return {"message": "Event created successfully"}


@event_router.patch("/{event_id}", response_model=EventSchema)
async def update_event(
    event_id: int,
    new_data: EventUpdateSchema,
    session: AsyncSession = Depends(get_db_session),
) -> Event:
    stmt = select(Event).where(Event.id == event_id)
    result = await session.execute(stmt)
    event = result.scalars().first()
    if event:
        event_data = new_data.dict(exclude_unset=True)
        for key, value in event_data.items():
            setattr(event, key, value)
        session.add(event)
        await session.commit()
        await session.refresh(event)
        return event

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.delete("/{event_id}")
async def delete_event(
    event_id: int, session: AsyncSession = Depends(get_db_session)
) -> Dict[str, str]:
    event = session.get(Event, event_id)
    if event:
        await session.delete(event)
        await session.commit()
        return {"message": "Event deleted successfully"}

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID doeest not exist",
    )
