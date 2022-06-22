
import logging
from fastapi import APIRouter, Depends
from typing import List

from sweet_cash.dependencies.events_dependencies import (
    create_event_dependency,
    get_events_dependency,
    get_events_by_role_dependency,
    get_events_invitations_dependency,
    update_event_dependency,
    create_event_participant_dependency,
    update_event_participant_dependency,
    confirm_event_participant_dependency,
    reject_event_participant_dependency
    )
from sweet_cash.services.events.create_event import CreateEvent
from sweet_cash.services.events.get_events import GetEvents
from sweet_cash.services.events.get_events_by_role import GetEventsByRole
from sweet_cash.services.events.get_events_invitations import GetEventsInvitations
from sweet_cash.services.events.update_event import UpdateEvent
from sweet_cash.services.events.create_event_participant import CreateEventParticipant
from sweet_cash.services.events.update_event_participant import UpdateEventParticipant
from sweet_cash.services.events.confirm_event_participant import ConfirmEventParticipant
from sweet_cash.services.events.reject_event_participant import RejectEventParticipant
from sweet_cash.types.events_types import EventModel, CreateEventModel
from sweet_cash.types.events_participants_types import (
    EventsParticipantsModel,
    CreateEventsParticipantsModel,
    UpdateEventsParticipantsModel
)
from sweet_cash.auth.auth_bearer import JWTBearer

logger = logging.getLogger(name="events")

events_api_router = APIRouter()


@events_api_router.post("/events",
                        response_model=EventModel,
                        dependencies=[Depends(JWTBearer())],
                        tags=["Events"])
async def create_event(
        body: CreateEventModel, create_event_: CreateEvent = Depends(dependency=create_event_dependency)
) -> EventModel:
    return await create_event_(body)


@events_api_router.get("/events",
                       response_model=List[EventModel],
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def get_events(
        ids: str,
        get_events_: GetEvents = Depends(dependency=get_events_dependency)
) -> List[EventModel]:
    return await get_events_(ids)


@events_api_router.get("/events/by_role",
                       response_model=List[EventModel],
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def get_events_by_role(
        roles: str,
        get_events_: GetEventsByRole = Depends(dependency=get_events_by_role_dependency)
) -> List[EventModel]:
    return await get_events_(roles)


@events_api_router.get("/events/invitations",
                       response_model=List[EventModel],
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def get_events_invitations(
        get_events_: GetEventsInvitations = Depends(dependency=get_events_invitations_dependency)
) -> List[EventModel]:
    return await get_events_()


@events_api_router.put("/events/{event_id}",
                       response_model=EventModel,
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def update_event(
        event_id: int,
        body: CreateEventModel,
        update_event_: UpdateEvent = Depends(dependency=update_event_dependency)
) -> EventModel:
    return await update_event_(event_id, body)


@events_api_router.post("/events/{event_id}/participant",
                        response_model=EventsParticipantsModel,
                        dependencies=[Depends(JWTBearer())],
                        tags=["Events"])
async def create_events_participant(
        event_id: int,
        body: CreateEventsParticipantsModel,
        create_event_participant_: CreateEventParticipant = Depends(dependency=create_event_participant_dependency)
) -> EventsParticipantsModel:
    return await create_event_participant_(event_id, body)


@events_api_router.put("/events/participant/{participant_id}",
                       response_model=EventsParticipantsModel,
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def update_events_participant(
        participant_id: int,
        body: UpdateEventsParticipantsModel,
        update_event_participant_: UpdateEventParticipant = Depends(dependency=update_event_participant_dependency)
) -> EventsParticipantsModel:
    return await update_event_participant_(participant_id, body)


@events_api_router.put("/events/{event_id}/participant/confirm",
                       response_model=List[EventsParticipantsModel],
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def confirm_events_participant(
        event_id: int,
        confirm_event_participant_: ConfirmEventParticipant = Depends(dependency=confirm_event_participant_dependency)
) -> List[EventsParticipantsModel]:
    return await confirm_event_participant_(event_id)


@events_api_router.put("/events/{event_id}/participant/reject",
                       response_model=List[EventsParticipantsModel],
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def reject_events_participant(
        event_id: int,
        reject_event_participant_: RejectEventParticipant = Depends(dependency=reject_event_participant_dependency)
) -> List[EventsParticipantsModel]:
    return await reject_event_participant_(event_id)
