import logging
from typing import List, Optional

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.transaction_categories.get_transaction_categories import GetTransactionCategories

from sweet_cash.types.transaction_categories_types import TransactionCategoryModel


logger = logging.getLogger(name="transaction_categories")


class GetSubTransactionCategories(BaseService):
    def __init__(self,
                 user_id: int,
                 get_transaction_categories: GetTransactionCategories) -> None:
        self.user_id = user_id
        self.get_transaction_categories = get_transaction_categories

    async def __call__(self, category_id: int) -> List[TransactionCategoryModel]:
        def search_category_by_tree(
                category_id: int,
                category_tree: List[TransactionCategoryModel]
        ) -> Optional[TransactionCategoryModel]:
            for item in category_tree:
                if item.id == category_id:
                    return item
                if item.sub_categories:
                    c_ = search_category_by_tree(category_id, item.sub_categories)
                    if c_:
                        return c_
            return None

        def get_all_sub_categories(category: TransactionCategoryModel) -> List[TransactionCategoryModel]:
            result = []
            if category.sub_categories:
                result += category.sub_categories
                for sub_category in category.sub_categories:
                    result += get_all_sub_categories(sub_category)
            return result

        result = []
        category_tree = await self.get_transaction_categories()
        category_branch = search_category_by_tree(category_id, category_tree)
        if category_branch:
            result += get_all_sub_categories(category_branch)

        return result
