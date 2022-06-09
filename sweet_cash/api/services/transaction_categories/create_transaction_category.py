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


class CreateTransactionCategory(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id,
        self.transaction_categories_repository = transaction_categories_repository

    async def __call__(self, category: CreateTransactionCategoryModel) -> TransactionCategoryModel:
        async with self.transaction_categories_repository.transaction():
            transaction_category: TransactionCategoryModel = await self.transaction_categories_repository.\
                create_transaction_category(category)

            transaction_categories: List[TransactionCategoryModel] = await self.transaction_categories_repository. \
                get_transaction_categories()

            category_tree = create_category_tree(transaction_categories)

            RedisCache.setex(key='transaction:categories',
                             time=datetime.timedelta(seconds=Settings.TRANSACTIONS_CATEGORIES_CACHE_TTL_SECOND),
                             obj=category_tree)

            return transaction_category
