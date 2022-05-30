import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.receipts_repository import ReceiptsRepository
from api.types.receipts_types import ReceiptModel

logger = logging.getLogger(name="receipts")


class GetReceipts(BaseService):
    def __init__(self,
                 user_id: int,
                 receipts_repository: ReceiptsRepository) -> None:
        self.user_id = user_id,
        self.receipts_repository = receipts_repository

    async def __call__(self, receipts_ids: str) -> List[ReceiptModel]:
        # TODO
        pass


# import logging
#
# from api.models.receipt import ReceiptModel
# import api.errors as error
#
# logger = logging.getLogger(name="transactions")
#
#
# class GetReceipt(object):
#
#     def __call__(self, user_id: int, receipt_id: int) -> ReceiptModel:
#         receipt = ReceiptModel.get_by_user(receipt_id=receipt_id, user_id=int(user_id))
#         if receipt is None:
#             logger.warning(f'User {user_id} is trying to get a non-existent receipt {receipt_id}')
#             raise error.APIValueNotFound(f'Receipt with id {receipt_id} not found for user {user_id}')
#
#         logger.info(f'User {user_id} got receipt {receipt_id}')
#
#         return receipt
