
from __future__ import annotations

from typing import Dict, Any, List
from datetime import datetime
from pydantic import BaseModel, validator

from sweet_cash.types.transactions_types import TransactionType
from sweet_cash.types.transaction_categories_types import TransactionCategoryResponseModel


class AccountBalanceModel(BaseModel):
    balance: float

class CategoriesReportRequestModel(BaseModel):
    event_id: int
    transaction_type: TransactionType
    start: datetime
    end: datetime

    @validator("end")
    def validate_dates(cls, v: datetime, values: Dict[str, Any], **kwargs: Any) -> datetime:
        if v <= values["start"]:
            raise ValueError("'end' must be greater than 'start'")
        return v

class CategoryAmountModel(BaseModel):
    category: TransactionCategoryResponseModel
    amount: float

class PeriodModel(BaseModel):
    start: datetime
    end: datetime

class CategoriesReportModel(BaseModel):
    event_id: int
    transaction_type: TransactionType
    period: PeriodModel
    categories: List[CategoryAmountModel]