import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById

from sweet_cash.repositories.accounts_admitted_users_repository import AccountsAdmittedUsersRepository

from sweet_cash.types.accounts_admitted_users_types import AccountsAdmittedUsersModel
from sweet_cash.types.users_types import UserModel


logger = logging.getLogger(name="accounts")


class GetAccountsAdmittedUsersByAccount(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 accounts_admitted_users_repository: AccountsAdmittedUsersRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.accounts_admitted_users_repository = accounts_admitted_users_repository

    async def __call__(self, account_id: int) -> List[UserModel]:
        result: List = []

        async with self.accounts_admitted_users_repository.transaction():
            admitted_users: List[AccountsAdmittedUsersModel] = await self.accounts_admitted_users_repository. \
                get_by_account_id(account_id)

        for admitted_user in admitted_users:
            user = await self.get_user_by_id(admitted_user.user_id)
            if user is not None:
                result.append(user)

        return result
