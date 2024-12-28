import logging
from typing import Dict, List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_users_by_ids import GetUsersByIds

from sweet_cash.types.debts_types import DebtModel
from sweet_cash.types.users_types import UserModel


logger = logging.getLogger(name="accounts")


class EnrichDebts(BaseService):
    def __init__(self,
                 user_id: int,
                 get_users_by_ids: GetUsersByIds) -> None:
        self.user_id = user_id
        self.get_users_by_ids = get_users_by_ids

    async def __call__(self, debts: List[DebtModel]):
        users: Dict[int, UserModel] = await self.get_users_by_ids(
            list(set([debt.user_id for debt in debts]))
        )

        for debt in debts:
            try:
                debt.user = users[debt.user_id]
            except KeyError:
                debt.user = None
