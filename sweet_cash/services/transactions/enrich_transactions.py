import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_users_by_ids import GetUsersByIds
from sweet_cash.services.account.get_available_accounts_by_ids import GetAvailableAccountsByIdsInternal
from sweet_cash.services.events.get_events_by_ids import GetEventsByIdsInternal

from sweet_cash.types.users_types import UserModel
from sweet_cash.types.transactions_types import TransactionModel
from sweet_cash.types.accounts_types import AccountModel
from sweet_cash.types.events_types import EventModel


logger = logging.getLogger(name="transactions")


class EnrichTransactions(BaseService):
    def __init__(self,
                 user_id: int,
                 get_users_by_ids: GetUsersByIds,
                 get_available_accounts_by_ids: GetAvailableAccountsByIdsInternal,
                 get_events_by_ids: GetEventsByIdsInternal) -> None:
        self.user_id = user_id
        self.get_users_by_ids = get_users_by_ids
        self.get_available_accounts_by_ids = get_available_accounts_by_ids
        self.get_events_by_ids = get_events_by_ids

    async def __call__(self, transactions: List[TransactionModel]) -> List[TransactionModel]:
        users: Dict[int, UserModel] = await self.get_users_by_ids(
            list(set([transaction.user_id for transaction in transactions]))
        )

        accounts_ids = [account_id for transaction in transactions for account_id in
                        (transaction.source_account_id, transaction.target_account_id)]
        available_accounts: Dict[int, AccountModel] = await self.get_available_accounts_by_ids(
            list(set(accounts_ids))
        )

        events: Dict[int, EventModel] = await self.get_events_by_ids(
            list(set([transaction.event_id for transaction in transactions]))
        )


        for transaction in transactions:
            try:
                transaction.user = users[transaction.user_id]
            except KeyError:
                transaction.user = None

            try:
                transaction.source_account = available_accounts[transaction.source_account_id]
            except KeyError:
                transaction.source_account = None

            try:
                transaction.target_account = available_accounts[transaction.target_account_id]
            except KeyError:
                transaction.target_account = None

            try:
                transaction.event = events[transaction.event_id]
            except KeyError:
                transaction.event = None

        return transactions
