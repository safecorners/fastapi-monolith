from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status

from application.containers import Container
from application.exceptions import NotFoundError
from application.models import Event
from application.services import EventService

event_router = APIRouter(tags=["Event"])

@event_router.get("/events")
@inject
def get_events(
    event_service: EventService = Depends(Provide[Container.event_service])
) -> List[Event]:
    raise NotImplementedError

@event_router.get("/events/{event_id}")
@inject
def get_event_by_id(
    event_id: int,
    event_service: EventService = Depends(Provide[Container.event_service]) 
) -> Event:
    raise NotImplementedError

@event_router.post("/events/", status_code=status.HTTP_201_CREATED)
@inject
def add_event(event_service: EventService = Depends(Provide[Container.event_service])) -> Event:
    raise NotImplementedError

@event_router.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove_event(event_id: int, event_service: EventService = Depends(Provide[Container.event_service]),) -> Response:
    try:
        event_service.delete_event_by_id(event_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
