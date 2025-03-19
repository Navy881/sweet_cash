from fastapi import Request

from sweet_cash.services.users.get_user_profile import GetUserProfile

from sweet_cash.dependencies.users_dependecies import users_repository_dependency
from sweet_cash.dependencies.nalog_ru_dependencies import get_nalog_ru_session_dependency
from sweet_cash.dependencies.sc_users_api_dependencies import sc_users_api_dependency

'''
Вынесено в отдельнй файл, чтобы не было circular import
'''

async def get_user_profile_dependency(request: Request) -> GetUserProfile:
    return GetUserProfile(
        user_id=getattr(request, "user_id"),
        get_nalog_ru_session = await get_nalog_ru_session_dependency(request),
        users_repository = await users_repository_dependency(request),
        sc_user_api=await sc_users_api_dependency(request)
    )