import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById

from sweet_cash.repositories.debts_repository import DebtsRepository

from sweet_cash.types.debts_types import DebtModel


logger = logging.getLogger(name="accounts")


class GetDebtsByUser(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 debts_repository: DebtsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.debts_repository = debts_repository

    async def __call__(self) -> List[DebtModel]:
        async with self.debts_repository.transaction():
            users_debts: List[DebtModel] = await self.debts_repository.get_by_user_id(self.user_id)
            
        for i, debt in enumerate(users_debts):
            users_debts[i].user = await self.get_user_by_id(debt.user_id)

        return users_debts

