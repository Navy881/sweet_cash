
from __future__ import annotations

from pydantic import BaseModel


class AccountBalanceModel(BaseModel):
    balance: float