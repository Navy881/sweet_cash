
from __future__ import annotations

from datetime import datetime
from pydantic import BaseModel


class AccountsAdmittedUsersModel(BaseModel):
    id: int
    created_at: datetime
    account_id: int
    user_id: int
