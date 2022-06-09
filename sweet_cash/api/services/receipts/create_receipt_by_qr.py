import logging
from datetime import datetime
from typing import List

from api.services.base_service import BaseService
from api.repositories.nalog_ru_sessions_repository import NalogRuSessionsRepository
from api.repositories.events_participants_repository import EventsParticipantsRepository
from api.repositories.receipts_repository import ReceiptsRepository
from api.repositories.transactions_repository import TransactionsRepository
from api.types.receipts_types import ReceiptModel, CreateReceiptModel
from api.types.events_participants_types import EventsParticipantsModel
from api.types.nalog_ru_types import NalogRuSessionModel, NalogRuReceiptModel
from api.types.transactions_types import CreateTransactionModel, TransactionType
from api.integrations.nalog_ru_api import NalogRuApi
from api.errors import APIValueNotFound

logger = logging.getLogger(name="receipts")


class CreateReceiptByQr(BaseService):
    def __init__(self,
                 user_id: int,
                 nalog_ru_sessions_repository: NalogRuSessionsRepository,
                 events_participants_repository: EventsParticipantsRepository,
                 receipts_repository: ReceiptsRepository,
                 transactions_repository: TransactionsRepository,
                 nalog_ru_api: NalogRuApi) -> None:
        self.user_id = user_id
        self.nalog_ru_sessions_repository = nalog_ru_sessions_repository
        self.events_participants_repository = events_participants_repository
        self.receipts_repository = receipts_repository
        self.transactions_repository = transactions_repository
        self.nalog_ru_api = nalog_ru_api

    async def __call__(self, receipt_qr: CreateReceiptModel) -> ReceiptModel:
        async with self.events_participants_repository.transaction():
            # Checking that user in event
            event_participants: List[EventsParticipantsModel] = await self.events_participants_repository. \
                get_events_participants_by_user_id(user_id=self.user_id, event_id=receipt_qr.event_id)

            if not event_participants:
                raise APIValueNotFound(f'User {self.user_id} not associated with the event {receipt_qr.event_id}')

        async with self.nalog_ru_sessions_repository.transaction():
            # Checking registered in NalogAPI
            nalog_ru_session: NalogRuSessionModel = await self.nalog_ru_sessions_repository. \
                get_session_by_user(self.user_id)

            # Update sessionId for NalogAPI
            new_nalog_ru_session: NalogRuSessionModel = await self.nalog_ru_api. \
                get_new_session_id(nalog_ru_session.refresh_token)

            await self.nalog_ru_sessions_repository.update_nalog_ru_session(user_id=self.user_id,
                                                                            nalog_ru_session=new_nalog_ru_session)

            # Get receipt data by qr
            receipt_data: NalogRuReceiptModel = await self.nalog_ru_api. \
                get_receipt(session_id=new_nalog_ru_session.sessionId, qr=receipt_qr.qr)

        async with self.receipts_repository.transaction():
            # Save receipt
            receipt: ReceiptModel = await self.receipts_repository. \
                create_receipt_from_nalog_ru_data(user_id=self.user_id,
                                                  nalog_ru_receipt_data=receipt_data)

        async with self.transactions_repository.transaction():
            # Create transaction by receipt
            amount = receipt_data.data["operation"]["sum"]
            transaction_date = receipt_data.data["ticket"]["document"]["receipt"]["dateTime"]

            transaction: CreateTransactionModel = \
                CreateTransactionModel(event_id=receipt_qr.event_id,
                                       type=TransactionType.INCOME,
                                       category_id=1,  # TODO Выбрать какую категорию брать для чеков
                                       amount=amount/100,
                                       transaction_date=datetime.utcfromtimestamp(transaction_date).isoformat())

            await self.transactions_repository.create_transaction(user_id=self.user_id,
                                                                  transaction=transaction)

        return receipt
