from __future__ import annotations
import enum
from datetime import datetime
from typing import Any, Optional
from pydantic import BaseModel, validator, root_validator

from sweet_cash.types.users_types import UserResponseModel
from sweet_cash.types.events_types import EventModel, EventModelTiny
from sweet_cash.types.accounts_types import AccountModel, AccountResponseTinyModel


class TransactionType(enum.Enum):
    INCOME = "Income"
    EXPENSE = "Expense"
    TRANSFER = "Transfer"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_


class TransactionModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    number: int
    user_id: int
    event_id: int
    event: Optional[EventModel]
    type: TransactionType
    category_id: int
    amount: float
    transfer_fee: Optional[float]
    transaction_date: datetime
    description: Optional[str]
    receipt_id: Optional[int]
    user: Optional[UserResponseModel]
    source_account_id: Optional[int]
    source_account: Optional[AccountModel]
    target_account_id: Optional[int]
    target_account: Optional[AccountModel]


class TransactionResponseModel(BaseModel):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    number: int
    event_id: int
    event: Optional[EventModelTiny]
    type: TransactionType
    category_id: int
    amount: float
    transfer_fee: Optional[float]
    transaction_date: datetime
    description: Optional[str]
    receipt_id: Optional[int]
    user: Optional[UserResponseModel]
    source_account: Optional[AccountResponseTinyModel]
    target_account: Optional[AccountResponseTinyModel]



class CreateTransactionModel(BaseModel):
    event_id: int
    type: TransactionType
    category_id: int
    amount: float
    transfer_fee: Optional[float]
    transaction_date: datetime
    description: Optional[str]
    receipt_id: Optional[int]
    source_account_id: Optional[int]
    target_account_id: Optional[int]

    @validator("amount")
    def validate_amount(cls, v: float, **kwargs: Any) -> float:
        if v < 0:
            raise ValueError("'amount' must be positive")
        return v

    @validator("transfer_fee")
    def validate_transfer_fee(cls, v: float, **kwargs: Any) -> float:
        if v < 0:
            raise ValueError("'transfer_fee' must be positive")
        return v

    @root_validator(pre=True)
    def validate_accounts(cls, values):
        transaction_type = values.get("type")
        source_account_id = values.get("source_account_id")
        target_account_id = values.get("target_account_id")

        if transaction_type == TransactionType.EXPENSE.value and not source_account_id:
            raise ValueError("Field 'source_account_id' should not be empty for expense transaction")
        elif transaction_type == TransactionType.INCOME.value and not target_account_id:
            raise ValueError("Field 'target_account_id' should not be empty for income transaction")
        elif transaction_type == TransactionType.TRANSFER.value and (not source_account_id or not target_account_id):
            raise ValueError("Fields 'source_account_id' and 'target_account_id' "
                             "should not be empty for transfer transaction")

        return values

    @root_validator(pre=True)
    def validate_amount_and_transfer_fee(cls, values):
        amount = values.get("amount")
        transfer_fee = values.get("transfer_fee")

        if transfer_fee and transfer_fee > amount:
            raise ValueError("'transfer_fee' must be less than or equal to 'amount'")

        return values


class UpdateTransactionModel(BaseModel):
    type: TransactionType
    category_id: int
    amount: float
    transfer_fee: Optional[float]
    transaction_date: datetime
    description: Optional[str]
    receipt_id: Optional[int]
    source_account_id: Optional[int]
    target_account_id: Optional[int]

    @validator("amount")
    def validate_amount(cls, v: float, **kwargs: Any) -> float:
        if v < 0:
            raise ValueError("'amount' must be positive")
        return v

    @validator("transfer_fee")
    def validate_transfer_fee(cls, v: float, **kwargs: Any) -> float:
        if v < 0:
            raise ValueError("'transfer_fee' must be positive")
        return v

    @root_validator(pre=True)
    def validate_debtor_or_creditor(cls, values):
        transaction_type = values.get("type")
        source_account_id = values.get("source_account_id")
        target_account_id = values.get("target_account_id")

        if transaction_type == TransactionType.EXPENSE.value and not source_account_id:
            raise ValueError("Field 'source_account_id' should not be empty for expense transaction")
        elif transaction_type == TransactionType.INCOME.value and not target_account_id:
            raise ValueError("Field 'target_account_id' should not be empty for income transaction")
        elif transaction_type == TransactionType.TRANSFER.value and (not source_account_id or not target_account_id):
            raise ValueError("Fields 'source_account_id' and 'target_account_id' "
                             "should not be empty for transfer transaction")

        return values

    @root_validator(pre=True)
    def validate_amount_and_transfer_fee(cls, values):
        amount = values.get("amount")
        transfer_fee = values.get("transfer_fee")

        if transfer_fee and transfer_fee > amount:
            raise ValueError("'transfer_fee' must be less than or equal to 'amount'")

        return values
