from fastapi import Request

from sweet_cash.repositories.debts_repository import DebtsRepository

from sweet_cash.services.debts.create_debt import CreateDebt
from sweet_cash.services.debts.get_debts_by_user import GetDebtsByUser
from sweet_cash.services.debts.get_debts_by_ids import GetDebtsByIds
from sweet_cash.services.debts.update_debt import UpdateDebt
from sweet_cash.services.debts.enrich_debts import EnrichDebts

from sweet_cash.dependencies.users_dependecies import get_users_by_ids_dependency


async def debts_repository_dependency(request: Request) -> DebtsRepository:
    engine = request.app.state.db
    return DebtsRepository(engine)

async def enrich_debts_dependency(request: Request) -> EnrichDebts:
    return EnrichDebts(
        user_id = getattr(request, "user_id"),
        get_users_by_ids = await get_users_by_ids_dependency(request)
    )

async def create_debt_dependency(request: Request) -> CreateDebt:
    return CreateDebt(
        user_id = getattr(request, "user_id"),
        enrich_debts = await enrich_debts_dependency(request),
        debts_repository = await debts_repository_dependency(request)
    )


async def update_debt_dependency(request: Request) -> UpdateDebt:
    return UpdateDebt(
        user_id = getattr(request, "user_id"),
        enrich_debts = await enrich_debts_dependency(request),
        debts_repository = await debts_repository_dependency(request)
    )


async def get_debts_by_user_dependency(request: Request) -> GetDebtsByUser:
    return GetDebtsByUser(
        user_id = getattr(request, "user_id"),
        enrich_debts = await enrich_debts_dependency(request),
        debts_repository = await debts_repository_dependency(request)
    )

async def get_debts_by_ids_dependency(request: Request) -> GetDebtsByIds:
    return GetDebtsByIds(
        user_id = getattr(request, "user_id"),
        enrich_debts = await enrich_debts_dependency(request),
        debts_repository = await debts_repository_dependency(request)
    )
