from fastapi import Request

from sweet_cash.services.analytics.get_account_balance import GetAccountBalance

from sweet_cash.dependencies.accounts_dependencies import get_available_accounts_by_ids_internal_dependency
from sweet_cash.dependencies.transactions_dependencies import get_transactions_by_account_id_dependency


async def get_account_balance_dependency(request: Request) -> GetAccountBalance:
    return GetAccountBalance(
        user_id = getattr(request, "user_id"),
        get_available_accounts_by_ids = await get_available_accounts_by_ids_internal_dependency(request),
        get_transactions_by_account_id = await get_transactions_by_account_id_dependency(request)
    )
