import logging
from datetime import datetime
from typing import List

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser
from sweet_cash.services.nalog_ru.get_receipt_by_qr import GetReceiptByQr
from sweet_cash.services.transactions.create_transaction import CreateTransaction, CreateTransactionV2

from sweet_cash.repositories.receipts_repository import ReceiptsRepository

from sweet_cash.types.receipts_types import ReceiptModel, CreateReceiptModel, CreateReceiptModelV2
from sweet_cash.types.nalog_ru_types import NalogRuReceiptModel
from sweet_cash.types.transactions_types import CreateTransactionModel, TransactionType
from sweet_cash.types.events_participants_types import EventParticipantRole

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="receipts")


class CreateReceiptByQr(BaseService):
    def __init__(self,
                 user_id: int,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 get_receipt_by_qr: GetReceiptByQr,
                 create_transaction: CreateTransaction,
                 receipts_repository: ReceiptsRepository) -> None:
        self.user_id = user_id
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.get_receipt_by_qr = get_receipt_by_qr
        self.create_transaction = create_transaction
        self.receipts_repository = receipts_repository


    async def __call__(self, receipt_qr: CreateReceiptModel) -> ReceiptModel:
        user_roles: List[EventParticipantRole] = \
            await self.get_event_participants_roles_for_user(event_id=receipt_qr.event_id, user_id=self.user_id)

        if len(user_roles) == 0:
            raise APIValueNotFound(f'User {self.user_id} not associated with the event {receipt_qr.event_id}')

        # Get receipt data by qr
        receipt_data: NalogRuReceiptModel = await self.get_receipt_by_qr(receipt_qr.qr)

        # Save receipt
        async with self.receipts_repository.transaction():
            receipt: ReceiptModel = await self.receipts_repository. \
                create_receipt_from_nalog_ru_data(user_id=self.user_id, nalog_ru_receipt_data=receipt_data)

        # Create transaction by receipt
        amount = receipt_data.data["operation"]["sum"]
        transaction_date = receipt_data.data["ticket"]["document"]["receipt"]["dateTime"]
        transaction: CreateTransactionModel = \
            CreateTransactionModel(event_id=receipt_qr.event_id,
                                   type=TransactionType.EXPENSE,
                                   category_id=1,  # TODO Выбрать какую категорию брать для чеков
                                   amount=amount / 100,
                                   transaction_date=datetime.utcfromtimestamp(transaction_date).isoformat(),
                                   receipt_id=receipt.id)

        await self.create_transaction(transaction)

        return receipt


class CreateReceiptByQrV2(BaseService):
    def __init__(self,
                 user_id: int,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 get_receipt_by_qr: GetReceiptByQr,
                 create_transaction: CreateTransactionV2,
                 receipts_repository: ReceiptsRepository) -> None:
        self.user_id = user_id
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.get_receipt_by_qr = get_receipt_by_qr
        self.create_transaction = create_transaction
        self.receipts_repository = receipts_repository


    async def __call__(self, receipt_qr: CreateReceiptModelV2) -> ReceiptModel:
        user_roles: List[EventParticipantRole] = \
            await self.get_event_participants_roles_for_user(event_id=receipt_qr.event_id, user_id=self.user_id)

        if len(user_roles) == 0:
            raise APIValueNotFound(f'User {self.user_id} not associated with the event {receipt_qr.event_id}')

        # Get receipt data by qr
        receipt_data: NalogRuReceiptModel = await self.get_receipt_by_qr(receipt_qr.qr)

        # Save receipt
        async with self.receipts_repository.transaction():
            receipt: ReceiptModel = await self.receipts_repository. \
                create_receipt_from_nalog_ru_data(user_id=self.user_id, nalog_ru_receipt_data=receipt_data)

        # Create transaction by receipt
        amount = receipt_data.data["operation"]["sum"]
        transaction_date = receipt_data.data["ticket"]["document"]["receipt"]["dateTime"]
        transaction: CreateTransactionModel = \
            CreateTransactionModel(event_id=receipt_qr.event_id,
                                   type=TransactionType.EXPENSE,
                                   category_id=1,  # TODO Выбрать какую категорию брать для чеков
                                   amount=amount / 100,
                                   transaction_date=datetime.utcfromtimestamp(transaction_date).isoformat(),
                                   source_account_id=receipt_qr.account_id,
                                   receipt_id=receipt.id)

        await self.create_transaction(transaction)

        return receipt