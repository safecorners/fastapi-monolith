from typing import Dict, List

from fastapi import APIRouter, Body, HTTPException, status

from planner.models.events import Event

event_router = APIRouter(tags=["Events"])

events: List[Event] = []


@event_router.get("/", response_model=List[Event])
async def retrieve_all_events() -> List[Event]:
    return events


@event_router.get("/{id}", response_model=Event)
async def retrieve_event(id: int) -> Event:
    for event in events:
        if event.id == id:
            return event
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID does not exist",
    )


@event_router.post("/new")
async def create_event(event: Event = Body(...)) -> Dict[str, str]:
    events.append(event)
    return {"message": "Event created successfully"}


@event_router.delete("/{id}")
async def delete_event(id: int) -> Dict[str, str]:
    for event in events:
        if event.id == id:
            events.remove(event)
            return {"message": "Event deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Event with supplied ID doeest not exist",
    )


@event_router.delete("/")
async def delete_all_events() -> Dict[str, str]:
    events.clear()
    return {"message": "Events deleted successfully"}
