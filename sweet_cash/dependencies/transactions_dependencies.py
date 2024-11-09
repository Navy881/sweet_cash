from fastapi import Request

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.services.transactions.create_transaction import CreateTransaction, CreateTransactionV2
from sweet_cash.services.transactions.get_all_transactions import GetAllTransactions
from sweet_cash.services.transactions.get_transactions_by_ids import GetTransactionsByIds
from sweet_cash.services.transactions.update_transaction import UpdateTransaction, UpdateTransactionV2
from sweet_cash.services.transactions.delete_transaction import DeleteTransaction

from sweet_cash.dependencies.users_dependecies import get_user_by_id_dependency
from sweet_cash.dependencies.accounts_dependencies import (
    get_account_by_id_dependency,
    get_available_accounts_by_id_dependency
)
from sweet_cash.dependencies.transaction_categories_dependencies import get_transaction_category_by_id_dependency
from sweet_cash.dependencies.events_dependencies import get_event_participants_roles_for_user_dependency


async def transactions_repository_dependency(request: Request) -> TransactionsRepository:
    engine = request.app.state.db
    return TransactionsRepository(engine)


async def create_transaction_dependency(request: Request) -> CreateTransaction:
    return CreateTransaction(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_account_by_id = await get_account_by_id_dependency(request),
        get_available_account_by_id = await get_available_accounts_by_id_dependency(request),
        get_transaction_category_by_id = await get_transaction_category_by_id_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def get_all_transactions_dependency(request: Request) -> GetAllTransactions:
    return GetAllTransactions(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_available_account_by_id = await get_available_accounts_by_id_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def get_transactions_dependency(request: Request) -> GetTransactionsByIds:
    return GetTransactionsByIds(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_available_account_by_id = await get_available_accounts_by_id_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def update_transaction_dependency(request: Request) -> UpdateTransaction:
    return UpdateTransaction(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_available_account_by_id = await get_available_accounts_by_id_dependency(request),
        get_transaction_category_by_id = await get_transaction_category_by_id_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def delete_transaction_dependency(request: Request) -> DeleteTransaction:
    return DeleteTransaction(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_available_account_by_id = await get_available_accounts_by_id_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def create_transaction_dependency_v2(request: Request) -> CreateTransactionV2:
    return CreateTransactionV2(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_account_by_id = await get_account_by_id_dependency(request),
        get_available_account_by_id = await get_available_accounts_by_id_dependency(request),
        get_transaction_category_by_id = await get_transaction_category_by_id_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def update_transaction_dependency_v2(request: Request) -> UpdateTransactionV2:
    return UpdateTransactionV2(
        user_id=getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_account_by_id = await get_account_by_id_dependency(request),
        get_available_account_by_id = await get_available_accounts_by_id_dependency(request),
        get_transaction_category_by_id = await get_transaction_category_by_id_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )
