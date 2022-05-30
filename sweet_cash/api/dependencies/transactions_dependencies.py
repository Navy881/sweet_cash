
from fastapi import Request

from api.repositories.transactions_repository import TransactionsRepository
from api.repositories.transaction_categories_repository import TransactionCategoriesRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.services.transactions.create_transaction import CreateTransaction
from api.services.transactions.get_transactions import GetAllTransactions
from api.services.transactions.get_transaction import GetTransactions
from api.services.transactions.update_transaction import UpdateTransaction
from api.services.transactions.delete_transaction import DeleteTransaction
from db import engine


def transactions_repository_dependency(request: Request) -> TransactionsRepository:
    pg_engine = request
    return TransactionsRepository()


def transaction_categories_repository_dependency(request: Request) -> TransactionCategoriesRepository:
    pg_engine = request
    return TransactionCategoriesRepository()


def events_participants_repository_dependency(request: Request) -> EventsParticipantsRepository:
    pg_engine = request
    return EventsParticipantsRepository()


def create_transaction_dependency(request: Request) -> CreateTransaction:
    return CreateTransaction(
        user_id=getattr(request, "user_id"),
        transaction_categories_repository=transaction_categories_repository_dependency(request),
        events_participants_repository=events_participants_repository_dependency(request),
        transactions_repository=transactions_repository_dependency(request)
    )


def get_all_transactions_dependency(request: Request) -> GetAllTransactions:
    return GetAllTransactions(
        user_id=getattr(request, "user_id"),
        events_participants_repository=events_participants_repository_dependency(request),
        transactions_repository=transactions_repository_dependency(request)
    )


def get_transactions_dependency(request: Request) -> GetTransactions:
    return GetTransactions(
        user_id=getattr(request, "user_id"),
        events_participants_repository=events_participants_repository_dependency(request),
        transactions_repository=transactions_repository_dependency(request)
    )


def update_transaction_dependency(request: Request) -> UpdateTransaction:
    return UpdateTransaction(
        user_id=getattr(request, "user_id"),
        transaction_categories_repository=transaction_categories_repository_dependency(request),
        events_participants_repository=events_participants_repository_dependency(request),
        transactions_repository=transactions_repository_dependency(request)
    )


def delete_transaction_dependency(request: Request) -> DeleteTransaction:
    return DeleteTransaction(
        user_id=getattr(request, "user_id"),
        events_participants_repository=events_participants_repository_dependency(request),
        transactions_repository=transactions_repository_dependency(request)
    )
