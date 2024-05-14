
from fastapi import Request

from sweet_cash.repositories.receipts_repository import ReceiptsRepository
from sweet_cash.repositories.transactions_repository import TransactionsRepository
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.repositories.nalog_ru_sessions_repository import NalogRuSessionsRepository
from sweet_cash.services.receipts.create_receipt_by_qr import CreateReceiptByQr
from sweet_cash.services.receipts.get_receipt import GetReceipts
from sweet_cash.integrations.nalog_ru_api import NalogRuApi


async def nalog_ru_sessions_repository_dependency(request: Request) -> NalogRuSessionsRepository:
    engine = request.app.state.db
    return NalogRuSessionsRepository(engine)


async def events_participants_repository_dependency(request: Request) -> EventsParticipantsRepository:
    engine = request.app.state.db
    return EventsParticipantsRepository(engine)


async def receipts_repository_dependency(request: Request) -> ReceiptsRepository:
    engine = request.app.state.db
    return ReceiptsRepository(engine)


async def transactions_repository_dependency(request: Request) -> TransactionsRepository:
    engine = request.app.state.db
    return TransactionsRepository(engine)


async def nalog_ru_api_dependency(request: Request) -> NalogRuApi:
    session = request.app.state.session
    settings = request.app.state.settings
    return NalogRuApi(session=session,
                      timeout=settings.NALOG_RU_TIMEOUT,
                      url=settings.NALOG_RU_HOST)


async def create_receipt_dependency(request: Request) -> CreateReceiptByQr:
    return CreateReceiptByQr(
        user_id=getattr(request, "user_id"),
        nalog_ru_sessions_repository = await nalog_ru_sessions_repository_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request),
        receipts_repository = await receipts_repository_dependency(request),
        transactions_repository = await transactions_repository_dependency(request),
        nalog_ru_api = await nalog_ru_api_dependency(request)
    )


async def get_receipts_dependency(request: Request) -> GetReceipts:
    return GetReceipts(
        user_id=getattr(request, "user_id"),
        receipts_repository = await receipts_repository_dependency(request)
    )
