import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.account.enrich_accounts import EnrichAccounts

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import UpdateAccountModel, AccountModel

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="accounts")


class UpdateAccount(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_accounts: EnrichAccounts,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.enrich_accounts = enrich_accounts
        self.accounts_repository = accounts_repository

    async def __call__(self, account_id: int, account: UpdateAccountModel) -> AccountModel:
        async with self.accounts_repository.transaction():
            account_model = await self.accounts_repository \
                .update_account(user_id=self.user_id, account_id=account_id, item=account)

            if not isinstance(account_model, AccountModel):
                raise APIValueNotFound(f'Account {account_id} not found')

            await self.enrich_accounts([account_model])
            return account_model
