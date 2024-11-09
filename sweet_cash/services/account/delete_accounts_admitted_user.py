import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.account.get_account_by_id import GetAccountById

from sweet_cash.repositories.accounts_admitted_users_repository import AccountsAdmittedUsersRepository

from sweet_cash.types.accounts_admitted_users_types import AccountsAdmittedUsersModel

from sweet_cash.errors import APIValueNotFound, APIAuthError


logger = logging.getLogger(name="accounts")


class DeleteAccountsAdmittedUser(BaseService):
    def __init__(self,
                 user_id: int,
                 get_account_by_id: GetAccountById,
                 accounts_admitted_users_repository: AccountsAdmittedUsersRepository) -> None:
        self.user_id = user_id
        self.get_account_by_id = get_account_by_id
        self.accounts_admitted_users_repository = accounts_admitted_users_repository

    async def __call__(self, account_id: int, user_id: int) -> AccountsAdmittedUsersModel:
        # Проверка, что пользователь является владельцем account
        account = await self.get_account_by_id(account_id)
        if account is None:
            raise APIValueNotFound(f'Account {account_id} not found')
        
        if account.user_id != self.user_id:
            raise APIAuthError(f'No access to account {account_id}')
        
        async with self.accounts_admitted_users_repository.transaction():
            admitted_user = await self.accounts_admitted_users_repository. \
                get_by_account_id_and_user_id(account_id=account_id, user_id=user_id)
            if admitted_user is None:
                raise APIValueNotFound(f'User {user_id} not added to account {account_id}')

            return await self.accounts_admitted_users_repository.delete_admitted_user(admitted_user.id)
 