import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import AccountModel


logger = logging.getLogger(name="accounts")


class GetAccountsByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.accounts_repository = accounts_repository

    async def __call__(self, account_ids: List[int]) -> Dict[int, AccountModel]:
        async with self.accounts_repository.transaction():
            accounts: List[AccountModel] = await self.accounts_repository.get_accounts_by_ids(account_ids)
            return {account.id: account for account in accounts}
