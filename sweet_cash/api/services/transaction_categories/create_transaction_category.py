import logging

from api.services.base_service import BaseService
from api.repositories.transaction_categories_repository import TransactionCategoriesRepository
from api.types.transaction_categories_types import TransactionCategoryModel, CreateTransactionCategoryModel

logger = logging.getLogger(name="transactions")


class CreateTransactionCategory(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id,
        self.transaction_categories_repository = transaction_categories_repository

    async def __call__(self, category: CreateTransactionCategoryModel) -> TransactionCategoryModel:
        async with self.transaction_categories_repository.transaction():
            return await self.transaction_categories_repository.create_transaction_category(category)
