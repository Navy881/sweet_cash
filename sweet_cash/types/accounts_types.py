
from __future__ import annotations

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

from sweet_cash.types.users_types import UserModel, UserResponseModel


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
    created_at: datetime
    updated_at: Optional[datetime]
    name: str
    description: Optional[str]
    is_blocked: bool
    user: Optional[UserResponseModel]
    admitted_users: Optional[List[UserResponseModel]]


class AccountResponseTinyModel(BaseModel):
    id: int
    name: str
    description: Optional[str]
    is_blocked: bool
    user: Optional[UserResponseModel]


class CreateAccountModel(BaseModel):
    name: str
    description: Optional[str]


class UpdateAccountModel(BaseModel):
    name: str
    description: Optional[str]
    is_blocked: bool