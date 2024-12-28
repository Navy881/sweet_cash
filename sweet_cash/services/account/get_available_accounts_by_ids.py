import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.account.enrich_accounts import EnrichAccounts

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import AccountModel

from sweet_cash.utils import ids2list


logger = logging.getLogger(name="accounts")


class GetAvailableAccountsByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_accounts: EnrichAccounts,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.enrich_accounts = enrich_accounts
        self.accounts_repository = accounts_repository

    async def __call__(self, account_ids, with_blocked: bool = False) -> List[AccountModel]:
        if isinstance(account_ids, str):
            account_ids: List[id] = ids2list(account_ids)

        async with self.accounts_repository.transaction():
            accounts: List[AccountModel] = await self.accounts_repository \
                .get_available_accounts_by_ids(
                    user_id=self.user_id,
                    account_ids=account_ids,
                    with_blocked=with_blocked
                )

            await self.enrich_accounts(accounts)
            return accounts


class GetAvailableAccountsByIdsInternal(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_accounts: EnrichAccounts,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.enrich_accounts = enrich_accounts
        self.accounts_repository = accounts_repository

    async def __call__(self, account_ids, with_blocked: bool = False) -> Dict[int, AccountModel]:
        if isinstance(account_ids, str):
            account_ids: List[id] = ids2list(account_ids)

        async with self.accounts_repository.transaction():
            accounts: List[AccountModel] = await self.accounts_repository \
                .get_available_accounts_by_ids(
                    user_id=self.user_id,
                    account_ids=account_ids,
                    with_blocked=with_blocked
                )
            await self.enrich_accounts(accounts)
            return {account.id: account for account in accounts}