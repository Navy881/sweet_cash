
import logging
from fastapi import APIRouter, Depends
from typing import List

from sweet_cash.api.dependencies.transactions_dependencies import (
    create_transaction_dependency,
    get_all_transactions_dependency,
    get_transactions_dependency,
    update_transaction_dependency,
    delete_transaction_dependency
)
from sweet_cash.api.services.transactions.create_transaction import CreateTransaction
from sweet_cash.api.services.transactions.get_transactions import GetAllTransactions
from sweet_cash.api.services.transactions.get_transaction import GetTransactions
from sweet_cash.api.services.transactions.update_transaction import UpdateTransaction
from sweet_cash.api.services.transactions.delete_transaction import DeleteTransaction
from sweet_cash.api.types.transactions_types import TransactionModel, CreateTransactionModel
from sweet_cash.api.auth.auth_bearer import JWTBearer


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

# from flask import request, Blueprint
# import logging
#
# from api.api import SuccessResponse, auth, jsonbody, query_params, features, formatting
# from api.services.transactions.create_transaction import CreateTransaction
# from api.services.transactions.update_transaction import UpdateTransaction
# from api.services.transactions.get_transaction import GetTransactions
# from api.services.transactions.get_transactions import GetAllTransactions
# from api.services.transactions.delete_transaction import DeleteTransaction
# from api.services.transactions.get_categories import GetCategories
#
# logger = logging.getLogger(name="transactions")
#
# transactions_api = Blueprint('transactions', __name__)
#
#
# @transactions_api.route('/transactions', methods=['POST'])
# @auth()
# @jsonbody(event_id=features(type=int, required=True),
#           transaction_date=features(type=str, required=True),
#           type=features(type=str, required=True),
#           category=features(type=int, required=True),
#           amount=features(type=float, required=True),
#           receipt_id=features(type=int),
#           description=features(type=str))
# def create_transaction(event_id: int,
#                        transaction_date: str,
#                        type: str,
#                        category: int,
#                        amount: float,
#                        receipt_id=None,
#                        description=None,
#                        create_transaction=CreateTransaction()):
#     """
#     Create new user transaction
#
#         Returns 401 if
#
#         Returns structure like
#         {
#             "amount": 2.05,
#             "category": "Категория 3",
#             "created_at": "Mon, 18 Oct 2021 16:28:33 GMT",
#             "description": "description",
#             "id": 12,
#             "transaction_date": "Sun, 10 Oct 2021 04:25:03 GMT",
#             "type": "Тип 3"
#         }
#
#         or code 404 if
#         {
#         }
#     """
#     result = formatting(create_transaction(user_id=getattr(request, "user_id"),
#                                            event_id=event_id,
#                                            transaction_date=transaction_date,
#                                            type=type,
#                                            category_id=category,
#                                            amount=amount,
#                                            receipt_id=receipt_id,
#                                            description=description))
#
#     return SuccessResponse(result)
#
#
# @transactions_api.route('/transactions/all', methods=['GET'])
# @auth()
# @query_params(event_id=features(type=str, required=True),
#               start=features(type=str, required=True),
#               end=features(type=str, required=True),
#               limit=features(type=str),
#               offset=features(type=str))
# def get_transactions(event_id: int,
#                      start=None,
#                      end=None,
#                      limit=100,
#                      offset=0,
#                      get_all_transactions=GetAllTransactions()):
#     transactions = get_all_transactions(user_id=getattr(request, "user_id"),
#                                         event_id=event_id,
#                                         start=start,
#                                         end=end,
#                                         limit=int(limit),
#                                         offset=int(offset))
#     result = [formatting(item) for item in transactions]
#     return SuccessResponse(result)
#
#
# @transactions_api.route('/transactions', methods=['GET'])
# @auth()
# @query_params(ids=features(type=str))
# def get_transactions_by_id(ids=None, get_transactions=GetTransactions()):
#     transactions = get_transactions(user_id=getattr(request, "user_id"),
#                                     transaction_ids=ids)
#     result = [formatting(item) for item in transactions]
#     return SuccessResponse(result)
#
#
# @transactions_api.route('/transactions/<int:transaction_id>', methods=['PUT'])
# @auth()
# @jsonbody(transaction_date=features(type=str, required=True),
#           type=features(type=str, required=True),
#           category=features(type=int, required=True),
#           amount=features(type=float, required=True),
#           receipt_id=features(type=int),
#           description=features(type=str))
# def update_transaction(transaction_id: int,
#                        transaction_date: str,
#                        type: str,
#                        category: int,
#                        amount: float,
#                        receipt_id=None,
#                        description=None,
#                        update_transaction=UpdateTransaction()):
#     result = formatting(update_transaction(user_id=getattr(request, "user_id"),
#                                            transaction_id=transaction_id,
#                                            transaction_date=transaction_date,
#                                            type=type,
#                                            category_id=category,
#                                            amount=amount,
#                                            receipt_id=receipt_id,
#                                            description=description))
#     return SuccessResponse(result)
#
#
# @transactions_api.route('/transactions/<int:transaction_id>', methods=['DELETE'])
# @auth()
# def delete_transaction(transaction_id: int, delete_transaction=DeleteTransaction()):
#     result = delete_transaction(user_id=getattr(request, "user_id"),
#                                 transaction_id=transaction_id)
#     return SuccessResponse(f'{result} transactions deleted')
#
#
# @transactions_api.route('/transactions/categories', methods=['GET'])
# @auth()
# def get_categories(get_categories=GetCategories()):
#     categories = get_categories(user_id=getattr(request, "user_id"))
#     result = [formatting(item) for item in categories]
#     return SuccessResponse(result)
