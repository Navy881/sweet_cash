
from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import Union

from sweet_cash.types.events_participants_types import EventParticipantRole

class EventType(Enum):
    PARTISIPANT_ADDED = "partisipant_added"
    PARTISIPANT_GOT_ROLE = "partisipant_got_role"


@dataclass(frozen=True)
class PartisipantsAddedData:
    user_id: int
    event_id: int
    event_name: str
    role: EventParticipantRole


@dataclass(frozen=True)
class PartisipantsGotRoleData:
    user_id: int
    event_id: int
    event_name: str
    role: EventParticipantRole


@dataclass(frozen=True)
class Event:
    timestamp: datetime
    event_type: EventType
    for_user_id: int
    data: Union[PartisipantsAddedData, PartisipantsGotRoleData, None]


class KafkaTopic(str, Enum):
    notifications = "notifications"
