from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReceiptModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int
    external_id: int


class CreateReceiptModel(BaseModel):
    event_id: int
    qr: str
