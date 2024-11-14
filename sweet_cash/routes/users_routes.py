import logging
from fastapi import APIRouter, Depends

from sweet_cash.dependencies.user_profile_dependencies import get_user_profile_dependency

from sweet_cash.services.users.get_user_profile import GetUserProfile

from sweet_cash.types.users_types import UserProfile

from sweet_cash.auth.auth_bearer import JWTBearer


logger = logging.getLogger(name="users")

user_api_router = APIRouter()


@user_api_router.get("/user/profile",
                     response_model=UserProfile,
                     dependencies=[Depends(JWTBearer())],
                     tags=["Users"])
async def get_user_profile(
        get_user_profile_: GetUserProfile = Depends(dependency=get_user_profile_dependency)
) -> UserProfile:
    return await get_user_profile_()