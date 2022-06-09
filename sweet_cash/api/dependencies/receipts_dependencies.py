
from fastapi import Request
from pydantic import AnyHttpUrl, PositiveInt

from api.repositories.receipts_repository import ReceiptsRepository
from api.repositories.transactions_repository import TransactionsRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.repositories.nalog_ru_sessions_repository import NalogRuSessionsRepository
from api.services.receipts.create_receipt_by_qr import CreateReceiptByQr
from api.services.receipts.get_receipt import GetReceipts
from api.integrations.nalog_ru_api import NalogRuApi
from settings import Settings
from db import engine


def nalog_ru_sessions_repository_dependency(request: Request) -> NalogRuSessionsRepository:
    pg_engine = request
    return NalogRuSessionsRepository()


def events_participants_repository_dependency(request: Request) -> EventsParticipantsRepository:
    pg_engine = request
    return EventsParticipantsRepository()


def receipts_repository_dependency(request: Request) -> ReceiptsRepository:
    pg_engine = request
    return ReceiptsRepository()


def transactions_repository_dependency(request: Request) -> TransactionsRepository:
    pg_engine = request
    return TransactionsRepository()


def nalog_ru_api_dependency() -> NalogRuApi:
    nalog_ru_timeout: PositiveInt = 600
    nalog_ru_url: AnyHttpUrl = Settings.NALOG_RU_HOST
    return NalogRuApi(timeout=nalog_ru_timeout, url=nalog_ru_url)


def create_receipt_dependency(request: Request) -> CreateReceiptByQr:
    return CreateReceiptByQr(
        user_id=getattr(request, "user_id"),
        nalog_ru_sessions_repository=nalog_ru_sessions_repository_dependency(request),
        events_participants_repository=events_participants_repository_dependency(request),
        receipts_repository=receipts_repository_dependency(request),
        transactions_repository=transactions_repository_dependency(request),
        nalog_ru_api=nalog_ru_api_dependency()
    )


def get_receipts_dependency(request: Request) -> GetReceipts:
    return GetReceipts(
        user_id=getattr(request, "user_id"),
        receipts_repository=receipts_repository_dependency(request)
    )
