
from fastapi import Request

from sweet_cash.repositories.accounts_repository import AccountsRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.services.account.create_account import CreateAccount
from sweet_cash.services.account.update_account import UpdateAccount
from sweet_cash.services.account.get_accounts_by_ids import GetAccounts
from sweet_cash.services.account.get_user_accounts import GetUserAccounts


async def accounts_repository_dependency(request: Request) -> AccountsRepository:
    engine = request.app.state.db
    return AccountsRepository(engine)


async def users_repository_dependency(request: Request) -> UsersRepository:
    engine = request.app.state.db
    return UsersRepository(engine)


async def create_account_dependency(request: Request) -> CreateAccount:
    return CreateAccount(
        user_id=getattr(request, "user_id"),
        accounts_repository = await accounts_repository_dependency(request),
        user_repository = await users_repository_dependency(request)
    )


async def update_account_dependency(request: Request) -> UpdateAccount:
    return UpdateAccount(
        user_id=getattr(request, "user_id"),
        accounts_repository = await accounts_repository_dependency(request),
        user_repository = await users_repository_dependency(request)
    )


async def get_user_accounts_dependency(request: Request) -> GetUserAccounts:
    return GetUserAccounts(
        user_id=getattr(request, "user_id"),
        accounts_repository = await accounts_repository_dependency(request),
        user_repository = await users_repository_dependency(request)
    )


async def get_accounts_dependency(request: Request) -> GetAccounts:
    return GetAccounts(
        user_id=getattr(request, "user_id"),
        accounts_repository = await accounts_repository_dependency(request),
        user_repository = await users_repository_dependency(request)
    )
