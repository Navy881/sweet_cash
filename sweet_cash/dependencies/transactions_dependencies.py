
from fastapi import Request

from sweet_cash.repositories.transactions_repository import TransactionsRepository
from sweet_cash.repositories.transaction_categories_repository import TransactionCategoriesRepository
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.services.transactions.create_transaction import CreateTransaction
from sweet_cash.services.transactions.get_transactions import GetAllTransactions
from sweet_cash.services.transactions.get_transaction import GetTransactions
from sweet_cash.services.transactions.update_transaction import UpdateTransaction
from sweet_cash.services.transactions.delete_transaction import DeleteTransaction


async def transactions_repository_dependency(request: Request) -> TransactionsRepository:
    engine = request.app.state.db
    return TransactionsRepository(engine)


async def transaction_categories_repository_dependency(request: Request) -> TransactionCategoriesRepository:
    engine = request.app.state.db
    return TransactionCategoriesRepository(engine)


async def events_participants_repository_dependency(request: Request) -> EventsParticipantsRepository:
    engine = request.app.state.db
    return EventsParticipantsRepository(engine)


async def create_transaction_dependency(request: Request) -> CreateTransaction:
    return CreateTransaction(
        user_id=getattr(request, "user_id"),
        transaction_categories_repository = await transaction_categories_repository_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def get_all_transactions_dependency(request: Request) -> GetAllTransactions:
    return GetAllTransactions(
        user_id=getattr(request, "user_id"),
        events_participants_repository = await events_participants_repository_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def get_transactions_dependency(request: Request) -> GetTransactions:
    return GetTransactions(
        user_id=getattr(request, "user_id"),
        events_participants_repository = await events_participants_repository_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def update_transaction_dependency(request: Request) -> UpdateTransaction:
    return UpdateTransaction(
        user_id=getattr(request, "user_id"),
        transaction_categories_repository = await transaction_categories_repository_dependency(request),
        events_participants_repository = await events_participants_repository_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )


async def delete_transaction_dependency(request: Request) -> DeleteTransaction:
    return DeleteTransaction(
        user_id=getattr(request, "user_id"),
        events_participants_repository = await events_participants_repository_dependency(request),
        transactions_repository = await transactions_repository_dependency(request)
    )
