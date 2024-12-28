import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.debts.enrich_debts import EnrichDebts

from sweet_cash.repositories.debts_repository import DebtsRepository

from sweet_cash.types.debts_types import DebtModel


logger = logging.getLogger(name="accounts")


class GetDebtsByUser(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_debts: EnrichDebts,
                 debts_repository: DebtsRepository) -> None:
        self.user_id = user_id
        self.enrich_debts = enrich_debts
        self.debts_repository = debts_repository

    async def __call__(self) -> List[DebtModel]:
        async with self.debts_repository.transaction():
            users_debts: List[DebtModel] = await self.debts_repository.get_debts_by_user_id(self.user_id)
            await self.enrich_debts(users_debts)
            return users_debts

