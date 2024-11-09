from fastapi import Request

from sweet_cash.repositories.accounts_repository import AccountsRepository
from sweet_cash.repositories.accounts_admitted_users_repository import AccountsAdmittedUsersRepository

from sweet_cash.services.account.create_account import CreateAccount
from sweet_cash.services.account.update_account import UpdateAccount
from sweet_cash.services.account.get_account_by_id import GetAccountById
from sweet_cash.services.account.get_available_accounts_by_ids import GetAvailableAccountsByIds
from sweet_cash.services.account.get_available_accounts_by_user import GetAvailableAccountsByUser
from sweet_cash.services.account.create_accounts_admitted_user import CreateAccountsAdmittedUser
from sweet_cash.services.account.delete_accounts_admitted_user import DeleteAccountsAdmittedUser
from sweet_cash.services.account.get_accounts_by_admitted_user import GetAccountsByAdmittedUser
from sweet_cash.services.account.get_accounts_admitted_users_by_account import GetAccountsAdmittedUsersByAccount
from sweet_cash.services.account.get_available_account_by_id import GetAvailableAccountById
from sweet_cash.services.account.get_accounts_admitted_user_by_account_id_and_user_id import (
    GetAccountsAdmittedUserByAccountIdAndUserId
)

from sweet_cash.dependencies.users_dependecies import get_user_by_id_dependency


async def accounts_repository_dependency(request: Request) -> AccountsRepository:
    engine = request.app.state.db
    return AccountsRepository(engine)


async def accounts_admitted_users_repository_dependency(request: Request) -> AccountsAdmittedUsersRepository:
    engine = request.app.state.db
    return AccountsAdmittedUsersRepository(engine)


async def create_account_dependency(request: Request) -> CreateAccount:
    return CreateAccount(
        user_id = getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def get_account_by_id_dependency(request: Request) -> GetAccountById:
    return GetAccountById(
        user_id = getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def create_accounts_admitted_user_dependency(request: Request) -> CreateAccountsAdmittedUser:
    return CreateAccountsAdmittedUser(
        user_id = getattr(request, "user_id"),
        get_accounts_by_id = await get_account_by_id_dependency(request),
        accounts_admitted_users_repository = await accounts_admitted_users_repository_dependency(request)
    )


async def get_accounts_by_admitted_user_dependency(request: Request) -> GetAccountsByAdmittedUser:
    return GetAccountsByAdmittedUser(
        user_id = getattr(request, "user_id"),
        get_accounts_by_ids = await get_available_accounts_by_ids_dependency(request),
        accounts_admitted_users_repository = await accounts_admitted_users_repository_dependency(request)
    )


async def get_admitted_users_by_accounts_dependency(request: Request) -> GetAccountsAdmittedUsersByAccount:
    return GetAccountsAdmittedUsersByAccount(
        user_id = getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        accounts_admitted_users_repository = await accounts_admitted_users_repository_dependency(request)
    )


async def delete_accounts_admitted_user_dependency(request: Request) -> DeleteAccountsAdmittedUser:
    return DeleteAccountsAdmittedUser(
        user_id = getattr(request, "user_id"),
        get_account_by_id = await get_account_by_id_dependency(request),
        accounts_admitted_users_repository = await accounts_admitted_users_repository_dependency(request)
    )


async def update_account_dependency(request: Request) -> UpdateAccount:
    return UpdateAccount(
        user_id = getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_admitted_users_by_account = await get_admitted_users_by_accounts_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def get_available_accounts_by_user_dependency(request: Request) -> GetAvailableAccountsByUser:
    return GetAvailableAccountsByUser(
        user_id = getattr(request, "user_id"),
        get_accounts_by_admitted_user = await get_accounts_by_admitted_user_dependency(request),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_admitted_users_by_account = await get_admitted_users_by_accounts_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )


async def get_accounts_admitted_user_by_account_id_and_user_id_dependency(request: Request
    ) -> GetAccountsAdmittedUserByAccountIdAndUserId:
    return GetAccountsAdmittedUserByAccountIdAndUserId(
        user_id = getattr(request, "user_id"),
        accounts_admitted_users_repository = await accounts_admitted_users_repository_dependency(request)
    )


async def get_available_accounts_by_ids_dependency(request: Request) -> GetAvailableAccountsByIds:
    return GetAvailableAccountsByIds(
        user_id = getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_admitted_users_by_account = await get_admitted_users_by_accounts_dependency(request),
        get_admitted_user_by_account_id_and_user_id = \
            await get_accounts_admitted_user_by_account_id_and_user_id_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )

async def get_available_accounts_by_id_dependency(request: Request) -> GetAvailableAccountById:
    return GetAvailableAccountById(
        user_id = getattr(request, "user_id"),
        get_user_by_id = await get_user_by_id_dependency(request),
        get_admitted_users_by_account = await get_admitted_users_by_accounts_dependency(request),
        get_admitted_user_by_account_id_and_user_id = \
            await get_accounts_admitted_user_by_account_id_and_user_id_dependency(request),
        accounts_repository = await accounts_repository_dependency(request)
    )

