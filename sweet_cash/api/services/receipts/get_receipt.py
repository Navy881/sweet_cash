import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.receipts_repository import ReceiptsRepository
from api.types.receipts_types import ReceiptModel
from api.utils import ids2list

logger = logging.getLogger(name="receipts")


class GetReceipts(BaseService):
    def __init__(self,
                 user_id: int,
                 receipts_repository: ReceiptsRepository) -> None:
        self.user_id = user_id
        self.receipts_repository = receipts_repository

    async def __call__(self, receipts_ids: str) -> List[ReceiptModel]:
        receipts_ids: List[id] = ids2list(receipts_ids)

        async with self.receipts_repository.transaction():
            # Get receipts
            receipts: List[ReceiptModel] = await self.receipts_repository.get_receipts(receipts_ids)
            return [receipt for receipt in receipts if receipt.user_id == self.user_id]
