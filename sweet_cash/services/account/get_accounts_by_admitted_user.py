import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.account.get_available_accounts_by_ids import GetAvailableAccountsByIds

from sweet_cash.repositories.accounts_admitted_users_repository import AccountsAdmittedUsersRepository

from sweet_cash.types.accounts_types import AccountModel
from sweet_cash.types.accounts_admitted_users_types import AccountsAdmittedUsersModel


logger = logging.getLogger(name="accounts")


class GetAccountsByAdmittedUser(BaseService):
    def __init__(self,
                 user_id: int,
                 get_accounts_by_ids: GetAvailableAccountsByIds,
                 accounts_admitted_users_repository: AccountsAdmittedUsersRepository) -> None:
        self.user_id = user_id
        self.get_accounts_by_ids = get_accounts_by_ids
        self.accounts_admitted_users_repository = accounts_admitted_users_repository

    async def __call__(self, user_id: int, with_blocked: bool = False) -> List[AccountModel]:
        async with self.accounts_admitted_users_repository.transaction():
            accounts_admitted_users_items: List[AccountsAdmittedUsersModel] = \
                await self.accounts_admitted_users_repository.get_by_user_id(user_id)

        account_ids = [accounts_admitted_users_item.account_id
                       for accounts_admitted_users_item in accounts_admitted_users_items]

        return await self.get_accounts_by_ids(account_ids=account_ids, with_blocked=with_blocked)
