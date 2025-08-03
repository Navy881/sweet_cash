import logging
from typing import List
from datetime import datetime

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import TransactionModel, TransactionType


logger = logging.getLogger(name="transactions")


class GetTransactionsByEventAndType(BaseService):
    def __init__(self,
                 user_id: int,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.transactions_repository = transactions_repository

    async def __call__(
            self,
            event_id: int,
            start: datetime,
            end: datetime,
            transaction_type: TransactionType,
            category_ids: List[int] = None
    ) -> List[TransactionModel]:
        async with self.transactions_repository.transaction():
            transactions: List[TransactionModel] = await self.transactions_repository. \
                get_transactions_by_event_and_type(
                    event_id=event_id,
                    start=start.isoformat(),
                    end=end.isoformat(),
                    transaction_type=transaction_type,
                    category_ids=category_ids
                )

        return transactions
