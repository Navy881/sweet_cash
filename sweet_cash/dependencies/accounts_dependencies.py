from fastapi import Request

from sweet_cash.repositories.accounts_repository import AccountsRepository

from sweet_cash.services.account.create_account import CreateAccount
from sweet_cash.services.account.update_account import UpdateAccount
from sweet_cash.services.account.get_accounts_by_ids import GetAccountsByIds
from sweet_cash.services.account.get_available_accounts_by_ids import (
    GetAvailableAccountsByIds,
    GetAvailableAccountsByIdsInternal
)
from sweet_cash.services.account.get_available_accounts_by_user import GetAvailableAccountsByUser
from sweet_cash.services.account.create_accounts_admitted_user import CreateAccountsAdmittedUser
from sweet_cash.services.account.delete_accounts_admitted_user import DeleteAccountsAdmittedUser
from sweet_cash.services.account.enrich_accounts import EnrichAccounts

from sweet_cash.dependencies.users_dependecies import get_users_by_ids_dependency


async def accounts_repository_dependency(request: Request) -> AccountsRepository:
    engine = request.app.state.db
    return AccountsRepository(engine)


async def enrich_accounts_dependency(request: Request) -> EnrichAccounts:
    return EnrichAccounts(
        user_id = getattr(request, "user_id"),
        get_users_by_ids = await get_users_by_ids_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def create_account_dependency(request: Request) -> CreateAccount:
    return CreateAccount(
        user_id = getattr(request, "user_id"),
        enrich_accounts = await enrich_accounts_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def get_account_by_ids_dependency(request: Request) -> GetAccountsByIds:
    return GetAccountsByIds(
        user_id = getattr(request, "user_id"),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def create_accounts_admitted_user_dependency(request: Request) -> CreateAccountsAdmittedUser:
    return CreateAccountsAdmittedUser(
        user_id = getattr(request, "user_id"),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def delete_accounts_admitted_user_dependency(request: Request) -> DeleteAccountsAdmittedUser:
    return DeleteAccountsAdmittedUser(
        user_id = getattr(request, "user_id"),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def update_account_dependency(request: Request) -> UpdateAccount:
    return UpdateAccount(
        user_id = getattr(request, "user_id"),
        enrich_accounts=await enrich_accounts_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def get_available_accounts_by_user_dependency(request: Request) -> GetAvailableAccountsByUser:
    return GetAvailableAccountsByUser(
        user_id = getattr(request, "user_id"),
        enrich_accounts=await enrich_accounts_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def get_available_accounts_by_ids_dependency(request: Request) -> GetAvailableAccountsByIds:
    return GetAvailableAccountsByIds(
        user_id = getattr(request, "user_id"),
        enrich_accounts = await enrich_accounts_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )

async def get_available_accounts_by_ids_internal_dependency(request: Request) -> GetAvailableAccountsByIdsInternal:
    return GetAvailableAccountsByIdsInternal(
        user_id = getattr(request, "user_id"),
        enrich_accounts = await enrich_accounts_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )
