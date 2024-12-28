from __future__ import annotations

import enum
from datetime import datetime
from typing import Any, Optional, Dict, List

from pydantic import BaseModel, validator

from sweet_cash.types.users_types import UserResponseModel


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
    user: Optional[UserResponseModel]


class EventModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    description: Optional[str]
    participants: Optional[List[EventsParticipantsModel]]


class CreateEventModel(BaseModel):
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    description: Optional[str]

    @validator("end")
    def validate_dates(cls, v: datetime, values: Dict[str, Any], **kwargs: Any) -> datetime:
        if v <= values["start"]:
            raise ValueError("'end' must be greater than 'start'")
        return v


class CreateEventsParticipantsModel(BaseModel):
    user_id: int
    role: EventParticipantRole


class UpdateEventsParticipantsModel(BaseModel):
    role: EventParticipantRole
