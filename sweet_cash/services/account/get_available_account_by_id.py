import logging
from typing import Union

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById
from sweet_cash.services.account.get_accounts_admitted_users_by_account import GetAccountsAdmittedUsersByAccount
from sweet_cash.services.account.get_accounts_admitted_user_by_account_id_and_user_id import GetAccountsAdmittedUserByAccountIdAndUserId

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import AccountModel, AccountResponseModel


logger = logging.getLogger(name="accounts")


class GetAvailableAccountById(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 get_admitted_users_by_account: GetAccountsAdmittedUsersByAccount,
                 get_admitted_user_by_account_id_and_user_id: GetAccountsAdmittedUserByAccountIdAndUserId,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.get_admitted_users_by_account = get_admitted_users_by_account
        self.get_admitted_user_by_account_id_and_user_id = get_admitted_user_by_account_id_and_user_id
        self.accounts_repository = accounts_repository

    async def __call__(self, account_id: int) -> Union[AccountModel, AccountResponseModel]:
        async with self.accounts_repository.transaction():
            account = await self.accounts_repository.get_by_id(account_id=account_id)

        if account is None:
            return AccountResponseModel(id=account_id)

        # Проверка, что user связан с account
        admitted_user = await self.get_admitted_user_by_account_id_and_user_id(account_id=account.id,
                                                                               user_id=self.user_id)
        if account.user_id != self.user_id and admitted_user is None:
            return AccountResponseModel(id=account_id)

        # Обогащение модели account
        account.user  = await self.get_user_by_id(account.user_id)
        account.admitted_users = await self.get_admitted_users_by_account(account.id)

        return account
