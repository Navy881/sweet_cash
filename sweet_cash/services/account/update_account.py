
import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.accounts_repository import AccountsRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.types.accounts_types import UpdateAccountModel, AccountModel
from sweet_cash.types.users_types import UserResponseModel
from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="accounts")


class UpdateAccount(BaseService):
    def __init__(self,
                 user_id: int,
                 accounts_repository: AccountsRepository,
                 user_repository: UsersRepository) -> None:
        self.user_id = user_id
        self.accounts_repository = accounts_repository
        self.user_repository = user_repository

    async def __call__(self, account_id: int, account: UpdateAccountModel) -> AccountModel:
        async with self.accounts_repository.transaction():
            account_model = await self.accounts_repository.get_user_account_by_id(account_id=account_id,
                                                                                  user_id=self.user_id)
            if account_model is None:
                raise APIValueNotFound(f'Account {account_id} not found')

            account_model: AccountModel = await self.accounts_repository.update_account(account_id=account_id,
                                                                                        item=account)

        async with self.user_repository.transaction():
            user = await self.user_repository.get_by_id(account_model.user_id)
            account_model.user = UserResponseModel(**user.dict())

        return account_model
