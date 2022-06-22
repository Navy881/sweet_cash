
import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.transaction_categories_repository import TransactionCategoriesRepository
from sweet_cash.repositories.transaction_categories_cache_repository import TransactionCategoriesCacheRepository
from sweet_cash.types.transaction_categories_types import TransactionCategoryModel
from sweet_cash.settings import Settings
from sweet_cash.services.transaction_categories.create_category_tree import create_category_tree


logger = logging.getLogger(name="transaction_categories")


class GetTransactionCategories(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_cache_repository: TransactionCategoriesCacheRepository,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id
        self.transaction_categories_cache_repository = transaction_categories_cache_repository
        self.transaction_categories_repository = transaction_categories_repository

    async def __call__(self) -> List[TransactionCategoryModel]:
        result: List[TransactionCategoryModel] = await self.transaction_categories_cache_repository.get()

        if result is None:
            async with self.transaction_categories_repository.transaction():
                transaction_categories: List[TransactionCategoryModel] = await self.transaction_categories_repository.\
                    get_transaction_categories()

                result = create_category_tree(transaction_categories)

            await self.transaction_categories_cache_repository.set(transaction_categories=result,
                                                                   ttl_in_seconds=Settings.TRANSACTIONS_CATEGORIES_CACHE_TTL_SECOND)

        return result
