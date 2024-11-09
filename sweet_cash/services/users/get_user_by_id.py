import logging

from typing import Union

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.users_repository import UsersRepository

from sweet_cash.types.users_types import UserModel


logger = logging.getLogger(name="users")


class GetUserById(BaseService):
    def __init__(self,
                 user_id: int,
                 users_repository: UsersRepository) -> None:
        self.user_id = user_id
        self.users_repository = users_repository

    async def __call__(self, user_id: int) -> Union[UserModel, None]:
        async with self.users_repository.transaction():
            return await self.users_repository.get_by_id(user_id)
