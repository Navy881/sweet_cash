import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.transactions.enrich_transactions import EnrichTransactions
from sweet_cash.services.account.get_accounts_by_ids import GetAccountsByIds
from sweet_cash.services.transaction_categories.get_transaction_category_by_id import GetTransactionCategoryBiId
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser

from sweet_cash.repositories.transactions_repository import TransactionsRepository

from sweet_cash.types.transactions_types import TransactionModel, UpdateTransactionModel
from sweet_cash.types.accounts_types import AccountModel
from sweet_cash.types.events_types import EventParticipantRole

from sweet_cash.errors import APIConflict, APIValueNotFound


logger = logging.getLogger(name="transactions")


class UpdateTransaction(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_transactions: EnrichTransactions,
                 get_accounts_by_ids: GetAccountsByIds,
                 get_transaction_category_by_id: GetTransactionCategoryBiId,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 transactions_repository: TransactionsRepository) -> None:
        self.user_id = user_id
        self.enrich_transactions = enrich_transactions
        self.get_accounts_by_ids = get_accounts_by_ids
        self.get_transaction_category_by_id = get_transaction_category_by_id
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.transactions_repository = transactions_repository
        self.source_account = None
        self.target_account = None

    async def __call__(self, transaction_id: int, transaction: UpdateTransactionModel) -> TransactionModel:
        transaction_category_id: int = transaction.category_id

        # Проверка только по id, т.к. пользователь может создавать
        # транзкации со счётом, к которому у него нет доступа
        accounts: Dict[int, AccountModel] = await self.get_accounts_by_ids([transaction.source_account_id,
                                                                            transaction.target_account_id])
        if transaction.source_account_id is not None:
            try:
                self.source_account = accounts[transaction.source_account_id]
            except KeyError as e:
                logger.error(e)
            if self.source_account is None:
                raise APIValueNotFound(f'Account {transaction.source_account_id} not found')

        if transaction.target_account_id is not None:
            try:
                self.target_account = accounts[transaction.target_account_id]
            except KeyError as e:
                logger.error(e)
            if self.target_account is None:
                raise APIValueNotFound(f'Account {transaction.target_account_id} not found')

        # Checking exist transaction category
        await self.get_transaction_category_by_id(transaction_category_id)

        async with self.transactions_repository.transaction():
            # Checking access to transaction
            transaction_model = await self.transactions_repository.get_transaction_by_id(transaction_id)
            if transaction_model is None:
                raise APIValueNotFound(f'Transaction {transaction_id} not found')

            event_id: int = transaction_model.event_id

            if transaction_model.user_id != self.user_id:
                # Checking that user in event
                users_roles: List[EventParticipantRole] = \
                    await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)

                if EventParticipantRole.MANAGER not in users_roles:
                    raise APIConflict(f'User {self.user_id} cannot change the transaction {transaction_id}')
                    
            transaction_model = await self.transactions_repository.update_transaction(transaction_id=transaction_id,
                                                                                      transaction=transaction)

            result = await self.enrich_transactions([transaction_model])
            return result[0]