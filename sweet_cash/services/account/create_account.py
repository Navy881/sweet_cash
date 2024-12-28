import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.account.enrich_accounts import EnrichAccounts

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import CreateAccountModel, AccountModel


logger = logging.getLogger(name="accounts")


class CreateAccount(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_accounts: EnrichAccounts,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.enrich_accounts = enrich_accounts
        self.accounts_repository = accounts_repository

    async def __call__(self, account: CreateAccountModel) -> AccountModel:
        async with self.accounts_repository.transaction():
            account_model: AccountModel = await self.accounts_repository.create_account(user_id=self.user_id,
                                                                                        item=account)

            await self.enrich_accounts([account_model])
            return account_model