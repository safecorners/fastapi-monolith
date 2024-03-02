from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status

from planner.containers import Container
from planner.exceptions import NotFoundError
from planner.models import Event
from planner.schemas.event import Event as EventResponse
from planner.services import EventService

event_router = APIRouter(tags=["Event"])


@event_router.get("/events", response_model=List[EventResponse])
@inject
def get_events(
    event_service: EventService = Depends(Provide[Container.event_service]),
) -> List[Event]:
    raise NotImplementedError


@event_router.get("/events/{event_id}", response_model=EventResponse)
@inject
def get_event_by_id(
    event_id: int,
    event_service: EventService = Depends(Provide[Container.event_service]),
) -> Event:
    raise NotImplementedError


@event_router.post(
    "/events/", status_code=status.HTTP_201_CREATED, response_model=EventResponse
)
@inject
def add_event(
    event_service: EventService = Depends(Provide[Container.event_service]),
) -> Event:
    raise NotImplementedError


@event_router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove_event(
    event_id: int,
    event_service: EventService = Depends(Provide[Container.event_service]),
) -> Response:
    try:
        event_service.delete_event_by_id(event_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
