import logging
from typing import Dict, List

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.transaction_categories_repository import TransactionCategoriesRepository

from sweet_cash.types.transaction_categories_types import TransactionCategoryModel


logger = logging.getLogger(name="transaction_categories")


class GetTransactionCategoriesByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id
        self.transaction_categories_repository = transaction_categories_repository

    async def __call__(self, categories_ids: List[int]) -> Dict[int, TransactionCategoryModel]:
        async with self.transaction_categories_repository.transaction():
            categories: List[TransactionCategoryModel] = await self.transaction_categories_repository.\
                get_transaction_categories_by_ids(categories_ids)
            return {category.id: category for category in categories}

