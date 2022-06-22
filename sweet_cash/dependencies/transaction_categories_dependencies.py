
from fastapi import Request

from sweet_cash.repositories.transaction_categories_repository import TransactionCategoriesRepository
from sweet_cash.repositories.transaction_categories_cache_repository import TransactionCategoriesCacheRepository
from sweet_cash.services.transaction_categories.create_transaction_category import CreateTransactionCategory
from sweet_cash.services.transaction_categories.get_transaction_categories import GetTransactionCategories
from sweet_cash.services.transaction_categories.update_transaction_category import UpdateTransactionCategory
from sweet_cash.services.transaction_categories.delete_transaction_category import DeleteTransactionCategory


def transaction_categories_repository_dependency(request: Request) -> TransactionCategoriesRepository:
    engine = request.app.state.db
    return TransactionCategoriesRepository(engine)


def transaction_categories_cache_repository_dependency(request: Request) -> TransactionCategoriesCacheRepository:
    redis = request.app.state.redis
    return TransactionCategoriesCacheRepository(redis)


def create_transaction_categories_dependency(request: Request) -> CreateTransactionCategory:
    return CreateTransactionCategory(
        user_id=getattr(request, "user_id"),
        transaction_categories_cache_repository=transaction_categories_cache_repository_dependency(request),
        transaction_categories_repository=transaction_categories_repository_dependency(request)
    )


def get_transaction_categories_dependency(request: Request) -> GetTransactionCategories:
    return GetTransactionCategories(
        user_id=getattr(request, "user_id"),
        transaction_categories_cache_repository=transaction_categories_cache_repository_dependency(request),
        transaction_categories_repository=transaction_categories_repository_dependency(request)
    )


def update_transaction_categories_dependency(request: Request) -> UpdateTransactionCategory:
    return UpdateTransactionCategory(
        user_id=getattr(request, "user_id"),
        transaction_categories_cache_repository=transaction_categories_cache_repository_dependency(request),
        transaction_categories_repository=transaction_categories_repository_dependency(request)
    )


def delete_transaction_categories_dependency(request: Request) -> DeleteTransactionCategory:
    return DeleteTransactionCategory(
        user_id=getattr(request, "user_id"),
        transaction_categories_cache_repository=transaction_categories_cache_repository_dependency(request),
        transaction_categories_repository=transaction_categories_repository_dependency(request)
    )
