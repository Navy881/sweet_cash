from __future__ import annotations

import enum
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, validator


class TransactionType(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class TransactionModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    number: int
    user_id: int
    event_id: int
    type: TransactionType
    category_id: int
    amount: float
    transaction_date: datetime
    description: Optional[str]
    receipt_id: Optional[int]


class CreateTransactionModel(BaseModel):
    event_id: int
    type: TransactionType
    category_id: int
    amount: float
    transaction_date: datetime
    description: Optional[str]

    @validator("amount")
    def validate_email(cls, v: float,  **kwargs: Any) -> float:
        if v < 0:
            raise ValueError("'amount' must be positive")
        return v
