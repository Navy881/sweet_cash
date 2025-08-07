import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.transactions.enrich_transactions import EnrichTransactions
from sweet_cash.services.account.get_available_accounts_by_ids import GetAvailableAccountsByIdsInternal

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import TransactionModel
from sweet_cash.types.accounts_types import AccountModel
from sweet_cash.errors import APIParamError, APIValueNotFound


logger = logging.getLogger(name="transactions")


class GetTransactionsByAccount(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_transactions: EnrichTransactions,
                 get_available_accounts_by_ids: GetAvailableAccountsByIdsInternal,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.enrich_transactions = enrich_transactions
        self.get_available_accounts_by_ids = get_available_accounts_by_ids
        self.transactions_repository = transactions_repository

    async def __call__(self, account_id: int, start: str, end: str, limit: int, offset: int) -> List[TransactionModel]:
        if limit > 100:
            raise APIParamError(f'Limit value must be less than or equal to 100')

        transactions: List[TransactionModel]

        accounts: Dict[int, AccountModel] = await self.get_available_accounts_by_ids(account_ids=[account_id],
                                                                                     with_blocked=True)
        if account_id not in accounts.keys():
            raise APIValueNotFound(f'Account {account_id} not found')

        async with self.transactions_repository.transaction():
            transactions: List[TransactionModel] = await self.transactions_repository. \
                get_transactions_by_account_id_page(account_id=account_id,
                                                    start=start,
                                                    end=end,
                                                    limit=limit,
                                                    offset=offset)

            result = await self.enrich_transactions(transactions)
            return result
