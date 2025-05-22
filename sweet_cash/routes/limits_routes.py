
import logging
from fastapi import APIRouter, Depends
from typing import List

from sweet_cash.dependencies.limits_dependencies import (
    create_limit_dependency,
    update_limit_dependency,
    delete_limit_dependency,
    get_events_limits_dependency
)
from sweet_cash.services.limit.create_limit import CreateLimit
from sweet_cash.services.limit.update_limit import UpdateLimit
from sweet_cash.services.limit.delete_limit import DeleteLimit
from sweet_cash.services.limit.get_events_limits import GetEventsLimits
from sweet_cash.types.limits_types import (
    LimitModel,
    LimitResponseModel,
    CreateLimitModel,
    UpdateLimitModel
)
from sweet_cash.auth.auth_bearer import JWTBearer

logger = logging.getLogger(name="limits")

limits_api_router = APIRouter()


@limits_api_router.post("/limits",
                        response_model=LimitResponseModel,
                        dependencies=[Depends(JWTBearer())],
                        tags=["Limits"])
async def create_limit(
        body: CreateLimitModel, create_limit_: CreateLimit = Depends(dependency=create_limit_dependency)
) -> LimitModel:
    return await create_limit_(body)


@limits_api_router.put("/limits/{limit_id}",
                       response_model=LimitResponseModel,
                       dependencies=[Depends(JWTBearer())],
                       tags=["Limits"])
async def update_limit(
        limit_id: int,
        body: UpdateLimitModel,
        update_limit_: UpdateLimit = Depends(dependency=update_limit_dependency)
) -> LimitModel:
    return await update_limit_(limit_id, body)


@limits_api_router.delete("/limits/{limit_id}",
                       response_model=LimitResponseModel,
                       dependencies=[Depends(JWTBearer())],
                       tags=["Limits"])
async def delete_limit(
        limit_id: int,
        delete_limit_: DeleteLimit = Depends(dependency=delete_limit_dependency)
) -> LimitModel:
    return await delete_limit_(limit_id)


@limits_api_router.get("/limits",
                                response_model=List[LimitResponseModel],
                                dependencies=[Depends(JWTBearer())],
                                tags=["Limits"])
async def get_events_limits(
        event_id: int,
        limit: int,
        offset: int,
        get_events_limits_: GetEventsLimits = Depends(dependency=get_events_limits_dependency)
) -> List[LimitModel]:
    return await get_events_limits_(event_id, limit, offset)