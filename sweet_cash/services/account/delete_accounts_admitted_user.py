import logging

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import AccountsAdmittedUsersModel

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="accounts")


class DeleteAccountsAdmittedUser(BaseService):
    def __init__(self,
                 user_id: int,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.accounts_repository = accounts_repository

    async def __call__(self, account_id: int, user_id: int) -> AccountsAdmittedUsersModel:
        async with self.accounts_repository.transaction():
            result = await self.accounts_repository.delete_admitted_user(user_id=user_id, account_id=account_id)
            if isinstance(result, APIValueNotFound):
                raise APIValueNotFound(f'User {user_id} not added to account {account_id}')

            return result
