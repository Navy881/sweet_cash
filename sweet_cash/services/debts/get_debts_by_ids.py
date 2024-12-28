import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.debts.enrich_debts import EnrichDebts

from sweet_cash.repositories.debts_repository import DebtsRepository

from sweet_cash.types.debts_types import DebtModel

from sweet_cash.utils import ids2list


logger = logging.getLogger(name="accounts")


class GetDebtsByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_debts: EnrichDebts,
                 debts_repository: DebtsRepository) -> None:
        self.user_id = user_id
        self.enrich_debts = enrich_debts
        self.debts_repository = debts_repository

    async def __call__(self, debt_ids) -> List[DebtModel]:
        if isinstance(debt_ids, str):
            debt_ids: List[id] = ids2list(debt_ids)

        async with self.debts_repository.transaction():
            debts: List[DebtModel] = await self.debts_repository \
                .get_user_debts_by_ids(debt_ids=debt_ids, user_id=self.user_id)
            await self.enrich_debts(debts)
            return debts
