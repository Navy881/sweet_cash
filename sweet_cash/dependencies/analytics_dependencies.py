from fastapi import Request

from sweet_cash.services.analytics.get_account_balance import GetAccountBalance
from sweet_cash.services.analytics.get_categories_report import GetCategoriesReport

from sweet_cash.dependencies.accounts_dependencies import get_available_accounts_by_ids_internal_dependency
from sweet_cash.dependencies.events_dependencies import get_event_participants_roles_for_user_dependency
from sweet_cash.dependencies.transactions_dependencies import (
    get_transactions_by_account_id_dependency,
    get_transactions_by_event_and_type_dependency
)
from sweet_cash.dependencies.transaction_categories_dependencies import get_transaction_categories_by_ids_dependency


async def get_account_balance_dependency(request: Request) -> GetAccountBalance:
    return GetAccountBalance(
        user_id = getattr(request, "user_id"),
        get_available_accounts_by_ids = await get_available_accounts_by_ids_internal_dependency(request),
        get_transactions_by_account_id = await get_transactions_by_account_id_dependency(request)
    )


async def get_categories_report_dependency(request: Request) -> GetCategoriesReport:
    return GetCategoriesReport(
        user_id = getattr(request, "user_id"),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        get_transactions_by_event_and_type = await get_transactions_by_event_and_type_dependency(request),
        get_transaction_categories_by_ids = await get_transaction_categories_by_ids_dependency(request)
    )
