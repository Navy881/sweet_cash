import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.transaction_categories.create_category_tree import create_category_tree

from sweet_cash.repositories.transaction_categories_repository import TransactionCategoriesRepository
from sweet_cash.repositories.transaction_categories_cache_repository import TransactionCategoriesCacheRepository

from sweet_cash.types.transaction_categories_types import TransactionCategoryModel

from sweet_cash.settings import Settings

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="transaction_categories")


class DeleteTransactionCategory(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_cache_repository: TransactionCategoriesCacheRepository,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id
        self.transaction_categories_cache_repository = transaction_categories_cache_repository
        self.transaction_categories_repository = transaction_categories_repository

    async def __call__(self, transaction_category_id: int) -> TransactionCategoryModel:
        async with self.transaction_categories_repository.transaction():
            transaction_category = await self.transaction_categories_repository. \
                get_transaction_category_by_id(transaction_category_id)

            if transaction_category is None:
                raise APIValueNotFound(f'Transaction category {transaction_category_id} not found')
            
            transaction_category: TransactionCategoryModel = await self.transaction_categories_repository.\
                delete_transaction_category(transaction_category.id)

            # Запись в кэш по типу категории
            transaction_categories: List[TransactionCategoryModel] = await self.transaction_categories_repository. \
                get_transaction_categories_by_type(transaction_category.type)

            category_tree = create_category_tree(transaction_categories)

            await self.transaction_categories_cache_repository.set(transaction_categories=category_tree,
                                                                   ttl_in_seconds=Settings.TRANSACTIONS_CATEGORIES_CACHE_TTL_SECOND,
                                                                   type=transaction_category.type)
            
            # Запись в кэш по всем категорииям
            transaction_categories: List[TransactionCategoryModel] = await self.transaction_categories_repository. \
                get_transaction_categories()

            category_tree = create_category_tree(transaction_categories)

            await self.transaction_categories_cache_repository.set(transaction_categories=category_tree,
                                                                   ttl_in_seconds=Settings.TRANSACTIONS_CATEGORIES_CACHE_TTL_SECOND,
                                                                   type=None)

            return transaction_category
