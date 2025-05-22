import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_users_by_ids import GetUsersByIds
from sweet_cash.services.transaction_categories.get_transaction_categories_by_ids import GetTransactionCategoriesByIds

from sweet_cash.types.limits_types import LimitModel
from sweet_cash.types.users_types import UserModel
from sweet_cash.types.transaction_categories_types import TransactionCategoryModel


logger = logging.getLogger(name="limits")


class EnrichLimits(BaseService):
    def __init__(self,
                 user_id: int,
                 get_users_by_ids: GetUsersByIds,
                 get_transaction_categories_by_ids: GetTransactionCategoriesByIds) -> None:
        self.user_id = user_id
        self.get_users_by_ids = get_users_by_ids
        self.get_transaction_categories_by_ids = get_transaction_categories_by_ids

    async def __call__(self, limits: List[LimitModel]):
        user_ids = {limit.created_by_user_id for limit in limits}
        users: Dict[int, UserModel] = await self.get_users_by_ids(list(user_ids))

        categories_ids = {limit.category_id for limit in limits}
        categories: Dict[int, TransactionCategoryModel] = await \
            self.get_transaction_categories_by_ids(list(categories_ids))

        for limit in limits:
            limit.created_by = users[limit.created_by_user_id]

            if limit.category_id:
                limit.category = categories[limit.category_id]
