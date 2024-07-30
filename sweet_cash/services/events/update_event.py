import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.events_repository import EventsRepository
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.types.events_types import EventModel, CreateEventModel
from sweet_cash.types.events_participants_types import EventsParticipantsModel, EventParticipantRole
from sweet_cash.types.users_types import UserResponseModel
from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="events")


class UpdateEvent(BaseService):
    def __init__(self,
                 user_id: int,
                 events_repository: EventsRepository,
                 events_participants_repository: EventsParticipantsRepository,
                 user_repository: UsersRepository) -> None:
        self.user_id = user_id
        self.events_repository = events_repository
        self.events_participants_repository = events_participants_repository
        self.user_repository = user_repository

    async def __call__(self, event_id: int, event: CreateEventModel) -> EventModel:
        async with self.events_participants_repository.transaction():
            # Get users events participants
            if not await self.events_participants_repository. \
                    check_exist_events_participant_by_role(user_id=self.user_id,
                                                           event_id=event_id,
                                                           role=EventParticipantRole('Manager')):
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {event_id}')

            # Get events_participants for event
            events_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
                get_events_participants_by_event_id(event_ids=[event_id])
            
        async with self.user_repository.transaction():
            for i, events_participant in enumerate(events_participants):
                user = await self.user_repository.get_by_id(events_participant.user_id)
                events_participants[i].user = UserResponseModel(**user.dict())

        async with self.events_repository.transaction():
            # Get event
            event: EventModel = await self.events_repository.update_event(event_id=event_id, event=event)

            # Addition events_participants for event
            event.participants = events_participants

            return event
