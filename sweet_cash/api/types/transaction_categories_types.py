from __future__ import annotations

from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class TransactionCategoryModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    name: str
    parent_category_id: Optional[int]
    description: Optional[str]
    sub_categories: Optional[List[TransactionCategoryModel]]


class CreateTransactionCategoryModel(BaseModel):
    name: str
    parent_category_id: Optional[int]
    description: Optional[str]
