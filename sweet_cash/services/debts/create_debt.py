import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.debts.enrich_debts import EnrichDebts

from sweet_cash.repositories.debts_repository import DebtsRepository

from sweet_cash.types.debts_types import CreateDebtModel, DebtModel


logger = logging.getLogger(name="debts")


class CreateDebt(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_debts: EnrichDebts,
                 debts_repository: DebtsRepository) -> None:
        self.user_id = user_id
        self.enrich_debts = enrich_debts
        self.debts_repository = debts_repository

    async def __call__(self, debt: CreateDebtModel) -> DebtModel:
        async with self.debts_repository.transaction():
            debt_model: DebtModel = await self.debts_repository.create_debt(user_id=self.user_id, item=debt)
            await self.enrich_debts([debt_model])
            return debt_model
