
from fastapi import Request

from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.repositories.nalog_ru_sessions_repository import NalogRuSessionsRepository
from sweet_cash.integrations.nalog_ru_api import NalogRuApi
from sweet_cash.services.nalog_ru.send_otp import SendOtp
from sweet_cash.services.nalog_ru.verify_otp import VerifyOtp


async def user_repository_dependency(request: Request) -> UsersRepository:
    engine = request.app.state.db
    return UsersRepository(engine)


async def nalog_ru_sessions_repository_dependency(request: Request) -> NalogRuSessionsRepository:
    engine = request.app.state.db
    return NalogRuSessionsRepository(engine)


async def nalog_ru_api_dependency(request: Request) -> NalogRuApi:
    session = request.app.state.session
    settings = request.app.state.settings
    return NalogRuApi(session=session,
                      timeout=settings.NALOG_RU_TIMEOUT,
                      url=settings.NALOG_RU_HOST)


async def send_otp_dependency(request: Request) -> SendOtp:
    return SendOtp(
        user_id=getattr(request, "user_id"),
        user_repository = await user_repository_dependency(request),
        nalog_ru_api = await nalog_ru_api_dependency(request)
    )


async def verify_otp_dependency(request: Request) -> VerifyOtp:
    return VerifyOtp(
        user_id=getattr(request, "user_id"),
        user_repository = await user_repository_dependency(request),
        nalog_ru_sessions_repository = await nalog_ru_sessions_repository_dependency(request),
        nalog_ru_api = await nalog_ru_api_dependency(request)
    )
