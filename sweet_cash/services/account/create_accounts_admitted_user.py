import logging

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import AccountModel, AccountsAdmittedUsersModel

from sweet_cash.errors import APIValueNotFound, APIConflict


logger = logging.getLogger(name="accounts")


class CreateAccountsAdmittedUser(BaseService):
    def __init__(self,
                 user_id: int,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.accounts_repository = accounts_repository

    async def __call__(self, account_id: int, user_id: int) -> AccountsAdmittedUsersModel:
        async with self.accounts_repository.transaction():
            account_model = await self.accounts_repository \
                .get_user_account_by_id(user_id=self.user_id, account_id=account_id)
            if not isinstance(account_model, AccountModel):
                raise APIValueNotFound(f'Account {account_id} not found')

            result = await self.accounts_repository.create_admitted_user(user_id=user_id, account_id=account_id)
            if isinstance(result, APIConflict):
                raise APIConflict(f'User {user_id} already added to account {account_id}')

            return result
 