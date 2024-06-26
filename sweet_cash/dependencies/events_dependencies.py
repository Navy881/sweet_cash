
from fastapi import Request

from sweet_cash.repositories.events_repository import EventsRepository
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.services.events.create_event import CreateEvent
from sweet_cash.services.events.get_events import GetEvents
from sweet_cash.services.events.get_events_by_role import GetEventsByRole
from sweet_cash.services.events.get_events_invitations import GetEventsInvitations
from sweet_cash.services.events.update_event import UpdateEvent
from sweet_cash.services.events.create_event_participant import CreateEventParticipant
from sweet_cash.services.events.update_event_participant import UpdateEventParticipant
from sweet_cash.services.events.confirm_event_participant import ConfirmEventParticipant
from sweet_cash.services.events.reject_event_participant import RejectEventParticipant


def events_repository_dependency(request: Request) -> EventsRepository:
    engine = request.app.state.db
    return EventsRepository(engine)


def events_participants_repository_dependency(request: Request) -> EventsParticipantsRepository:
    engine = request.app.state.db
    return EventsParticipantsRepository(engine)


def users_repository_dependency(request: Request) -> UsersRepository:
    engine = request.app.state.db
    return UsersRepository(engine)


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
