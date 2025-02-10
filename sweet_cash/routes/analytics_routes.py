import logging
from fastapi import APIRouter, Depends

from sweet_cash.dependencies.analytics_dependencies import (
    get_account_balance_dependency
)

from sweet_cash.services.analytics.get_account_balance import GetAccountBalance

from sweet_cash.types.analytics_types import (
    AccountBalanceModel
)

from sweet_cash.auth.auth_bearer import JWTBearer


logger = logging.getLogger(name="analytics")

analytics_api_router = APIRouter()


@analytics_api_router.get("/analytics/accountBalance/{account_id}",
                         response_model=AccountBalanceModel,
                         dependencies=[Depends(JWTBearer())],
                         tags=["Analytics"])
async def get_account_balance(
    account_id: int,
    get_account_balance_: GetAccountBalance = Depends(dependency=get_account_balance_dependency)
) -> AccountBalanceModel:
    return await get_account_balance_(account_id)