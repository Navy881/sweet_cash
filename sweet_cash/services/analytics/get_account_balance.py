import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.account.get_available_accounts_by_ids import GetAvailableAccountsByIdsInternal
from sweet_cash.services.transactions.get_transactions_by_account_id import GetTransactionsByAccountId

from sweet_cash.types.analytics_types import AccountBalanceModel
from sweet_cash.types.accounts_types import AccountModel
from sweet_cash.types.transactions_types import TransactionModel, TransactionType

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="accounts")


class GetAccountBalance(BaseService):
    def __init__(self,
                 user_id: int,
                 get_available_accounts_by_ids: GetAvailableAccountsByIdsInternal,
                 get_transactions_by_account_id: GetTransactionsByAccountId) -> None:
        self.user_id = user_id
        self.get_available_accounts_by_ids = get_available_accounts_by_ids
        self.get_transactions_by_account_id = get_transactions_by_account_id

    async def __call__(self, account_id: int) -> AccountBalanceModel:
        accounts: Dict[int, AccountModel] = await self.get_available_accounts_by_ids(account_ids=[account_id],
                                                                                     with_blocked=True)
        if account_id not in accounts.keys():
            raise APIValueNotFound(f'Account {account_id} not found')

        balance: float = 0
        transactions: List[TransactionModel] = await self.get_transactions_by_account_id(account_id)
        for transaction in transactions:
            if transaction.type == TransactionType.INCOME and account_id == transaction.target_account_id:
                balance += transaction.amount
                print(f'transaction id: {transaction.id}, + {transaction.amount}, balance: {balance}')
            if transaction.type == TransactionType.EXPENSE and account_id == transaction.source_account_id:
                balance -= transaction.amount
                print(f'transaction id: {transaction.id}, - {transaction.amount}, balance: {balance}')
            if transaction.type == TransactionType.TRANSFER:
                if account_id == transaction.target_account_id:
                    balance += transaction.amount
                    print(f'transaction id: {transaction.id}, + {transaction.amount}, balance: {balance}')
                if account_id == transaction.source_account_id:
                    balance -= transaction.amount
                    print(f'transaction id: {transaction.id}, - {transaction.amount}, balance: {balance}')

        return AccountBalanceModel(balance=balance)
