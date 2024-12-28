from fastapi import Request

from sweet_cash.repositories.receipts_repository import ReceiptsRepository

from sweet_cash.services.receipts.create_receipt_by_qr import CreateReceiptByQr
from sweet_cash.services.receipts.get_receipt import GetReceipts

from sweet_cash.dependencies.events_dependencies import get_event_participants_roles_for_user_dependency
from sweet_cash.dependencies.nalog_ru_dependencies import get_receipt_by_qr_dependency
from sweet_cash.dependencies.transactions_dependencies import create_transaction_dependency


async def receipts_repository_dependency(request: Request) -> ReceiptsRepository:
    engine = request.app.state.db
    return ReceiptsRepository(engine)


async def create_receipt_dependency(request: Request) -> CreateReceiptByQr:
    return CreateReceiptByQr(
        user_id=getattr(request, "user_id"),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        get_receipt_by_qr = await get_receipt_by_qr_dependency(request),
        create_transaction = await create_transaction_dependency(request),
        receipts_repository = await receipts_repository_dependency(request)
    )


async def get_receipts_dependency(request: Request) -> GetReceipts:
    return GetReceipts(
        user_id=getattr(request, "user_id"),
        receipts_repository = await receipts_repository_dependency(request)
    )
