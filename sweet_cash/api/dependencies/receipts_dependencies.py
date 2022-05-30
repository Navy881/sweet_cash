
from fastapi import Request

from api.repositories.receipts_repository import ReceiptsRepository
from api.repositories.transactions_repository import TransactionsRepository
from api.services.receipts.create_receipt_by_qr import CreateReceiptByQr
from api.services.receipts.get_receipt import GetReceipts
from db import engine


def receipts_repository_dependency(request: Request) -> ReceiptsRepository:
    pg_engine = request
    return ReceiptsRepository()


def transactions_repository_dependency(request: Request) -> TransactionsRepository:
    pg_engine = request
    return TransactionsRepository()


def create_receipt_dependency(request: Request) -> CreateReceiptByQr:
    return CreateReceiptByQr(
        user_id=getattr(request, "user_id"),
        receipts_repository=receipts_repository_dependency(request),
        transactions_repository=transactions_repository_dependency(request)
    )


def get_receipts_dependency(request: Request) -> GetReceipts:
    return GetReceipts(
        user_id=getattr(request, "user_id"),
        receipts_repository=receipts_repository_dependency(request)
    )
