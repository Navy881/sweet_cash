
import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.accounts_repository import AccountsRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.types.accounts_types import AccountModel
from sweet_cash.types.users_types import UserResponseModel
from sweet_cash.utils import ids2list


logger = logging.getLogger(name="accounts")


class GetAccounts(BaseService):
    def __init__(self,
                 user_id: int,
                 accounts_repository: AccountsRepository,
                 user_repository: UsersRepository) -> None:
        self.user_id = user_id
        self.accounts_repository = accounts_repository
        self.user_repository = user_repository

    async def __call__(self, account_ids: str) -> List[AccountModel]:
        account_ids: List[id] = ids2list(account_ids)

        async with self.accounts_repository.transaction():
            accounts: List[AccountModel] = await self.accounts_repository.get_user_accounts_by_ids(account_ids=account_ids, 
                                                                                                  user_id=self.user_id)

        async with self.user_repository.transaction():
            for i, account in enumerate(accounts):
                user = await self.user_repository.get_by_id(account.user_id)
                accounts[i].user = UserResponseModel(**user.dict())

            return accounts
