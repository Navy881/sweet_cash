from fastapi import Request

from sweet_cash.repositories.notifications_events_repository import NotificationsEventsRepository

from sweet_cash.services.notifications_events.send_event import SendEvent


async def notifications_events_repository_dependency(request: Request) -> NotificationsEventsRepository:
    producer = request.app.state.kafka
    return NotificationsEventsRepository(producer)


async def send_event_dependency(request: Request) -> SendEvent:
    return SendEvent(
        user_id=getattr(request, "user_id"),
        notifications_events_repository = await notifications_events_repository_dependency(request)
    )