
from fastapi import Request

from sweet_cash.repositories.notifications_events_repository import NotificationsEventsRepository
from sweet_cash.services.notifications_events.send_partisipant_added_event import SendPartisipantAddedEvent
from sweet_cash.services.notifications_events.send_partisipant_got_role_event import SendPartisipantGotRoleEvent
from sweet_cash.repositories.events_repository import EventsRepository
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository


async def notifications_events_repository_dependency(request: Request) -> NotificationsEventsRepository:
    producer = request.app.state.kafka
    return NotificationsEventsRepository(producer)


async def send_partisipant_added_event_dependency(
        request: Request, 
        events_repository: EventsRepository, 
        events_participants_repository: EventsParticipantsRepository
        ) -> SendPartisipantAddedEvent:
    return SendPartisipantAddedEvent(
        user_id=getattr(request, "user_id"),
        events_repository = await events_repository,
        events_participants_repository = await events_participants_repository,
        notifications_events_repository = await notifications_events_repository_dependency(request)
    )


async def send_partisipant_got_role_event_dependency(
        request: Request, 
        events_repository: EventsRepository, 
        events_participants_repository: EventsParticipantsRepository
        ) -> SendPartisipantGotRoleEvent:
    return SendPartisipantGotRoleEvent(
        user_id=getattr(request, "user_id"),
        events_repository = await events_repository,
        events_participants_repository = await events_participants_repository,
        notifications_events_repository = await notifications_events_repository_dependency(request)
    )