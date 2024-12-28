import logging
from fastapi import APIRouter, Depends
from typing import List

from sweet_cash.dependencies.receipts_dependencies import (
    get_receipts_dependency,
    create_receipt_dependency
)
from sweet_cash.services.receipts.create_receipt_by_qr import CreateReceiptByQr
from sweet_cash.services.receipts.get_receipt import GetReceipts
from sweet_cash.types.receipts_types import ReceiptModel, CreateReceiptModel
from sweet_cash.auth.auth_bearer import JWTBearer


logger = logging.getLogger(name="receipts")

receipts_api_router = APIRouter()


@receipts_api_router.get("/receipts",
                         response_model=List[ReceiptModel],
                         dependencies=[Depends(JWTBearer())],
                         tags=["Receipts"])
async def get_receipts(
        receipts_ids: str,
        get_receipts_: GetReceipts = Depends(dependency=get_receipts_dependency)
) -> List[ReceiptModel]:
    return await get_receipts_(receipts_ids)


receipts_api_router_v2 = APIRouter()


@receipts_api_router_v2.post("/receipts/qr",
                          response_model=ReceiptModel,
                          dependencies=[Depends(JWTBearer())],
                          tags=["Receipts"])
async def create_receipt_by_qr_v2(
        body: CreateReceiptModel,
        create_receipt_by_qr_: CreateReceiptByQr = Depends(dependency=create_receipt_dependency)
) -> ReceiptModel:
    return await create_receipt_by_qr_(body)