import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById
from sweet_cash.services.account.get_accounts_admitted_users_by_account import GetAccountsAdmittedUsersByAccount

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import UpdateAccountModel, AccountModel

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="accounts")


class UpdateAccount(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 get_admitted_users_by_account: GetAccountsAdmittedUsersByAccount,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.get_admitted_users_by_account = get_admitted_users_by_account
        self.accounts_repository = accounts_repository

    async def __call__(self, account_id: int, account: UpdateAccountModel) -> AccountModel:
        async with self.accounts_repository.transaction():
            account_model = await self.accounts_repository.get_user_account_by_id(account_id=account_id,
                                                                                  user_id=self.user_id)
            if account_model is None:
                raise APIValueNotFound(f'Account {account_id} not found')

            account_model: AccountModel = await self.accounts_repository.update_account(account_id=account_id,
                                                                                        item=account)

        account_model.user = await self.get_user_by_id(account_model.user_id)
        account_model.admitted_users = await self.get_admitted_users_by_account(account_model.id)

        return account_model
