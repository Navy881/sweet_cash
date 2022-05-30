import logging

from api.services.base_service import BaseService
from api.repositories.transaction_categories_repository import TransactionCategoriesRepository
from api.types.transaction_categories_types import TransactionCategoryModel

logger = logging.getLogger(name="transactions")


class DeleteTransactionCategory(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id,
        self.transaction_categories_repository = transaction_categories_repository

    async def __call__(self, transaction_category_id: int) -> TransactionCategoryModel:
        async with self.transaction_categories_repository.transaction():
            return await self.transaction_categories_repository.delete_transaction_category(transaction_category_id)
