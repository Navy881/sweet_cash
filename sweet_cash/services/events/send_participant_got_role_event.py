import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.get_event_by_id import GetEventById
from sweet_cash.services.events.get_event_participants_by_event import GetEventParticipantsByEvent
from sweet_cash.services.notifications_events.send_event import SendEvent

from sweet_cash.types.notifications_events import EventType, ParticipantsGotRoleData
from sweet_cash.types.events_participants_types import EventsParticipantsModel, EventParticipantRole


logger = logging.getLogger(name="notifications events sending")


class SendParticipantGotRoleEvent(BaseService):
    def __init__(self,
                 user_id: int,
                 get_event_by_id: GetEventById,
                 get_event_participants_by_event: GetEventParticipantsByEvent,
                 send_event: SendEvent) -> None:
        self.user_id = user_id
        self.get_event_by_id = get_event_by_id
        self.get_event_participants_by_event = get_event_participants_by_event
        self.send_event = send_event

    async def __call__(self, event_id: int, user_id: int, role: EventParticipantRole) -> None:
        event = await self.get_event_by_id(event_id)

        event_data = ParticipantsGotRoleData(
            user_id=user_id,
            event_id=event_id,
            event_name=event.name,
            role=role
        )

        events_participants: List[EventsParticipantsModel] = await self.get_event_participants_by_event(event_id)
        for participant in events_participants:
            await self.send_event(event_type=EventType.PARTICIPANT_GOT_ROLE.value,
                                  for_user_id=participant.user_id,
                                  event_data=event_data)

        return None
