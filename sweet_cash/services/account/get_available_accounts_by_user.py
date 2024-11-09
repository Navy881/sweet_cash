import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.account.get_accounts_by_admitted_user import GetAccountsByAdmittedUser
from sweet_cash.services.users.get_user_by_id import GetUserById
from sweet_cash.services.account.get_accounts_admitted_users_by_account import GetAccountsAdmittedUsersByAccount

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import AccountModel


logger = logging.getLogger(name="accounts")


class GetAvailableAccountsByUser(BaseService):
    def __init__(self,
                 user_id: int,
                 get_accounts_by_admitted_user: GetAccountsByAdmittedUser,
                 get_user_by_id: GetUserById,
                 get_admitted_users_by_account: GetAccountsAdmittedUsersByAccount,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.get_accounts_by_admitted_user = get_accounts_by_admitted_user
        self.get_user_by_id = get_user_by_id
        self.get_admitted_users_by_account = get_admitted_users_by_account
        self.accounts_repository = accounts_repository

    async def __call__(self, with_blocked: bool = False) -> List[AccountModel]:
        async with self.accounts_repository.transaction():
            users_accounts: List[AccountModel] = await self.accounts_repository. \
                get_by_user_id(user_id=self.user_id, with_blocked=with_blocked)
            
        for i, account in enumerate(users_accounts):
            users_accounts[i].user = await self.get_user_by_id(account.user_id)
            
        # Получение account, для которых у user есть доступ
        available_external_accounts: List[AccountModel] = \
            await self.get_accounts_by_admitted_user(user_id=self.user_id, with_blocked=with_blocked)

        # Обогащение addmited_users у account
        all_accounts = users_accounts + available_external_accounts
        for i, account in enumerate(all_accounts):
            all_accounts[i].admitted_users = await self.get_admitted_users_by_account(account.id)

        return all_accounts
