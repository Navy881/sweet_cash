import logging
from typing import Dict, List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_users_by_ids import GetUsersByIds

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.types.accounts_types import AccountModel, AccountsAdmittedUsersModel
from sweet_cash.types.users_types import UserModel


logger = logging.getLogger(name="accounts")


class EnrichAccounts(BaseService):
    def __init__(self,
                 user_id: int,
                 get_users_by_ids: GetUsersByIds,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.get_users_by_ids = get_users_by_ids
        self.accounts_repository = accounts_repository

    async def __call__(self, accounts: List[AccountModel]):
        account_ids = [account.id for account in accounts]
        async with self.accounts_repository.transaction():
            admitted_users: List[AccountsAdmittedUsersModel] = await self.accounts_repository. \
                get_admitted_users_by_account_ids(account_ids)

        users_ids = [account.user_id for account in accounts]
        for admitted_user in admitted_users: users_ids.append(admitted_user.user_id)

        users: Dict[int, UserModel] = await self.get_users_by_ids(
            list(set(users_ids))
        )

        for account in accounts:
            try:
                account.user = users[account.user_id]
            except KeyError:
                account.user = None

            account.admitted_users = []
            for admitted_user in admitted_users:
                if admitted_user.account_id == account.id:
                    try:
                        account.admitted_users.append(users[admitted_user.user_id])
                    except KeyError as e:
                        logger.error(e)

