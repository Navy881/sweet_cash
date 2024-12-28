import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.account.enrich_accounts import EnrichAccounts

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import AccountModel


logger = logging.getLogger(name="accounts")


class GetAvailableAccountsByUser(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_accounts: EnrichAccounts,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.enrich_accounts = enrich_accounts
        self.accounts_repository = accounts_repository

    async def __call__(self, with_blocked: bool = False) -> List[AccountModel]:
        async with self.accounts_repository.transaction():
            users_accounts: List[AccountModel] = await self.accounts_repository. \
                get_available_accounts_by_user_id(user_id=self.user_id, with_blocked=with_blocked)

            await self.enrich_accounts(users_accounts)
            return users_accounts
