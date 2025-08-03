import logging
from typing import List

from sqlalchemy.util import await_only
from typing_extensions import Optional

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.limit.enrich_limits import EnrichLimits
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser
from sweet_cash.services.transactions.get_transactions_by_event_and_type import GetTransactionsByEventAndType
from sweet_cash.services.transaction_categories.get_sub_transaction_categories import GetSubTransactionCategories

from sweet_cash.repositories.limits_repository import LimitsRepository

from sweet_cash.types.limits_types import LimitModel
from sweet_cash.types.events_types import EventParticipantRole
from sweet_cash.types.transaction_categories_types import TransactionCategoryModel
from sweet_cash.errors import APIConflict, APIParamError


logger = logging.getLogger(name="limits")


class GetEventsLimits(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_limits: EnrichLimits,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 get_transactions_by_event_and_type: GetTransactionsByEventAndType,
                 get_sub_transaction_categories: GetSubTransactionCategories,
                 limits_repository: LimitsRepository) -> None:
        self.user_id = user_id
        self.enrich_limits = enrich_limits
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.get_transactions_by_event_and_type = get_transactions_by_event_and_type
        self.get_sub_transaction_categories = get_sub_transaction_categories
        self.limits_repository = limits_repository

    async def __call__(self, event_id: int, limit: int, offset: int) -> List[LimitModel]:
        if limit > 100:
            raise APIParamError(f'Limit value must be less than or equal to 100')

        # Checking that user in event
        users_roles: List[EventParticipantRole] = \
            await self.get_event_participants_roles_for_user(event_id=event_id, user_id=self.user_id)

        if len(users_roles) == 0:
            raise APIConflict(f'User {self.user_id} cannot get limits for event {event_id}')

        async with self.limits_repository.transaction():
            limit_models = await self.limits_repository.get_limits_page(event_id=event_id, limit=limit, offset=offset)

        await self.enrich_limits(limit_models)

        # Calculating balance
        for limit_model in limit_models:

            # Получение всех подкатегорий для категории лимита
            category_ids = None
            if limit_model.category_id:
                category_ids = [limit_model.category_id]
                sub_categories : List[TransactionCategoryModel] = \
                    await self.get_sub_transaction_categories(limit_model.category_id)
                category_ids += [c.id for c in sub_categories]

            transactions = await self.get_transactions_by_event_and_type(
                event_id=limit_model.event_id,
                start=limit_model.start,
                end=limit_model.end,
                transaction_type=limit_model.type,
                category_ids=category_ids
            )

            for transaction in transactions:
                limit_model.balance += transaction.amount

        return limit_models
