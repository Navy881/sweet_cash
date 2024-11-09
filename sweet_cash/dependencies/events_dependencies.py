from fastapi import Request

from sweet_cash.repositories.events_repository import EventsRepository
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository

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
from sweet_cash.services.events.create_event_participant_for_owner import CreateEventParticipantForOwner
from sweet_cash.services.events.get_event_participants_by_event import GetEventParticipantsByEvent
from sweet_cash.services.events.get_event_participants_by_user import GetEventParticipantsByUser
from sweet_cash.services.events.get_event_participants_by_user_and_roles import GetEventParticipantsByUserAndRoles
from sweet_cash.services.events.get_event_by_id import GetEventById
from sweet_cash.services.events.send_participant_added_event import SendParticipantAddedEvent
from sweet_cash.services.events.send_participant_got_role_event import SendParticipantGotRoleEvent

from sweet_cash.dependencies.users_dependecies import get_user_by_id_dependency
from sweet_cash.dependencies.notifications_events_dependencies import send_event_dependency


async def events_repository_dependency(request: Request) -> EventsRepository:
    engine = request.app.state.db
    return EventsRepository(engine)


async def events_participants_repository_dependency(request: Request) -> EventsParticipantsRepository:
    engine = request.app.state.db
    return EventsParticipantsRepository(engine)


async def create_event_participant_dependency(request: Request) -> CreateEventParticipant:
    return CreateEventParticipant(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request),
        events_sender = await send_participant_added_event_dependency(request)
    )


async def create_event_participant_for_owner_dependency(request: Request) -> CreateEventParticipantForOwner:
    return CreateEventParticipantForOwner(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request)
    )


async def create_event_dependency(request: Request) -> CreateEvent:
    return CreateEvent(
        user_id=getattr(request, "user_id"),
        create_event_participant_for_owner = await create_event_participant_for_owner_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def get_event_participants_by_user_dependency(request: Request) -> GetEventParticipantsByUser:
    return GetEventParticipantsByUser(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request)
    )


async def get_event_participants_by_event_dependency(request: Request) -> GetEventParticipantsByEvent:
    return GetEventParticipantsByEvent(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request)
    )


async def get_events_dependency(request: Request) -> GetEventsByIds:
    return GetEventsByIds(
        user_id=getattr(request, "user_id"),
        get_event_participants_by_user = await get_event_participants_by_user_dependency(request),
        get_event_participants_by_event = await get_event_participants_by_event_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def get_event_participants_by_user_and_roles_dependency(request: Request) -> GetEventParticipantsByUserAndRoles:
    return GetEventParticipantsByUserAndRoles(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request)
    )


async def get_events_by_role_dependency(request: Request) -> GetEventsByRoles:
    return GetEventsByRoles(
        user_id=getattr(request, "user_id"),
        get_event_participants_by_user_and_roles = await get_event_participants_by_user_and_roles_dependency(request),
        get_event_participants_by_event=await get_event_participants_by_event_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def get_events_invitations_dependency(request: Request) -> GetEventsInvitations:
    return GetEventsInvitations(
        user_id=getattr(request, "user_id"),
        get_event_participants_by_user = await get_event_participants_by_user_dependency(request),
        get_event_participants_by_event = await get_event_participants_by_event_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def get_event_participants_roles_for_user_dependency(request: Request) -> GetEventParticipantsRolesForUser:
    return GetEventParticipantsRolesForUser(
        user_id=getattr(request, "user_id"),
        events_participants_repository = await events_participants_repository_dependency(request)
    )


async def update_event_dependency(request: Request) -> UpdateEvent:
    return UpdateEvent(
        user_id=getattr(request, "user_id"),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        get_event_participants_by_event = await get_event_participants_by_event_dependency(request),
        events_repository = await events_repository_dependency(request)
    )


async def update_event_participant_dependency(request: Request) -> UpdateEventParticipant:
    return UpdateEventParticipant(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request),
        events_sender = await send_participant_got_role_event_dependency(request)
    )


async def confirm_event_participant_dependency(request: Request) -> ConfirmEventParticipant:
    return ConfirmEventParticipant(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request)
    )


async def reject_event_participant_dependency(request: Request) -> RejectEventParticipant:
    return RejectEventParticipant(
        user_id=getattr(request, "user_id"),
        get_user_by_id=await get_user_by_id_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request)
    )

async def get_event_by_id_dependency(request: Request) -> GetEventById:
    return GetEventById(
        user_id=getattr(request, "user_id"),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        get_event_participants_by_event = await get_event_participants_by_event_dependency(request),
        events_repository = await events_repository_dependency(request)
    )

async def send_participant_added_event_dependency(request: Request) -> SendParticipantAddedEvent:
    return SendParticipantAddedEvent(
        user_id=getattr(request, "user_id"),
        get_event_by_id = await get_event_by_id_dependency(request),
        get_event_participants_by_event = await get_event_participants_by_event_dependency(request),
        send_event = await send_event_dependency(request)
    )


async def send_participant_got_role_event_dependency(request: Request) -> SendParticipantGotRoleEvent:
    return SendParticipantGotRoleEvent(
        user_id=getattr(request, "user_id"),
        get_event_by_id = await get_event_by_id_dependency(request),
        get_event_participants_by_event = await get_event_participants_by_event_dependency(request),
        send_event = await send_event_dependency(request)
    )
