import logging
from typing import Optional

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.accounts_admitted_users_repository import AccountsAdmittedUsersRepository

from sweet_cash.types.accounts_admitted_users_types import AccountsAdmittedUsersModel

logger = logging.getLogger(name="accounts")


class GetAccountsAdmittedUserByAccountIdAndUserId(BaseService):
    def __init__(self,
                 user_id: int,
                 accounts_admitted_users_repository: AccountsAdmittedUsersRepository) -> None:
        self.user_id = user_id
        self.accounts_admitted_users_repository = accounts_admitted_users_repository

    async def __call__(self, account_id: int, user_id: int) -> Optional[AccountsAdmittedUsersModel]:
        async with self.accounts_admitted_users_repository.transaction():
            return await self.accounts_admitted_users_repository.get_by_account_id_and_user_id(account_id=account_id,
                                                                                               user_id=user_id)
