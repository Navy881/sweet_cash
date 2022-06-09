import logging
import datetime
from typing import List

from api.services.base_service import BaseService
from api.repositories.transaction_categories_repository import TransactionCategoriesRepository
from api.types.transaction_categories_types import TransactionCategoryModel, CreateTransactionCategoryModel
from settings import Settings
from cache_management import RedisCache
from api.services.transaction_categories.create_category_tree import create_category_tree


logger = logging.getLogger(name="transactions")


class UpdateTransactionCategory(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id,
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

            RedisCache.setex(key='transaction:categories',
                             time=datetime.timedelta(seconds=Settings.TRANSACTIONS_CATEGORIES_CACHE_TTL_SECOND),
                             obj=category_tree)

            return transaction_category
