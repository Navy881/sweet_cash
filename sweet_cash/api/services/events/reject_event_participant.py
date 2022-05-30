
import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.types.events_participants_types import EventsParticipantsModel

logger = logging.getLogger(name="events")


class RejectEventParticipant(BaseService):
    def __init__(self, user_id: int,
                 events_participants_repository: EventsParticipantsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository

    async def __call__(self, event_id: int) -> List[EventsParticipantsModel]:
        # Get not accepted events participants
        event_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
            get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id, accepted=False)

        return await self.events_participants_repository.\
            delete_events_participants([event_participant.id for event_participant in event_participants])


# import logging
#
# from api.services.events.get_event_participant import GetEventParticipant
# from api.models.event_participants import EventParticipantsModel
#
#
# logger = logging.getLogger(name="events")
#
#
# class RejectEventParticipant(object):
#     get_event_participant = GetEventParticipant()
#
#     def __call__(self, **kwargs) -> EventParticipantsModel:
#         user_id = kwargs.get("user_id")
#         event_id = kwargs.get("event_id")
#
#         participant = self.get_event_participant(event_id=event_id, user_id=user_id, accepted=False)
#
#         participant.delete(participant_id=participant.id)
#
#         logger.info(f'User {user_id} rejected event {event_id} with role {participant.role}')
#
#         return participant
