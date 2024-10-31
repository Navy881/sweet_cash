
import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.repositories.transactions_repository import TransactionsRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.repositories.accounts_repository import AccountsRepository
from sweet_cash.types.transactions_types import TransactionModel
from sweet_cash.types.events_participants_types import EventsParticipantsModel, EventParticipantRole
from sweet_cash.types.users_types import UserResponseModel
from sweet_cash.types.accounts_types import AccountResponseModel
from sweet_cash.errors import APIValueNotFound, APIConflict


logger = logging.getLogger(name="transactions")


class DeleteTransaction(BaseService):
    def __init__(self,
                 user_id: int,
                 events_participants_repository: EventsParticipantsRepository,
                 transactions_repository: TransactionsRepository,
                 user_repository: UsersRepository,
                 accounts_repository: AccountsRepository) -> None:
        self.user_id = user_id
        self.events_participants_repository = events_participants_repository
        self.transactions_repository = transactions_repository
        self.user_repository = user_repository
        self.accounts_repository = accounts_repository

    async def __call__(self, transaction_id: int) -> TransactionModel:
        async with self.transactions_repository.transaction():
            transaction: TransactionModel = await self.transactions_repository.get_transaction_by_id(transaction_id)
            event_id: int = transaction.event_id

            async with self.events_participants_repository.transaction():
                # Checking that user in event
                event_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
                    get_events_participants_by_user_id(user_id=self.user_id, event_id=event_id)

                if len(event_participants) == 0:
                    raise APIValueNotFound(f'User {self.user_id} not associated with the event for transaction '
                                           f'{transaction_id}')

                if self.user_id != transaction.user_id:
                    if EventParticipantRole.MANAGER not in \
                            [event_participant.role for event_participant in event_participants]:
                        raise APIConflict(f'Updating a transaction {transaction_id} unavailable for user {self.user_id}')

                
                transaction = await self.transactions_repository.delete_transaction(transaction_id)
            
        # Update transactions user
        async with self.user_repository.transaction():
            user = await self.user_repository.get_by_id(transaction.user_id)
            transaction.user = UserResponseModel(**user.dict())

        # Update transactions accounts
        async with self.accounts_repository.transaction():
            if transaction.source_account_id:
                account = await self.accounts_repository.get_user_account_by_id(account_id=transaction.source_account_id,
                                                                                user_id=self.user_id)
                if account:
                    transaction.source_account = AccountResponseModel(**account.dict())
                else:
                    transaction.source_account = AccountResponseModel(id=transaction.source_account_id)

            if transaction.target_account_id:
                account = await self.accounts_repository.get_user_account_by_id(account_id=transaction.target_account_id,
                                                                                user_id=self.user_id)  
                if account:
                    transaction.target_account = AccountResponseModel(**account.dict())
                else:
                    transaction.target_account = AccountResponseModel(id=transaction.target_account_id)

        return transaction
