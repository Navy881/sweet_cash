import logging
from fastapi import APIRouter, Depends
from typing import List

from sweet_cash.dependencies.accounts_dependencies import (
    create_account_dependency,
    update_account_dependency,
    get_available_accounts_by_ids_dependency,
    get_available_accounts_by_user_dependency,
    create_accounts_admitted_user_dependency,
    delete_accounts_admitted_user_dependency
)

from sweet_cash.services.account.create_account import CreateAccount
from sweet_cash.services.account.update_account import UpdateAccount
from sweet_cash.services.account.get_available_accounts_by_ids import GetAvailableAccountsByIds
from sweet_cash.services.account.get_available_accounts_by_user import GetAvailableAccountsByUser
from sweet_cash.services.account.create_accounts_admitted_user import CreateAccountsAdmittedUser
from sweet_cash.services.account.delete_accounts_admitted_user import DeleteAccountsAdmittedUser

from sweet_cash.types.accounts_types import (
    AccountResponseModel,
    CreateAccountModel,
    UpdateAccountModel,
    AccountModel,
    AccountsAdmittedUsersModel
)

from sweet_cash.auth.auth_bearer import JWTBearer


logger = logging.getLogger(name="accounts")

accounts_api_router = APIRouter()


@accounts_api_router.post("/accounts",
                          response_model=AccountResponseModel,
                          dependencies=[Depends(JWTBearer())],
                          tags=["Accounts"])
async def create_account(
    body: CreateAccountModel,
    create_account_: CreateAccount = Depends(dependency=create_account_dependency)
) -> AccountModel:
    return await create_account_(body)


@accounts_api_router.put("/accounts/{account_id}",
                         response_model=AccountResponseModel,
                         dependencies=[Depends(JWTBearer())],
                         tags=["Accounts"])
async def update_account(
    account_id: int,
    body: UpdateAccountModel,
    update_account_: UpdateAccount = Depends(dependency=update_account_dependency)
) -> AccountModel:
    return await update_account_(account_id, body)


@accounts_api_router.get("/accounts/by_user",
                         response_model=List[AccountResponseModel],
                         dependencies=[Depends(JWTBearer())],
                         tags=["Accounts"])
async def get_user_accounts(
    with_blocked: bool = False,
    get_user_accounts_: GetAvailableAccountsByUser = Depends(dependency=get_available_accounts_by_user_dependency)
) -> List[AccountModel]:
    return await get_user_accounts_(with_blocked)


@accounts_api_router.get("/accounts",
                         response_model=List[AccountResponseModel],
                         dependencies=[Depends(JWTBearer())],
                         tags=["Accounts"])
async def get_accounts(
    ids: str,
    get_accounts_: GetAvailableAccountsByIds = Depends(dependency=get_available_accounts_by_ids_dependency)
) -> List[AccountModel]:
    return await get_accounts_(account_ids=ids, with_blocked=True)


@accounts_api_router.post("/accounts/{account_id}/addUser",
                         response_model=AccountsAdmittedUsersModel,
                         dependencies=[Depends(JWTBearer())],
                         tags=["Accounts"])
async def create_accounts_admitted_user(
    account_id: int,
    user_id: int,
    create_accounts_admitted_user_: CreateAccountsAdmittedUser = \
            Depends(dependency=create_accounts_admitted_user_dependency)
) -> AccountsAdmittedUsersModel:
    return await create_accounts_admitted_user_(account_id=account_id, user_id=user_id)


@accounts_api_router.delete("/accounts/{account_id}/deleteUser/{user_id}",
                         response_model=AccountsAdmittedUsersModel,
                         dependencies=[Depends(JWTBearer())],
                         tags=["Accounts"])
async def delete_accounts_admitted_user(
    account_id: int,
    user_id: int,
    delete_accounts_admitted_user_: DeleteAccountsAdmittedUser = \
            Depends(dependency=delete_accounts_admitted_user_dependency)
) -> AccountsAdmittedUsersModel:
    return await delete_accounts_admitted_user_(account_id=account_id, user_id=user_id)
