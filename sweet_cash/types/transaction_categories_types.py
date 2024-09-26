
from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class TransactionCategoryType(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class TransactionCategoryModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    name: str
    type: TransactionCategoryType
    parent_category_id: Optional[int]
    description: Optional[str]
    sub_categories: Optional[List[TransactionCategoryModel]]


class CreateTransactionCategoryModel(BaseModel):
    name: str
    type: TransactionCategoryType
    parent_category_id: Optional[int]
    description: Optional[str]
