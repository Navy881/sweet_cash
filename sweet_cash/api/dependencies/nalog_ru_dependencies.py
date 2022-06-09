
from fastapi import Request
from pydantic import AnyHttpUrl, PositiveInt

from api.repositories.users_repository import UsersRepository
from api.repositories.nalog_ru_sessions_repository import NalogRuSessionsRepository
from api.integrations.nalog_ru_api import NalogRuApi
from api.services.nalog_ru.send_otp import SendOtp
from api.services.nalog_ru.verify_otp import VerifyOtp
from settings import Settings
from db import engine


def user_repository_dependency(request: Request) -> UsersRepository:
    pg_engine = request
    return UsersRepository()


def nalog_ru_sessions_repository_dependency(request: Request) -> NalogRuSessionsRepository:
    pg_engine = request
    return NalogRuSessionsRepository()


def nalog_ru_api_dependency() -> NalogRuApi:
    nalog_ru_timeout: PositiveInt = 600
    nalog_ru_url: AnyHttpUrl = Settings.NALOG_RU_HOST
    return NalogRuApi(timeout=nalog_ru_timeout, url=nalog_ru_url)


def send_otp_dependency(request: Request) -> SendOtp:
    return SendOtp(
        user_id=getattr(request, "user_id"),
        user_repository=user_repository_dependency(request),
        nalog_ru_api=nalog_ru_api_dependency()
    )


def verify_otp_dependency(request: Request) -> VerifyOtp:
    return VerifyOtp(
        user_id=getattr(request, "user_id"),
        user_repository=user_repository_dependency(request),
        nalog_ru_sessions_repository=nalog_ru_sessions_repository_dependency(request),
        nalog_ru_api=nalog_ru_api_dependency()
    )
