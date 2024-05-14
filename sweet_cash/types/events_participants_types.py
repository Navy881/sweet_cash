from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class EventParticipantRole(enum.Enum):
    MANAGER = "Manager"
    OBSERVER = "Observer"
    PARTNER = "Partner"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class EventsParticipantsModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int
    event_id: int
    role: EventParticipantRole
    accepted: bool


class CreateEventsParticipantsModel(BaseModel):
    user_id: int
    role: EventParticipantRole


class UpdateEventsParticipantsModel(BaseModel):
    role: EventParticipantRole
