import logging
from typing import List
from unicodedata import category

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.limit.enrich_limits import EnrichLimits
from sweet_cash.services.events.get_event_participants_roles_for_user import GetEventParticipantsRolesForUser
from sweet_cash.services.transaction_categories.get_transaction_category_by_id import GetTransactionCategoryBiId

from sweet_cash.repositories.limits_repository import LimitsRepository

from sweet_cash.types.limits_types import LimitModel, CreateLimitModel
from sweet_cash.types.events_types import EventParticipantRole
from sweet_cash.errors import APIConflict


logger = logging.getLogger(name="limits")


class CreateLimit(BaseService):
    def __init__(self,
                 user_id: int,
                 enrich_limits: EnrichLimits,
                 get_event_participants_roles_for_user: GetEventParticipantsRolesForUser,
                 get_transaction_category_by_id: GetTransactionCategoryBiId,
                 limits_repository: LimitsRepository) -> None:
        self.user_id = user_id
        self.enrich_limits = enrich_limits
        self.get_event_participants_roles_for_user = get_event_participants_roles_for_user
        self.get_transaction_category_by_id = get_transaction_category_by_id
        self.limits_repository = limits_repository

    async def __call__(self, limit: CreateLimitModel) -> LimitModel:
        # Checking that user in event
        users_roles: List[EventParticipantRole] = \
            await self.get_event_participants_roles_for_user(event_id=limit.event_id, user_id=self.user_id)

        if EventParticipantRole.MANAGER not in users_roles:
            raise APIConflict(f'User {self.user_id} cannot create limit for event {limit.event_id}')

        # Checking exist transaction category
        if limit.category_id:
            category_model = await self.get_transaction_category_by_id(limit.category_id)

            if category_model.type.value != limit.type.value:
                raise APIConflict(f'Category type ({category_model.type.value}) '
                                  f'must not differ from the limit type ({limit.type.value})')

        async with self.limits_repository.transaction():
            limit_model = await self.limits_repository.create_limit(user_id=self.user_id, limit=limit)

        await self.enrich_limits([limit_model])
        return limit_model
