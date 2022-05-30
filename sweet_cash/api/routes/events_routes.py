from fastapi import APIRouter, Depends
from typing import List

from api.dependencies.events_dependencies import (
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
from api.services.events.create_event import CreateEvent
from api.services.events.get_events import GetEvents
from api.services.events.get_events_by_role import GetEventsByRole
from api.services.events.get_events_invitations import GetEventsInvitations
from api.services.events.update_event import UpdateEvent
from api.services.events.create_event_participant import CreateEventParticipant
from api.services.events.update_event_participant import UpdateEventParticipant
from api.services.events.confirm_event_participant import ConfirmEventParticipant
from api.services.events.reject_event_participant import RejectEventParticipant
from api.types.events_types import EventModel, CreateEventModel
from api.types.events_participants_types import (
    EventsParticipantsModel,
    CreateEventsParticipantsModel,
    UpdateEventsParticipantsModel
)
from api.auth.auth_bearer import JWTBearer

import logging

logger = logging.getLogger(name="events")

events_api_router = APIRouter()


@events_api_router.post("/api/v1/events",
                        response_model=EventModel,
                        dependencies=[Depends(JWTBearer())],
                        tags=["Events"])
async def create_event(
        body: CreateEventModel, create_event_: CreateEvent = Depends(dependency=create_event_dependency)
) -> EventModel:
    return await create_event_(body)


@events_api_router.get("/api/v1/events",
                       response_model=List[EventModel],
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def get_events(
        ids: str,
        get_events_: GetEvents = Depends(dependency=get_events_dependency)
) -> List[EventModel]:
    return await get_events_(ids)


@events_api_router.get("/api/v1/events/by_role",
                       response_model=List[EventModel],
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def get_events_by_role(
        roles: str,
        get_events_: GetEventsByRole = Depends(dependency=get_events_by_role_dependency)
) -> List[EventModel]:
    return await get_events_(roles)


@events_api_router.get("/api/v1/events/invitations",
                       response_model=List[EventModel],
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def get_events_invitations(
        get_events_: GetEventsInvitations = Depends(dependency=get_events_invitations_dependency)
) -> List[EventModel]:
    return await get_events_()


@events_api_router.put("/api/v1/events/{event_id}",
                       response_model=EventModel,
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def update_event(
        event_id: int,
        body: CreateEventModel,
        update_event_: UpdateEvent = Depends(dependency=update_event_dependency)
) -> EventModel:
    return await update_event_(event_id, body)


@events_api_router.post("/api/v1/events/{event_id}/participant",
                        response_model=EventsParticipantsModel,
                        dependencies=[Depends(JWTBearer())],
                        tags=["Events"])
async def create_events_participant(
        event_id: int,
        body: CreateEventsParticipantsModel,
        create_event_participant_: CreateEventParticipant = Depends(dependency=create_event_participant_dependency)
) -> EventsParticipantsModel:
    return await create_event_participant_(event_id, body)


@events_api_router.put("/api/v1/events/participant/{participant_id}",
                       response_model=EventsParticipantsModel,
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def update_events_participant(
        participant_id: int,
        body: UpdateEventsParticipantsModel,
        update_event_participant_: UpdateEventParticipant = Depends(dependency=update_event_participant_dependency)
) -> EventsParticipantsModel:
    return await update_event_participant_(participant_id, body)


@events_api_router.put("/api/v1/events/{event_id}/participant/confirm",
                       response_model=List[EventsParticipantsModel],
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def confirm_events_participant(
        event_id: int,
        confirm_event_participant_: ConfirmEventParticipant = Depends(dependency=confirm_event_participant_dependency)
) -> List[EventsParticipantsModel]:
    return await confirm_event_participant_(event_id)


@events_api_router.put("/api/v1/events/{event_id}/participant/reject",
                       response_model=List[EventsParticipantsModel],
                       dependencies=[Depends(JWTBearer())],
                       tags=["Events"])
async def reject_events_participant(
        event_id: int,
        reject_event_participant_: RejectEventParticipant = Depends(dependency=reject_event_participant_dependency)
) -> List[EventsParticipantsModel]:
    return await reject_event_participant_(event_id)

# from flask import request, Blueprint
# import logging
#
# from api.api import SuccessResponse, auth, jsonbody, query_params, features, formatting
# from api.services.events.create_event import CreateEvent
# from api.services.events.get_events import GetEvents
# from api.services.events.get_events_by_filter import GetEventsByFilter
# from api.services.events.update_event import UpdateEvent
# from api.services.events.create_event_participant import CreateEventParticipant
# from api.services.events.update_event_participant import UpdateEventParticipant
# from api.services.events.confirm_event_participant import ConfirmEventParticipant
# from api.services.events.reject_event_participant import RejectEventParticipant
#
# logger = logging.getLogger(name="events")
#
# events_api = Blueprint('events', __name__)
#
#
# @events_api.route('/api/v1/events', methods=['POST'])
# @auth()
# @jsonbody(name=features(type=str, required=True),
#           start=features(type=str),
#           end=features(type=str),
#           description=features(type=str))
# def create_event(name: str,
#                  start=None,
#                  end=None,
#                  description=None,
#                  create_event=CreateEvent()):
#     result = formatting(create_event(user_id=getattr(request, "user_id"),
#                                      name=name,
#                                      start=start,
#                                      end=end,
#                                      description=description))
#     return SuccessResponse(result)
#
#
# @events_api.route('/api/v1/events', methods=['GET'])
# @auth()
# @query_params(ids=features(type=str))
# def get_events(ids=None,
#                get_events=GetEvents()):
#     events = ч(user_id=getattr(request, "user_id"),
#                         event_ids=ids)
#     result = [formatting(item) for item in events]
#     return SuccessResponse(result)
#
#
# @events_api.route('/api/v1/events/by_filter', methods=['GET'])
# @auth()
# @query_params(role=features(type=str),
#               accepted=features(type=str))
# def get_events_by_filter(role=None,
#                          accepted=True,
#                          get_events_by_filter=GetEventsByFilter()):
#     events = get_events_by_filter(user_id=getattr(request, "user_id"),
#                                   role=role,
#                                   accepted=accepted)
#     result = [formatting(item) for item in events]
#     return SuccessResponse(result)
#
#
# @events_api.route('/api/v1/events/<int:event_id>', methods=['PUT'])
# @auth()
# @jsonbody(name=features(type=str, required=True),
#           start=features(type=str),
#           end=features(type=str),
#           description=features(type=str))
# def update_event(event_id: int,
#                  name: str,
#                  start=None,
#                  end=None,
#                  description=None,
#                  update_event=UpdateEvent()):
#     result = formatting(update_event(user_id=getattr(request, "user_id"),
#                                      event_id=event_id,
#                                      name=name,
#                                      start=start,
#                                      end=end,
#                                      description=description))
#     return SuccessResponse(result)
#
#
# @events_api.route('/api/v1/events/<int:event_id>/participant', methods=['POST'])
# @auth()
# @jsonbody(user_id=features(type=int, required=True),
#           role=features(type=str, required=True))
# def add_participant(event_id: int,
#                     user_id: int,
#                     role: str,
#                     create_participant=CreateEventParticipant()):
#     result = formatting(create_participant(request_user_id=getattr(request, "user_id"),
#                                            event_id=event_id,
#                                            user_id=user_id,
#                                            role=role))
#     return SuccessResponse(result)
#
#
# @events_api.route('/api/v1/events/<int:event_id>/participant/<int:participant_id>', methods=['PUT'])
# @auth()
# @jsonbody(role=features(type=str, required=True))
# def update_participant(event_id: int,
#                        participant_id: int,
#                        role: str,
#                        update_participant=UpdateEventParticipant()):
#     result = formatting(update_participant(user_id=getattr(request, "user_id"),
#                                            event_id=event_id,
#                                            participant_id=participant_id,
#                                            role=role))
#     return SuccessResponse(result)
#
#
# @events_api.route('/api/v1/events/<int:event_id>/participant/confirm', methods=['PUT'])
# @auth()
# def confirm_event(event_id: int,
#                   confirm_event_participant=ConfirmEventParticipant()):
#     result = formatting(confirm_event_participant(user_id=getattr(request, "user_id"),
#                                                   event_id=event_id))
#     return SuccessResponse(result)
#
#
# @events_api.route('/api/v1/events/<int:event_id>/participant/reject', methods=['PUT'])
# @auth()
# def reject_event(event_id: int,
#                  reject_event_participant=RejectEventParticipant()):
#     result = formatting(reject_event_participant(user_id=getattr(request, "user_id"),
#                                                  event_id=event_id))
#     return SuccessResponse(result)
