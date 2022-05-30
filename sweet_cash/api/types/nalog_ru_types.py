from __future__ import annotations

from pydantic import BaseModel


class NalogRuSessionModel(BaseModel):
    sessionId: str
    refresh_token: str


class OtpModel(BaseModel):
    otp: str
