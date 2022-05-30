
from fastapi import Request

from api.repositories.events_repository import EventsRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.repositories.users_repository import UsersRepository
from api.services.events.create_event import CreateEvent
from api.services.events.get_events import GetEvents
from api.services.events.get_events_by_role import GetEventsByRole
from api.services.events.get_events_invitations import GetEventsInvitations
from api.services.events.update_event import UpdateEvent
from api.services.events.create_event_participant import CreateEventParticipant
from api.services.events.update_event_participant import UpdateEventParticipant
from api.services.events.confirm_event_participant import ConfirmEventParticipant
from api.services.events.reject_event_participant import RejectEventParticipant
from db import engine


def events_repository_dependency(request: Request) -> EventsRepository:
    pg_engine = request
    return EventsRepository()


def events_participants_repository_dependency(request: Request) -> EventsParticipantsRepository:
    pg_engine = request
    return EventsParticipantsRepository()


def users_repository_dependency(request: Request) -> UsersRepository:
    pg_engine = request
    return UsersRepository()


def create_event_dependency(request: Request) -> CreateEvent:
    return CreateEvent(
        user_id=getattr(request, "user_id"),
        events_repository=events_repository_dependency(request),
        events_participants_repository=events_participants_repository_dependency(request)
    )


def get_events_dependency(request: Request) -> GetEvents:
    return GetEvents(
        user_id=getattr(request, "user_id"),
        events_repository=events_repository_dependency(request),
        events_participants_repository=events_participants_repository_dependency(request)
    )


def get_events_by_role_dependency(request: Request) -> GetEventsByRole:
    return GetEventsByRole(
        user_id=getattr(request, "user_id"),
        events_repository=events_repository_dependency(request),
        events_participants_repository=events_participants_repository_dependency(request)
    )


def get_events_invitations_dependency(request: Request) -> GetEventsInvitations:
    return GetEventsInvitations(
        user_id=getattr(request, "user_id"),
        events_repository=events_repository_dependency(request),
        events_participants_repository=events_participants_repository_dependency(request)
    )


def update_event_dependency(request: Request) -> UpdateEvent:
    return UpdateEvent(
        user_id=getattr(request, "user_id"),
        events_repository=events_repository_dependency(request),
        events_participants_repository=events_participants_repository_dependency(request)
    )


def create_event_participant_dependency(request: Request) -> CreateEventParticipant:
    return CreateEventParticipant(
        user_id=getattr(request, "user_id"),
        users_repository=users_repository_dependency(request),
        events_participants_repository=events_participants_repository_dependency(request)
    )


def update_event_participant_dependency(request: Request) -> UpdateEventParticipant:
    return UpdateEventParticipant(
        user_id=getattr(request, "user_id"),
        events_participants_repository=events_participants_repository_dependency(request)
    )


def confirm_event_participant_dependency(request: Request) -> ConfirmEventParticipant:
    return ConfirmEventParticipant(
        user_id=getattr(request, "user_id"),
        events_participants_repository=events_participants_repository_dependency(request)
    )


def reject_event_participant_dependency(request: Request) -> RejectEventParticipant:
    return RejectEventParticipant(
        user_id=getattr(request, "user_id"),
        events_participants_repository=events_participants_repository_dependency(request)
    )
