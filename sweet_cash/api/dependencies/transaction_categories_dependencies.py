
from fastapi import Request

from api.repositories.transaction_categories_repository import TransactionCategoriesRepository
from api.services.transaction_categories.create_transaction_category import CreateTransactionCategory
from api.services.transaction_categories.get_transaction_categories import GetTransactionCategories
from api.services.transaction_categories.update_transaction_category import UpdateTransactionCategory
from api.services.transaction_categories.delete_transaction_category import DeleteTransactionCategory
from db import engine


def transaction_categories_repository_dependency(request: Request) -> TransactionCategoriesRepository:
    pg_engine = request
    return TransactionCategoriesRepository()


def create_transaction_categories_dependency(request: Request) -> CreateTransactionCategory:
    return CreateTransactionCategory(
        user_id=getattr(request, "user_id"),
        transaction_categories_repository=transaction_categories_repository_dependency(request)
    )


def get_transaction_categories_dependency(request: Request) -> GetTransactionCategories:
    return GetTransactionCategories(
        user_id=getattr(request, "user_id"),
        transaction_categories_repository=transaction_categories_repository_dependency(request)
    )


def update_transaction_categories_dependency(request: Request) -> UpdateTransactionCategory:
    return UpdateTransactionCategory(
        user_id=getattr(request, "user_id"),
        transaction_categories_repository=transaction_categories_repository_dependency(request)
    )


def delete_transaction_categories_dependency(request: Request) -> DeleteTransactionCategory:
    return DeleteTransactionCategory(
        user_id=getattr(request, "user_id"),
        transaction_categories_repository=transaction_categories_repository_dependency(request)
    )
