import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import CreateAccountModel, AccountModel


logger = logging.getLogger(name="accounts")


class CreateAccount(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.accounts_repository = accounts_repository

    async def __call__(self, account: CreateAccountModel) -> AccountModel:
        async with self.accounts_repository.transaction():
            account_model: AccountModel = await self.accounts_repository.create_account(user_id=self.user_id,
                                                                                        item=account)
        
        account_model.user = await self.get_user_by_id(account_model.user_id)
        return account_model