import logging
from typing import Dict, List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_users_by_ids import GetUsersByIds
from sweet_cash.services.events.send_events_notifications import SendEventsNotifications

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.events_types import (
    EventsParticipantsModel,
    CreateEventsParticipantsModel,
    EventParticipantRole
)
from sweet_cash.types.users_types import UserModel
from sweet_cash.types.notifications_events import ParticipantsAddedData

from sweet_cash.errors import APIValueNotFound, APIParamError


logger = logging.getLogger(name="events")


class CreateEventParticipant(BaseService):
    def __init__(self, user_id: int,
                 get_users_by_ids: GetUsersByIds,
                 events_repository: EventsRepository,
                 events_sender: SendEventsNotifications) -> None:
        self.user_id = user_id
        self.get_users_by_ids = get_users_by_ids
        self.events_repository = events_repository
        self.events_sender = events_sender

    async def __call__(self, event_id: int,
                       event_participants: CreateEventsParticipantsModel) -> EventsParticipantsModel:
        user_id: int = event_participants.user_id
        role: EventParticipantRole = event_participants.role

        users: Dict[int, UserModel] = await self.get_users_by_ids([user_id])
        if user_id not in users.keys():
            raise APIValueNotFound(f'User {user_id} not found')
        user = users[user_id]

        async with self.events_repository.transaction():
            # Checking that requests user is the event manager
            user_events_participants: List[EventsParticipantsModel] = await self.events_repository. \
                get_events_participants_by_user_and_event(event_id=event_id, user_id=self.user_id, accepted=True)

            roles = [user_events_participant.role for user_events_participant in user_events_participants]

            if EventParticipantRole.MANAGER not in roles:
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

            # Checking that user is not events participant
            user_events_participants: List[EventsParticipantsModel] = await self.events_repository. \
                get_events_participants_by_user_and_event(event_id=event_id, user_id=user_id, accepted=True)

            roles = [user_events_participant.role for user_events_participant in user_events_participants]

            if role in roles:
                raise APIParamError(f'Participant with role {role.name} for user'
                                    f' {user_id} already exist in event {event_id}')

            event_participant: EventsParticipantsModel = await self.events_repository. \
                create_events_participant(event_id=event_id, event_participant=event_participants)
            
            event_participant.user = user

            # Send notification event to kafka
            event_data = ParticipantsAddedData(
                user_id=event_participant.user_id,
                event_id=event_id,
                role=event_participant.role
            )
            await self.events_sender(event_id=event_id, event_data=event_data)

        return event_participant