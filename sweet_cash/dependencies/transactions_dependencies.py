from fastapi import Request

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.services.transactions.create_transaction import CreateTransaction
from sweet_cash.services.transactions.get_all_transactions import GetAllTransactions
from sweet_cash.services.transactions.get_transactions_by_ids import GetTransactionsByIds
from sweet_cash.services.transactions.update_transaction import UpdateTransaction
from sweet_cash.services.transactions.delete_transaction import DeleteTransaction
from sweet_cash.services.transactions.enrich_transactions import EnrichTransactions
from sweet_cash.services.transactions.get_transactions_by_account_id import GetTransactionsByAccountId
from sweet_cash.services.transactions.get_transactions_by_event_and_type import GetTransactionsByEventAndType

from sweet_cash.dependencies.users_dependecies import get_users_by_ids_dependency
from sweet_cash.dependencies.accounts_dependencies import (
    get_account_by_ids_dependency,
    get_available_accounts_by_ids_internal_dependency
)
from sweet_cash.dependencies.transaction_categories_dependencies import get_transaction_category_by_id_dependency
from sweet_cash.dependencies.events_dependencies import get_event_participants_roles_for_user_dependency


async def transactions_repository_dependency(request: Request) -> TransactionsRepository:
    engine = request.app.state.db
    return TransactionsRepository(engine)

async def enrich_transactions_dependency(request: Request) -> EnrichTransactions:
    return EnrichTransactions(
        user_id=getattr(request, "user_id"),
        get_users_by_ids = await get_users_by_ids_dependency(request),
        get_available_accounts_by_ids = await get_available_accounts_by_ids_internal_dependency(request)
    )


async def get_all_transactions_dependency(request: Request) -> GetAllTransactions:
    return GetAllTransactions(
        user_id=getattr(request, "user_id"),
        enrich_transactions = await enrich_transactions_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def get_transactions_dependency(request: Request) -> GetTransactionsByIds:
    return GetTransactionsByIds(
        user_id=getattr(request, "user_id"),
        enrich_transactions=await enrich_transactions_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def delete_transaction_dependency(request: Request) -> DeleteTransaction:
    return DeleteTransaction(
        user_id=getattr(request, "user_id"),
        enrich_transactions=await enrich_transactions_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def create_transaction_dependency(request: Request) -> CreateTransaction:
    return CreateTransaction(
        user_id=getattr(request, "user_id"),
        enrich_transactions = await enrich_transactions_dependency(request),
        get_accounts_by_ids = await get_account_by_ids_dependency(request),
        get_transaction_category_by_id = await get_transaction_category_by_id_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def update_transaction_dependency(request: Request) -> UpdateTransaction:
    return UpdateTransaction(
        user_id=getattr(request, "user_id"),
        enrich_transactions = await enrich_transactions_dependency(request),
        get_accounts_by_ids = await get_account_by_ids_dependency(request),
        get_transaction_category_by_id = await get_transaction_category_by_id_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )

async def get_transactions_by_account_id_dependency(request: Request) -> GetTransactionsByAccountId:
    return GetTransactionsByAccountId(
        user_id=getattr(request, "user_id"),
        enrich_transactions = await enrich_transactions_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )

async def get_transactions_by_event_and_type_dependency(request: Request) -> GetTransactionsByEventAndType:
    return GetTransactionsByEventAndType(
        user_id=getattr(request, "user_id"),
        transactions_repository = await transactions_repository_dependency(request)
    )
