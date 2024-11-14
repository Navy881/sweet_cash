import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById

from sweet_cash.repositories.debts_repository import DebtsRepository

from sweet_cash.types.debts_types import CreateDebtModel, DebtModel


logger = logging.getLogger(name="debts")


class CreateDebt(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 debts_repository: DebtsRepository) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.debts_repository = debts_repository

    async def __call__(self, debt: CreateDebtModel) -> DebtModel:
        async with self.debts_repository.transaction():
            debt_model: DebtModel = await self.debts_repository.create_debt(user_id=self.user_id, item=debt)
        
        debt_model.user = await self.get_user_by_id(debt_model.user_id)
        return debt_model
