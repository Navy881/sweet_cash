import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.transaction_categories_repository import TransactionCategoriesRepository
from sweet_cash.repositories.transaction_categories_cache_repository import TransactionCategoriesCacheRepository
from sweet_cash.types.transaction_categories_types import TransactionCategoryModel, CreateTransactionCategoryModel
from sweet_cash.settings import Settings
from sweet_cash.services.transaction_categories.create_category_tree import create_category_tree


logger = logging.getLogger(name="transaction_categories")


class UpdateTransactionCategory(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_cache_repository: TransactionCategoriesCacheRepository,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id
        self.transaction_categories_cache_repository = transaction_categories_cache_repository
        self.transaction_categories_repository = transaction_categories_repository

    async def __call__(self, transaction_category_id: int,
                       transaction_category: CreateTransactionCategoryModel) -> TransactionCategoryModel:
        async with self.transaction_categories_repository.transaction():
            await self.transaction_categories_repository.get_transaction_category_by_id(transaction_category_id)
            transaction_category: TransactionCategoryModel = await self.transaction_categories_repository. \
                update_transaction_category(transaction_category_id=transaction_category_id,
                                            transaction_category=transaction_category)

            transaction_categories: List[TransactionCategoryModel] = await self.transaction_categories_repository. \
                get_transaction_categories()

            category_tree = create_category_tree(transaction_categories)

            await self.transaction_categories_cache_repository.set(transaction_categories=category_tree,
                                                                   ttl_in_seconds=Settings.TRANSACTIONS_CATEGORIES_CACHE_TTL_SECOND)

            return transaction_category
