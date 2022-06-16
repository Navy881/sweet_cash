
import logging
from fastapi import APIRouter, Depends
from typing import List

from sweet_cash.api.dependencies.receipts_dependencies import (
    create_receipt_dependency,
    get_receipts_dependency
)
from sweet_cash.api.services.receipts.create_receipt_by_qr import CreateReceiptByQr
from sweet_cash.api.services.receipts.get_receipt import GetReceipts
from sweet_cash.api.types.receipts_types import ReceiptModel, CreateReceiptModel
from sweet_cash.api.auth.auth_bearer import JWTBearer


logger = logging.getLogger(name="receipts")

receipts_api_router = APIRouter()


@receipts_api_router.post("/receipts/qr",
                          response_model=ReceiptModel,
                          dependencies=[Depends(JWTBearer())],
                          tags=["Receipts"])
async def create_receipt_by_qr(
        body: CreateReceiptModel,
        create_receipt_by_qr_: CreateReceiptByQr = Depends(dependency=create_receipt_dependency)
) -> ReceiptModel:
    return await create_receipt_by_qr_(body)


@receipts_api_router.get("/receipts",
                         response_model=List[ReceiptModel],
                         dependencies=[Depends(JWTBearer())],
                         tags=["Receipts"])
async def get_receipts(
        receipts_ids: str,
        get_receipts_: GetReceipts = Depends(dependency=get_receipts_dependency)
) -> List[ReceiptModel]:
    return await get_receipts_(receipts_ids)


# from flask import request, Blueprint
# import logging
#
# from api.api import SuccessResponse, auth, jsonbody, features, formatting
# from api.services.receipts.create_receipt_by_qr import CreateReceiptByQr
#
# logger = logging.getLogger(name="receipts")
#
# receipts_api = Blueprint('receipts', __name__)
#
#
# @receipts_api.route('/receipts/qr', methods=['POST'])
# @auth()
# @jsonbody(event_id=features(type=int, required=True),
#           qr=features(type=str, required=True))
# def save_receipt(event_id: int, qr: str, create_receipt_by_qr=CreateReceiptByQr()):
#     result = formatting(create_receipt_by_qr(user_id=getattr(request, "user_id"),
#                                              event_id=event_id,
#                                              qr=qr))
#     return SuccessResponse(result)
