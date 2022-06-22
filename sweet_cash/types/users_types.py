from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, validator

from sweet_cash.utils import (
    check_email_format,
    check_phone_format,
    check_password_format
)


class UserModel(BaseModel):
    id: int
    created_at: datetime
    name: str
    email: str
    password: str
    phone: str


class CreateUserModel(BaseModel):
    id: int
    created_at: datetime
    name: str
    email: str
    phone: str


class RegisterUserModel(BaseModel):
    name: str
    email: str
    phone: str
    password: str

    @validator("email")
    def validate_email(cls, v: str,  **kwargs: Any) -> str:
        if not check_email_format(v):
            raise ValueError("Invalid email format")
        return v

    @validator("phone")
    def validate_phone(cls, v: str, **kwargs: Any) -> str:
        if not check_phone_format(v):
            raise ValueError("Invalid phone format")
        return v

    @validator("password")
    def validate_password(cls, v: str, **kwargs: Any) -> str:
        if not check_password_format(v):
            raise ValueError("Invalid password format")
        return v


class TokenModel(BaseModel):
    refresh_token: str
    user_id: int
    token: str
    expire_at: datetime


class RefreshTokenModel(BaseModel):
    refresh_token: str
    user_id: int


class LoginModel(BaseModel):
    email: str
    password: str

    @validator("email")
    def validate_email(cls, v: str,  **kwargs: Any) -> str:
        if not check_email_format(v):
            raise ValueError("Invalid email format")
        return v

    @validator("password")
    def validate_password(cls, v: str, **kwargs: Any) -> str:
        if not check_password_format(v):
            raise ValueError("Invalid password format")
        return v


class GetAccessTokenModel(BaseModel):
    refresh_token: str
