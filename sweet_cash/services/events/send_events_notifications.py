import logging
from typing import List, Union

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.notifications_events.send_event import SendEvent

from sweet_cash.repositories.events_repository import EventsRepository

from sweet_cash.types.notifications_events import EventType, ParticipantsAddedData, ParticipantsGotRoleData
from sweet_cash.types.events_types import EventsParticipantsModel


logger = logging.getLogger(name="notifications events sending")


class SendEventsNotifications(BaseService):
    def __init__(self,
                 user_id: int,
                 send_event: SendEvent,
                 events_repository: EventsRepository) -> None:
        self.user_id = user_id
        self.send_event = send_event
        self.events_repository = events_repository

    async def __call__(self,
                       event_id: int,
                       event_data: Union[
                           ParticipantsAddedData,
                           ParticipantsGotRoleData
                       ]
                       ) -> None:

        event_type = None
        if isinstance(event_data, ParticipantsAddedData):
            event_type = EventType.PARTICIPANT_ADDED.value
        elif isinstance(event_data, ParticipantsGotRoleData):
            event_type = EventType.PARTICIPANT_GOT_ROLE.value

        event_participants: List[EventsParticipantsModel]

        async with self.events_repository.transaction():
            events_participants: List[EventsParticipantsModel] = await self.events_repository. \
                get_events_participants_by_event(event_id=event_id)

        for participant in events_participants:
            await self.send_event(event_type=event_type,
                                  for_user_id=participant.user_id,
                                  event_data=event_data)
