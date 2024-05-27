from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status

from planner.auth.authenticate import authenticate
from planner.containers import Container
from planner.exceptions import NotFoundError
from planner.models import Event
from planner.schemas.event import Event as EventResponse
from planner.schemas.event import EventUpdate
from planner.services import EventService

event_router = APIRouter(tags=["Event"])


@event_router.get("/events", response_model=List[EventResponse])
@inject
async def get_events(
    event_service: EventService = Depends(Provide[Container.event_service]),
) -> List[Event]:
    return await event_service.get_events()


@event_router.get("/events/{event_id}", response_model=EventResponse)
@inject
async def get_event_by_id(
    event_id: int,
    event_service: EventService = Depends(Provide[Container.event_service]),
) -> Event:
    try:
        return await event_service.get_event_by_id(event_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@event_router.post(
    "/events/", status_code=status.HTTP_201_CREATED, response_model=EventResponse
)
@inject
async def create_event(
    payload: EventResponse,
    username: str = Depends(authenticate),
    event_service: EventService = Depends(Provide[Container.event_service]),
) -> Event:
    try:
        return await event_service.create_event(
            username=username,
            title=payload.title,
            image=payload.image,
            description=payload.description,
            tags=payload.tags,
            location=payload.location,
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@event_router.put("/events/{event_id}", response_model=EventResponse)
@inject
async def update_event(
    event_id: int,
    payload: EventUpdate,
    event_service: EventService = Depends(Provide[Container.event_service]),
) -> Event:
    try:
        return await event_service.update_event(
            event_id=event_id,
            payload=payload,
        )
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)


@event_router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def remove_event(
    event_id: int,
    event_service: EventService = Depends(Provide[Container.event_service]),
) -> Response:
    try:
        await event_service.delete_event_by_id(event_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
