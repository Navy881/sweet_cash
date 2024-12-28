import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.enrich_events_participants import EnrichEventsParticipants
from sweet_cash.services.events.send_events_notifications import SendEventsNotifications

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import (
    EventsParticipantsModel,
    UpdateEventsParticipantsModel,
    EventParticipantRole
)
from sweet_cash.types.notifications_events import ParticipantsGotRoleData

from sweet_cash.errors import APIConflict, APIValueNotFound


logger = logging.getLogger(name="events")


class UpdateEventParticipant(BaseService):
    def __init__(self, user_id: int,
                 enrich_events_participants: EnrichEventsParticipants,
                 events_repository: EventsRepository,
                 events_sender: SendEventsNotifications) -> None:
        self.user_id = user_id
        self.enrich_events_participants = enrich_events_participants
        self.events_repository = events_repository
        self.events_sender = events_sender

    async def __call__(self,
                       event_participant_id: int,
                       event_participants: UpdateEventsParticipantsModel
                       ) -> EventsParticipantsModel:
        async with self.events_repository.transaction():
            # Checking participant exist
            event_participant = await self.events_repository. \
                get_events_participant_by_id(event_participant_id)

            if event_participant is None:
                raise APIValueNotFound(f'Event participant {event_participant_id} not found')

            event_id: int = event_participant.event_id

            # Checking that requests user is user from requests
            if self.user_id == event_participant.user_id:
                raise APIConflict(f'User {self.user_id} is trying to update his participant {event_participant_id}')

            # Checking that requests user is the event manager
            user_events_participants: List[EventsParticipantsModel] = await self.events_repository. \
                get_events_participants_by_user_and_event(event_id=event_participant.event_id,
                                                          user_id=self.user_id,
                                                          accepted=True)
            if EventParticipantRole.MANAGER not in [participant.role for participant in user_events_participants]:
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

            event_participant: EventsParticipantsModel = await self.events_repository. \
                update_events_participant(event_participant_id=event_participant_id,
                                          event_participant=event_participants)

        # Update user model for event_participant
        await self.enrich_events_participants([event_participant])

        # Send notification event to kafka
        event_data = ParticipantsGotRoleData(
            user_id=event_participant.user_id,
            event_id=event_id,
            role=event_participant.role
        )
        await self.events_sender(event_id=event_id, event_data=event_data)

        return event_participant