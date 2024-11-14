import logging
from fastapi import APIRouter, Depends
from typing import List

from sweet_cash.dependencies.debts_dependencies import (
    create_debt_dependency,
    update_debt_dependency,
    get_debts_by_user_dependency,
    get_debts_by_ids_dependency
)

from sweet_cash.services.debts.create_debt import CreateDebt
from sweet_cash.services.debts.get_debts_by_user import GetDebtsByUser
from sweet_cash.services.debts.get_debts_by_ids import GetDebtsByIds
from sweet_cash.services.debts.update_debt import UpdateDebt

from sweet_cash.types.debts_types import (
    DebtModel,
    DebtResponseModel,
    CreateDebtModel
)

from sweet_cash.auth.auth_bearer import JWTBearer


logger = logging.getLogger(name="accounts")

debt_api_router = APIRouter()


@debt_api_router.post("/debts",
                      response_model=DebtResponseModel,
                      dependencies=[Depends(JWTBearer())],
                      tags=["Debts"])
async def create_debt(
    body: CreateDebtModel,
    create_debt_: CreateDebt = Depends(dependency=create_debt_dependency)
) -> DebtModel:
    return await create_debt_(body)


@debt_api_router.put("/debts/{debt_id}",
                     response_model=DebtResponseModel,
                     dependencies=[Depends(JWTBearer())],
                     tags=["Debts"])
async def update_debt(
    debt_id: int,
    body: CreateDebtModel,
    update_debt_: UpdateDebt = Depends(dependency=update_debt_dependency)
) -> DebtModel:
    return await update_debt_(debt_id, body)


@debt_api_router.get("/debts/by_user",
                     response_model=List[DebtResponseModel],
                     dependencies=[Depends(JWTBearer())],
                     tags=["Debts"])
async def get_user_debts(
    get_user_debts_: GetDebtsByUser = Depends(dependency=get_debts_by_user_dependency)
) -> List[DebtModel]:
    return await get_user_debts_()


@debt_api_router.get("/debts",
                     response_model=List[DebtResponseModel],
                     dependencies=[Depends(JWTBearer())],
                     tags=["Debts"])
async def get_debts(
    ids: str,
    get_debts_: GetDebtsByIds = Depends(dependency=get_debts_by_ids_dependency)
) -> List[DebtModel]:
    return await get_debts_(debt_ids=ids)