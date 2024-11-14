from fastapi import Request

from sweet_cash.repositories.nalog_ru_sessions_repository import NalogRuSessionsRepository

from sweet_cash.integrations.nalog_ru_api import NalogRuApi

from sweet_cash.services.nalog_ru.send_otp import SendOtp
from sweet_cash.services.nalog_ru.verify_otp import VerifyOtp
from sweet_cash.services.nalog_ru.get_receipt_by_qr import GetReceiptByQr
from sweet_cash.services.nalog_ru.get_nalog_ru_session import GetNalogRuSession

from sweet_cash.dependencies.users_dependecies import get_user_by_id_dependency


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
        get_user_by_id = await get_user_by_id_dependency(request),
        nalog_ru_api = await nalog_ru_api_dependency(request)
    )


async def verify_otp_dependency(request: Request) -> VerifyOtp:
    return VerifyOtp(
        user_id=getattr(request, "user_id"),
        get_user_by_id=await get_user_by_id_dependency(request),
        nalog_ru_sessions_repository = await nalog_ru_sessions_repository_dependency(request),
        nalog_ru_api = await nalog_ru_api_dependency(request)
    )

async def get_receipt_by_qr_dependency(request: Request) -> GetReceiptByQr:
    return GetReceiptByQr(
        user_id=getattr(request, "user_id"),
        nalog_ru_sessions_repository = await nalog_ru_sessions_repository_dependency(request),
        nalog_ru_api = await nalog_ru_api_dependency(request)
    )

async def get_nalog_ru_session_dependency(request: Request) -> GetNalogRuSession:
    return GetNalogRuSession(
        user_id=getattr(request, "user_id"),
        nalog_ru_sessions_repository = await nalog_ru_sessions_repository_dependency(request)
    )
