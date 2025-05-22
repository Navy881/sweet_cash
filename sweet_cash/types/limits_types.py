from __future__ import annotations
from datetime import datetime
from typing import Any, Optional, Dict
from pydantic import BaseModel, validator

from sweet_cash.types.transactions_types import TransactionType
from sweet_cash.types.transaction_categories_types import TransactionCategoryResponseModel
from sweet_cash.types.users_types import UserResponseModel


class LimitModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    created_by_user_id: int
    created_by: Optional[UserResponseModel]
    start: datetime
    end: datetime
    event_id: int
    type: TransactionType
    category_id: Optional[int]
    category: Optional[TransactionCategoryResponseModel]
    amount: float
    balance: Optional[float] = 0


class LimitResponseModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: Optional[UserResponseModel]
    start: datetime
    end: datetime
    event_id: int
    type: TransactionType
    category: Optional[TransactionCategoryResponseModel]
    amount: float
    balance: Optional[float] = 0


class CreateLimitModel(BaseModel):
    start: datetime
    end: datetime
    event_id: int
    type: TransactionType
    category_id: Optional[int]
    amount: float

    @validator("end")
    def validate_dates(cls, v: datetime, values: Dict[str, Any], **kwargs: Any) -> datetime:
        if v <= values["start"]:
            raise ValueError("'end' must be greater than 'start'")
        return v

    @validator("amount")
    def validate_amount(cls, v: float, **kwargs: Any) -> float:
        if v < 0:
            raise ValueError("'amount' must be positive")
        return v


class UpdateLimitModel(BaseModel):
    start: datetime
    end: datetime
    type: TransactionType
    category_id: Optional[int]
    amount: float

    @validator("end")
    def validate_dates(cls, v: datetime, values: Dict[str, Any], **kwargs: Any) -> datetime:
        if v <= values["start"]:
            raise ValueError("'end' must be greater than 'start'")
        return v

    @validator("amount")
    def validate_amount(cls, v: float, **kwargs: Any) -> float:
        if v < 0:
            raise ValueError("'amount' must be positive")
        return v
