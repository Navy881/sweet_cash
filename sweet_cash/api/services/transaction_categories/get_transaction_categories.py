
import logging
from typing import List

from api.services.base_service import BaseService
from api.repositories.transaction_categories_repository import TransactionCategoriesRepository
from api.types.transaction_categories_types import TransactionCategoryModel

logger = logging.getLogger(name="transactions")


class GetTransactionCategories(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id,
        self.transaction_categories_repository = transaction_categories_repository

    async def __call__(self) -> List[TransactionCategoryModel]:
        async with self.transaction_categories_repository.transaction():
            transaction_categories: List[TransactionCategoryModel] = await self.transaction_categories_repository.\
                get_transaction_categories()

            result: List[TransactionCategoryModel] = []

            while transaction_categories:

                sub_category = transaction_categories.pop(0)

                if sub_category.parent_category_id is None:
                    result.append(sub_category)
                    break

                for parent_candidate in transaction_categories:
                    if sub_category.parent_category_id == parent_candidate.id:
                        parent_candidate.sub_categories.append(sub_category)
                        break

                result.append(sub_category)

            return result


# import logging
# import datetime
#
# from api.models.transaction_category import TransactionCategoryModel
# from cache_management import RedisCache
#
#
# logger = logging.getLogger(name="categories")
#
#
# class GetCategories(object):
#
#     def __call__(self, user_id) -> [TransactionCategoryModel]:
#         result = RedisCache.get(key='transaction:categories')
#
#         if result is None:
#             categories = TransactionCategoryModel.get()
#
#             result = []
#             while categories:
#                 sub_category = categories.pop(0)
#                 for parent_candidate in categories:
#                     if sub_category.parent_category_id == parent_candidate.id:
#                         if not hasattr(parent_candidate, 'sub_categories'):
#                             setattr(parent_candidate, 'sub_categories', [])
#                         parent_candidate.sub_categories.append(sub_category)
#                         break
#
#                     result.append(sub_category)
#
#                 if not categories:
#                     result.append(sub_category)
#
#             result = list(reversed(result))
#
#             RedisCache.setex(key='transaction:categories',
#                              time=datetime.timedelta(seconds=10),
#                              obj=result)
#
#         logger.info(f'User {user_id} got categories')
#
#         return result
