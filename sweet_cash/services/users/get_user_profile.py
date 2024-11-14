import logging
from typing import Union

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.nalog_ru.get_nalog_ru_session import GetNalogRuSession

from sweet_cash.repositories.users_repository import UsersRepository

from sweet_cash.types.users_types import UserProfile

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="users")


class GetUserProfile(BaseService):
    def __init__(self,
                 user_id: int,
                 get_nalog_ru_session: GetNalogRuSession,
                 users_repository: UsersRepository) -> None:
        self.user_id = user_id
        self.get_nalog_ru_session = get_nalog_ru_session
        self.users_repository = users_repository

    async def __call__(self) -> Union[UserProfile, None]:
        async with self.users_repository.transaction():
            user = await self.users_repository.get_by_id(self.user_id)
            if user is None:
                raise APIValueNotFound('User not found')

        profile: UserProfile = UserProfile(**user.dict())

        nalog_ru_session = await self.get_nalog_ru_session(self.user_id)
        if nalog_ru_session:
            profile.registered_in_nalog_ru = True

        return profile
