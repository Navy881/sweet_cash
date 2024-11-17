from __future__ import annotations
import enum
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, validator, root_validator

from sweet_cash.types.users_types import UserResponseModel

from sweet_cash.settings import Settings


class DebtType(enum.Enum):
    DEBIT = "Debit"
    CREDIT = "Credit"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class DebtModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    user_id: int
    user: Optional[UserResponseModel]
    type: DebtType
    amount: float
    currency: str
    percentage_rate: int
    due_date: datetime
    debtor: Optional[str]
    creditor: Optional[str]
    description: Optional[str]
    closed_at: Optional[datetime]


class DebtResponseModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    user: Optional[UserResponseModel]
    type: DebtType
    amount: float
    currency: str
    percentage_rate: int
    due_date: datetime
    debtor: Optional[str]
    creditor: Optional[str]
    description: Optional[str]
    closed_at: Optional[datetime]


class CreateDebtModel(BaseModel):
    type: DebtType
    amount: float
    currency: str
    percentage_rate: int
    due_date: datetime
    debtor: Optional[str]
    creditor: Optional[str]
    description: Optional[str]
    closed_at: Optional[datetime]

    @validator("amount")
    def validate_amount(cls, v: float, **kwargs: Any) -> float:
        if v < 0:
            raise ValueError("'amount' must be positive")
        return v

    @validator("percentage_rate")
    def validate_percentage_rate(cls, v: float, **kwargs: Any) -> float:
        if v < 0 or v > 100:
            raise ValueError("'percentage_rate' must be between 0 and 100")
        return v

    @root_validator(pre=True)
    def validate_debtor_or_creditor(cls, values):
        debt_type = values.get("type")
        debtor = values.get("debtor")
        creditor = values.get("creditor")

        if debt_type == DebtType.DEBIT.value and not debtor:
            raise ValueError("Field 'debtor' should not be empty for DEBIT debt")
        elif debt_type == DebtType.CREDIT.value and not creditor:
            raise ValueError("Field 'creditor' should not be empty for CREDIT debt")

        return values

    @validator("currency")
    def validate_currency(cls, v: str, **kwargs: Any) -> str:
        if v not in Settings.CURRENCIES.keys():
            raise ValueError("Unknown 'currency'")
        return v