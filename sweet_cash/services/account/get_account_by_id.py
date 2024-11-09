import logging
from typing import Union

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import AccountModel


logger = logging.getLogger(name="accounts")


class GetAccountById(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.accounts_repository = accounts_repository

    async def __call__(self, account_id: int) -> Union[AccountModel, None]:
        async with self.accounts_repository.transaction():
            account = await self.accounts_repository.get_by_id(account_id)

        if account:
            account.user = await self.get_user_by_id(account.user_id)

        return account
