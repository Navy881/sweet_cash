from fastapi import Request

from sweet_cash.repositories.limits_repository import LimitsRepository

from sweet_cash.services.limit.enrich_limits import EnrichLimits
from sweet_cash.services.limit.create_limit import CreateLimit
from sweet_cash.services.limit.update_limit import UpdateLimit
from sweet_cash.services.limit.delete_limit import DeleteLimit
from sweet_cash.services.limit.get_events_limits import GetEventsLimits

from sweet_cash.dependencies.users_dependecies import get_users_by_ids_dependency
from sweet_cash.dependencies.transaction_categories_dependencies import (
    get_transaction_categories_by_ids_dependency,
    get_transaction_category_by_id_dependency
)
from sweet_cash.dependencies.events_dependencies import get_event_participants_roles_for_user_dependency
from sweet_cash.dependencies.transactions_dependencies import get_transactions_by_event_and_type_dependency


async def limits_repository_dependency(request: Request) -> LimitsRepository:
    engine = request.app.state.db
    return LimitsRepository(engine)


async def enrich_limits_dependency(request: Request) -> EnrichLimits:
    return EnrichLimits(
        user_id=getattr(request, "user_id"),
        get_users_by_ids = await get_users_by_ids_dependency(request),
        get_transaction_categories_by_ids = await get_transaction_categories_by_ids_dependency(request)
    )

async def create_limit_dependency(request: Request) -> CreateLimit:
    return CreateLimit(
        user_id=getattr(request, "user_id"),
        limits_repository = await limits_repository_dependency(request),
        enrich_limits = await enrich_limits_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        get_transaction_category_by_id = await get_transaction_category_by_id_dependency(request)
    )

async def update_limit_dependency(request: Request) -> UpdateLimit:
    return UpdateLimit(
        user_id=getattr(request, "user_id"),
        limits_repository = await limits_repository_dependency(request),
        enrich_limits = await enrich_limits_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        get_transaction_category_by_id = await get_transaction_category_by_id_dependency(request)
    )


async def delete_limit_dependency(request: Request) -> DeleteLimit:
    return DeleteLimit(
        user_id=getattr(request, "user_id"),
        limits_repository = await limits_repository_dependency(request),
        enrich_limits = await enrich_limits_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request)
    )


async def get_events_limits_dependency(request: Request) -> GetEventsLimits:
    return GetEventsLimits(
        user_id=getattr(request, "user_id"),
        limits_repository = await limits_repository_dependency(request),
        enrich_limits = await enrich_limits_dependency(request),
        get_event_participants_roles_for_user = await get_event_participants_roles_for_user_dependency(request),
        get_transaction_category_by_id = await get_transaction_category_by_id_dependency(request),
        get_transactions_by_event_and_type = await get_transactions_by_event_and_type_dependency(request)
    )