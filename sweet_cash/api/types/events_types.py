from __future__ import annotations

from datetime import datetime
from typing import Any, Optional, Dict

from pydantic import BaseModel, validator


class EventModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    description: Optional[str]


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
