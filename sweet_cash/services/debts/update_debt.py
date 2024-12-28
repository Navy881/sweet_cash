import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.debts.enrich_debts import EnrichDebts

from sweet_cash.repositories.debts_repository import DebtsRepository

from sweet_cash.types.debts_types import CreateDebtModel, DebtModel

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="debts")


class UpdateDebt(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_debts: EnrichDebts,
                 debts_repository: DebtsRepository) -> None:
        self.user_id = user_id
        self.enrich_debts = enrich_debts
        self.debts_repository = debts_repository

    async def __call__(self, debt_id: int, debt: CreateDebtModel) -> DebtModel:
        async with self.debts_repository.transaction():
            debt_model = await self.debts_repository.update_debt(user_id=self.user_id, debt_id=debt_id, item=debt)
            if not isinstance(debt_model, DebtModel):
                raise APIValueNotFound(f'Debt {debt_id} not found')

            await self.enrich_debts([debt_model])
            return debt_model

