
import logging
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.events_participants_repository import EventsParticipantsRepository
from sweet_cash.repositories.transactions_repository import TransactionsRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.repositories.accounts_repository import AccountsRepository
from sweet_cash.types.transactions_types import TransactionModel
from sweet_cash.types.events_participants_types import EventParticipantRole
from sweet_cash.types.users_types import UserResponseModel
from sweet_cash.types.accounts_types import AccountResponseModel
from sweet_cash.utils import ids2list


logger = logging.getLogger(name="transactions")


class GetTransactions(BaseService):
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

    async def __call__(self, transaction_ids: str) -> List[TransactionModel]:
        transaction_ids: List[id] = ids2list(transaction_ids)
        result: List = []

        async with self.transactions_repository.transaction():
            transactions: List[TransactionModel] = await self.transactions_repository.get_transactions(transaction_ids)

        async with self.accounts_repository.transaction():
            async with self.events_participants_repository.transaction():
                async with self.user_repository.transaction():
                    for transaction in transactions:
                        if transaction.user_id != self.user_id:
                            if not await self.events_participants_repository. \
                                    check_exist_events_participant_by_role(user_id=self.user_id,
                                                                        event_id=transaction.event_id,
                                                                        role=EventParticipantRole.MANAGER.name):
                                continue
                        
                        # Update transactions user
                        user = await self.user_repository.get_by_id(transaction.user_id)
                        transaction.user = UserResponseModel(**user.dict())

                        # Update transactions accounts
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

                        result.append(transaction)
        
        return result
