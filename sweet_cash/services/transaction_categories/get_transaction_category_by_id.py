import logging

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.transaction_categories_repository import TransactionCategoriesRepository

from sweet_cash.types.transaction_categories_types import TransactionCategoryModel

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="transaction_categories")


class GetTransactionCategoryBiId(BaseService):
    def __init__(self,
                 user_id: int,
                 transaction_categories_repository: TransactionCategoriesRepository) -> None:
        self.user_id = user_id
        self.transaction_categories_repository = transaction_categories_repository

    async def __call__(self, transaction_category_id) -> TransactionCategoryModel:
        async with self.transaction_categories_repository.transaction():
            transaction_category = await self.transaction_categories_repository. \
                get_transaction_category_by_id(transaction_category_id)

            if transaction_category is None:
                raise APIValueNotFound(f'Transaction category {transaction_category_id} not found')

        return transaction_category
