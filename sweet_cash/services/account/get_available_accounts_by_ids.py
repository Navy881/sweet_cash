import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById
from sweet_cash.services.account.get_accounts_admitted_users_by_account import GetAccountsAdmittedUsersByAccount
from sweet_cash.services.account.get_accounts_admitted_user_by_account_id_and_user_id import GetAccountsAdmittedUserByAccountIdAndUserId

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import AccountModel

from sweet_cash.utils import ids2list


logger = logging.getLogger(name="accounts")


class GetAvailableAccountsByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 get_admitted_users_by_account: GetAccountsAdmittedUsersByAccount,
                 get_admitted_user_by_account_id_and_user_id: GetAccountsAdmittedUserByAccountIdAndUserId,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.get_admitted_users_by_account = get_admitted_users_by_account
        self.get_admitted_user_by_account_id_and_user_id = get_admitted_user_by_account_id_and_user_id
        self.accounts_repository = accounts_repository

    async def __call__(self, account_ids, with_blocked: bool = False) -> List[AccountModel]:
        if isinstance(account_ids, str):
            account_ids: List[id] = ids2list(account_ids)

        result: List = []
        async with self.accounts_repository.transaction():
            accounts: List[AccountModel] = await self.accounts_repository.get_by_ids(account_ids=account_ids,
                                                                                     with_blocked=with_blocked)

        # Проверка, что user связан с account
        for account in accounts:
            if account.user_id == self.user_id:
                result.append(account)
                continue

            if await self.get_admitted_user_by_account_id_and_user_id(account_id=account.id, user_id=self.user_id):
                result.append(account)
                continue

        # Обогащение модели account
        for i, account in enumerate(result):
            result[i].user = await self.get_user_by_id(account.user_id)
            result[i].admitted_users = await self.get_admitted_users_by_account(account.id)

        return result
