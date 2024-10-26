
import logging
from fastapi import APIRouter, Depends
from typing import List

from sweet_cash.dependencies.accounts_dependencies import (
    create_account_dependency,
    update_account_dependency,
    get_accounts_dependency,
    get_user_accounts_dependency
)
from sweet_cash.services.account.create_account import CreateAccount
from sweet_cash.services.account.update_account import UpdateAccount
from sweet_cash.services.account.get_accounts_by_ids import GetAccounts
from sweet_cash.services.account.get_user_accounts import GetUserAccounts
from sweet_cash.types.accounts_types import AccountResponseModel, CreateAccountModel, UpdateAccountModel, AccountModel
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
    with_blocked = False,
    get_user_accounts_: GetUserAccounts = Depends(dependency=get_user_accounts_dependency)
) -> List[AccountModel]:
    return await get_user_accounts_(with_blocked)


@accounts_api_router.get("/accounts",
                         response_model=List[AccountResponseModel],
                         dependencies=[Depends(JWTBearer())],
                         tags=["Accounts"])
async def get_accounts(
    account_ids: str,
    get_accounts_: GetAccounts = Depends(dependency=get_accounts_dependency)
) -> List[AccountModel]:
    return await get_accounts_(account_ids)
