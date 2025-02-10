import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.transactions.enrich_transactions import EnrichTransactions

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import TransactionModel


logger = logging.getLogger(name="transactions")


class GetTransactionsByAccountId(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_transactions: EnrichTransactions,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.enrich_transactions = enrich_transactions
        self.transactions_repository = transactions_repository

    async def __call__(self, account_id: int) -> List[TransactionModel]:
        async with self.transactions_repository.transaction():
            transactions: List[TransactionModel] = await self.transactions_repository. \
                get_transactions_by_account_id(account_id)

        result = await self.enrich_transactions(transactions)
        return result
