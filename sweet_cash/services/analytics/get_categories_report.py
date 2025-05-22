import logging
from typing import List, Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser
from sweet_cash.services.transactions.get_transactions_by_event_and_type import GetTransactionsByEventAndType
from sweet_cash.services.transaction_categories.get_transaction_categories_by_ids import GetTransactionCategoriesByIds

from sweet_cash.types.analytics_types import (
    CategoriesReportRequestModel,
    CategoriesReportModel,
    PeriodModel,
    CategoryAmountModel
)
from sweet_cash.types.transaction_categories_types import TransactionCategoryResponseModel, TransactionCategoryModel
from sweet_cash.types.events_types import EventParticipantRole

from sweet_cash.errors import APIConflict


logger = logging.getLogger(name="accounts")


class GetCategoriesReport(BaseService):
    def __init__(self,
                 user_id: int,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 get_transactions_by_event_and_type: GetTransactionsByEventAndType,
                 get_transaction_categories_by_ids: GetTransactionCategoriesByIds) -> None:
        self.user_id = user_id
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.get_transactions_by_event_and_type = get_transactions_by_event_and_type
        self.get_transaction_categories_by_ids = get_transaction_categories_by_ids

    async def __call__(self, request: CategoriesReportRequestModel) -> CategoriesReportModel:
        # Checking that user in event
        users_roles: List[EventParticipantRole] = \
            await self.get_event_participants_roles_for_user(event_id=request.event_id, user_id=self.user_id)

        if len(users_roles) == 0:
            raise APIConflict(f'User {self.user_id} cannot get report for event {request.event_id}')

        result = CategoriesReportModel(
            event_id=request.event_id,
            period=PeriodModel(
                start=request.start,
                end=request.end
            ),
            transaction_type=request.transaction_type,
            categories=[]
        )

        # Get transactions
        transactions = await self.get_transactions_by_event_and_type(
            event_id=request.event_id,
            start=request.start,
            end=request.end,
            transaction_type=request.transaction_type
        )

        # Calculate categories amounts
        categories_amounts = {}
        for transaction in transactions:
            if transaction.category_id in categories_amounts.keys():
                categories_amounts[transaction.category_id] += transaction.amount
            else:
                categories_amounts[transaction.category_id] = 0

        # Get categories into
        category_models: Dict[int, TransactionCategoryModel] = await self.get_transaction_categories_by_ids(list(categories_amounts.keys()))

        for category_id, amount in categories_amounts.items():
            category_model = category_models[category_id]
            if category_models[category_id] is None:
                category_model = TransactionCategoryResponseModel(id=category_id)

            result.categories.append(
                CategoryAmountModel(
                    category=category_model,
                    amount=amount
                )
            )

        return result
