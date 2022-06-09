
import logging
import datetime
from typing import List

from api.services.base_service import BaseService
from api.repositories.transaction_categories_repository import TransactionCategoriesRepository
from api.types.transaction_categories_types import TransactionCategoryModel
from settings import Settings
from cache_management import RedisCache
from api.services.transaction_categories.create_category_tree import create_category_tree


logger = logging.getLogger(name="transactions")


class GetTransactionCategories(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id,
        self.transaction_categories_repository = transaction_categories_repository

    async def __call__(self) -> List[TransactionCategoryModel]:
        result = RedisCache.get(key='transaction:categories')

        if result is None:
            async with self.transaction_categories_repository.transaction():
                transaction_categories: List[TransactionCategoryModel] = await self.transaction_categories_repository.\
                    get_transaction_categories()

                result = create_category_tree(transaction_categories)

            RedisCache.setex(key='transaction:categories',
                             time=datetime.timedelta(seconds=Settings.TRANSACTIONS_CATEGORIES_CACHE_TTL_SECOND),
                             obj=result)

        return result
