from fastapi import APIRouter, Depends
from typing import List

from api.dependencies.transaction_categories_dependencies import (
    create_transaction_categories_dependency,
    get_transaction_categories_dependency,
    update_transaction_categories_dependency,
    delete_transaction_categories_dependency
)
from api.services.transaction_categories.create_transaction_category import CreateTransactionCategory
from api.services.transaction_categories.get_transaction_categories import GetTransactionCategories
from api.services.transaction_categories.update_transaction_category import UpdateTransactionCategory
from api.services.transaction_categories.delete_transaction_category import DeleteTransactionCategory
from api.types.transaction_categories_types import TransactionCategoryModel, CreateTransactionCategoryModel
from api.auth.auth_bearer import JWTBearer

import logging

logger = logging.getLogger(name="transactions_categories")

transaction_category_api_router = APIRouter()


@transaction_category_api_router.post("/api/v1/transaction/categories",
                                      response_model=TransactionCategoryModel,
                                      dependencies=[Depends(JWTBearer())],
                                      tags=["Transactions categories"])
async def create_transaction_category(
        body: CreateTransactionCategoryModel,
        create_transaction_category_: CreateTransactionCategory = Depends(
            dependency=create_transaction_categories_dependency)
) -> TransactionCategoryModel:
    return await create_transaction_category_(body)


@transaction_category_api_router.get("/api/v1/transaction/categories",
                                     response_model=List[TransactionCategoryModel],
                                     dependencies=[Depends(JWTBearer())],
                                     tags=["Transactions categories"])
async def get_transaction_categories(
        get_transaction_categories_: GetTransactionCategories = Depends(
            dependency=get_transaction_categories_dependency)
) -> List[TransactionCategoryModel]:
    return await get_transaction_categories_()


@transaction_category_api_router.put("/api/v1/transaction/categories/{transaction_category_id}",
                                     response_model=TransactionCategoryModel,
                                     dependencies=[Depends(JWTBearer())],
                                     tags=["Transactions categories"])
async def update_transaction_category(
        transaction_category_id: int,
        body: CreateTransactionCategoryModel,
        update_transaction_category_: UpdateTransactionCategory = Depends(
            dependency=update_transaction_categories_dependency)
) -> TransactionCategoryModel:
    return await update_transaction_category_(transaction_category_id, body)


@transaction_category_api_router.delete("/api/v1/transaction/categories/{transaction_category_id}",
                                        response_model=TransactionCategoryModel,
                                        dependencies=[Depends(JWTBearer())],
                                        tags=["Transactions categories"])
async def delete_transaction_category(
        transaction_category_id: int,
        delete_transaction_category_: DeleteTransactionCategory = Depends(
            dependency=delete_transaction_categories_dependency)
) -> TransactionCategoryModel:
    return await delete_transaction_category_(transaction_category_id)
