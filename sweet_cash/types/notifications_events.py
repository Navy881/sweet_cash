from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Union

from sweet_cash.types.events_types import EventParticipantRole

class EventType(Enum):
    PARTICIPANT_ADDED = "participant_added"
    PARTICIPANT_GOT_ROLE = "participant_got_role"


@dataclass(frozen=True)
class ParticipantsAddedData:
    user_id: int
    event_id: int
    role: EventParticipantRole


@dataclass(frozen=True)
class ParticipantsGotRoleData:
    user_id: int
    event_id: int
    role: EventParticipantRole


@dataclass(frozen=True)
class Event:
    timestamp: datetime
    event_type: EventType
    for_user_id: int
    data: Union[ParticipantsAddedData, ParticipantsGotRoleData, None]


class KafkaTopic(str, Enum):
    notifications = "notifications"
