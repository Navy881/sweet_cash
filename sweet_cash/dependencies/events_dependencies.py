from fastapi import Request

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.services.events.create_event import CreateEvent
from sweet_cash.services.events.get_events_by_ids import GetEventsByIds
from sweet_cash.services.events.get_events_by_roles import GetEventsByRoles
from sweet_cash.services.events.get_events_invitations import GetEventsInvitations
from sweet_cash.services.events.update_event import UpdateEvent
from sweet_cash.services.events.create_event_participant import CreateEventParticipant
from sweet_cash.services.events.update_event_participant import UpdateEventParticipant
from sweet_cash.services.events.confirm_event_participant import ConfirmEventParticipant
from sweet_cash.services.events.reject_event_participant import RejectEventParticipant
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser
from sweet_cash.services.events.send_events_notifications import SendEventsNotifications
from sweet_cash.services.events.enrich_events import EnrichEvents
from sweet_cash.services.events.enrich_events_participants import EnrichEventsParticipants
from sweet_cash.services.events.get_events_by_ids import GetEventsByIdsInternal

from sweet_cash.dependencies.users_dependecies import get_users_by_ids_dependency
from sweet_cash.dependencies.notifications_events_dependencies import send_event_dependency


async def events_repository_dependency(request: Request) -> EventsRepository:
    engine = request.app.state.db
    return EventsRepository(engine)


async def enrich_events_dependency(request: Request) -> EnrichEvents:
    return EnrichEvents(
        user_id=getattr(request, "user_id"),
        events_repository = await events_repository_dependency(request),
        get_users_by_ids = await get_users_by_ids_dependency(request)
    )


async def enrich_events_participants_dependency(request: Request) -> EnrichEventsParticipants:
    return EnrichEventsParticipants(
        user_id=getattr(request, "user_id"),
        events_repository = await events_repository_dependency(request),
        get_users_by_ids = await get_users_by_ids_dependency(request)
    )


async def create_event_participant_dependency(request: Request) -> CreateEventParticipant:
    return CreateEventParticipant(
        user_id=getattr(request, "user_id"),
        get_users_by_ids = await get_users_by_ids_dependency(request),
        events_repository = await events_repository_dependency(request),
        events_sender = await send_events_notifications_dependency(request)
    )


async def create_event_dependency(request: Request) -> CreateEvent:
    return CreateEvent(
        user_id=getattr(request, "user_id"),
        enrich_events = await enrich_events_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def get_events_dependency(request: Request) -> GetEventsByIds:
    return GetEventsByIds(
        user_id=getattr(request, "user_id"),
        enrich_events = await enrich_events_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def get_events_by_role_dependency(request: Request) -> GetEventsByRoles:
    return GetEventsByRoles(
        user_id=getattr(request, "user_id"),
        enrich_events = await enrich_events_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def get_events_invitations_dependency(request: Request) -> GetEventsInvitations:
    return GetEventsInvitations(
        user_id=getattr(request, "user_id"),
        enrich_events=await enrich_events_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def get_event_participants_roles_for_user_dependency(request: Request) -> GetEventParticipantsRolesForUser:
    return GetEventParticipantsRolesForUser(
        user_id=getattr(request, "user_id"),
        events_repository=await events_repository_dependency(request)
    )


async def update_event_dependency(request: Request) -> UpdateEvent:
    return UpdateEvent(
        user_id=getattr(request, "user_id"),
        enrich_events = await enrich_events_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def update_event_participant_dependency(request: Request) -> UpdateEventParticipant:
    return UpdateEventParticipant(
        user_id=getattr(request, "user_id"),
        enrich_events_participants = await enrich_events_participants_dependency(request),
        events_repository = await events_repository_dependency(request),
        events_sender = await send_events_notifications_dependency(request)
    )


async def confirm_event_participant_dependency(request: Request) -> ConfirmEventParticipant:
    return ConfirmEventParticipant(
        user_id=getattr(request, "user_id"),
        enrich_events_participants = await enrich_events_participants_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def reject_event_participant_dependency(request: Request) -> RejectEventParticipant:
    return RejectEventParticipant(
        user_id=getattr(request, "user_id"),
        enrich_events_participants = await enrich_events_participants_dependency(request),
        events_repository=await events_repository_dependency(request)
    )


async def send_events_notifications_dependency(request: Request) -> SendEventsNotifications:
    return SendEventsNotifications(
        user_id=getattr(request, "user_id"),
        send_event = await send_event_dependency(request),
        events_repository = await events_repository_dependency(request)
    )

async def get_events_by_ids_internal_dependency(request: Request) -> GetEventsByIdsInternal:
    return GetEventsByIdsInternal(
        user_id=getattr(request, "user_id"),
        events_repository = await events_repository_dependency(request)
    )