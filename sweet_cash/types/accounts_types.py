
from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from sweet_cash.types.users_types import UserResponseModel


class AccountModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    name: str
    description: Optional[str]
    user_id: int
    is_blocked: bool
    user: Optional[UserResponseModel]
    admitted_users: Optional[List[UserResponseModel]]


class AccountResponseModel(BaseModel):
    id: int
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    name: Optional[str]
    description: Optional[str]
    is_blocked: Optional[bool]
    user: Optional[UserResponseModel]
    admitted_users: Optional[List[UserResponseModel]]


class AccountResponseTinyModel(BaseModel):
    id: int
    name: Optional[str]
    description: Optional[str]
    is_blocked: Optional[bool]
    user: Optional[UserResponseModel]


class CreateAccountModel(BaseModel):
    name: str
    description: Optional[str]


class UpdateAccountModel(BaseModel):
    name: str
    description: Optional[str]
    is_blocked: bool


class AccountsAdmittedUsersModel(BaseModel):
    id: int
    created_at: datetime
    account_id: int
    user_id: int
