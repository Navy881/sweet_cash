
import logging
from fastapi import APIRouter, Depends
from typing import List

from sweet_cash.dependencies.transactions_dependencies import (
    create_transaction_dependency,
    get_all_transactions_dependency,
    get_transactions_dependency,
    update_transaction_dependency,
    delete_transaction_dependency
)
from sweet_cash.services.transactions.create_transaction import CreateTransaction
from sweet_cash.services.transactions.get_transactions import GetAllTransactions
from sweet_cash.services.transactions.get_transaction import GetTransactions
from sweet_cash.services.transactions.update_transaction import UpdateTransaction
from sweet_cash.services.transactions.delete_transaction import DeleteTransaction
from sweet_cash.types.transactions_types import TransactionModel, CreateTransactionModel
from sweet_cash.auth.auth_bearer import JWTBearer


logger = logging.getLogger(name="transactions")

transactions_api_router = APIRouter()


@transactions_api_router.post("/transactions",
                              response_model=TransactionModel,
                              dependencies=[Depends(JWTBearer())],
                              tags=["Transactions"])
async def create_transaction(
        body: CreateTransactionModel,
        create_transaction_: CreateTransaction = Depends(dependency=create_transaction_dependency)
) -> TransactionModel:
    return await create_transaction_(body)


@transactions_api_router.get("/transactions/all",
                             response_model=List[TransactionModel],
                             dependencies=[Depends(JWTBearer())],
                             tags=["Transactions"])
async def get_all_transactions(
        event_id: int,
        start: str,
        end: str,
        limit: int,
        offset: int,
        get_all_transactions_: GetAllTransactions = Depends(dependency=get_all_transactions_dependency)
) -> List[TransactionModel]:
    return await get_all_transactions_(event_id, start, end, limit, offset)


@transactions_api_router.get("/transactions",
                             response_model=List[TransactionModel],
                             dependencies=[Depends(JWTBearer())],
                             tags=["Transactions"])
async def get_transactions(
        transaction_ids: str,
        get_transactions_: GetTransactions = Depends(dependency=get_transactions_dependency)
) -> List[TransactionModel]:
    return await get_transactions_(transaction_ids)


@transactions_api_router.put("/transactions/{transaction_id}",
                             response_model=TransactionModel,
                             dependencies=[Depends(JWTBearer())],
                             tags=["Transactions"])
async def update_transaction(
        transaction_id: int,
        body: CreateTransactionModel,
        update_transaction_: UpdateTransaction = Depends(dependency=update_transaction_dependency)
) -> TransactionModel:
    return await update_transaction_(transaction_id, body)


@transactions_api_router.delete("/transactions/{transaction_id}",
                                response_model=TransactionModel,
                                dependencies=[Depends(JWTBearer())],
                                tags=["Transactions"])
async def delete_transaction(
        transaction_id: int,
        delete_transaction_: DeleteTransaction = Depends(dependency=delete_transaction_dependency)
) -> TransactionModel:
    return await delete_transaction_(transaction_id)
