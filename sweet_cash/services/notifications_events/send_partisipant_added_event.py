import logging
from datetime import datetime, timezone

from sweet_cash.repositories.notifications_events_repository import NotificationsEventsRepository
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.repositories.events_repository import EventsRepository
from sweet_cash.types.notifications_events import Event, EventType, PartisipantsAddedData
from sweet_cash.types.events_participants_types import EventParticipantRole
from sweet_cash.errors import APIValueNotFound

logger = logging.getLogger(name="notifications events sending")


class SendPartisipantAddedEvent(object):
    def __init__(self,
                 user_id: int,
                 events_repository: EventsRepository,
                 events_participants_repository: EventsParticipantsRepository,
                 notifications_events_repository: NotificationsEventsRepository) -> None:
        self.user_id = user_id
        self.events_repository = events_repository
        self.events_participants_repository = events_participants_repository
        self.notifications_events_repository = notifications_events_repository

    async def __call__(self, event_id: Event, user_id: int, role: EventParticipantRole) -> None:

        async with self.events_repository.transaction():
            events = await self.events_repository.get_events([event_id])

            if len(events) == 0:
                raise APIValueNotFound(f'Event {event_id} not found')

        event_data = PartisipantsAddedData(
            user_id=user_id,
            event_id=event_id,
            event_name=events[0].name,
            role=role
        )

        async with self.events_participants_repository.transaction():
            events_participants = await self.events_participants_repository.get_events_participants_by_event_id([event_id])

            user_ids = set(p.user_id for p in events_participants)

            for user_id in user_ids:
                
                event = Event(
                    timestamp=datetime.now(timezone.utc),
                    event_type=EventType.PARTISIPANT_ADDED.value,
                    for_user_id=user_id,
                    data=event_data
                )

                await self.notifications_events_repository.send_event(event)
