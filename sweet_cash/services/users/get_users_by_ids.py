import logging

from typing import List, Dict

from sweet_cash.services.base_service import BaseService

from sweet_cash.repositories.users_repository import UsersRepository

from sweet_cash.types.users_types import UserModel


logger = logging.getLogger(name="users")


class GetUsersByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 users_repository: UsersRepository) -> None:
        self.user_id = user_id
        self.users_repository = users_repository

    async def __call__(self, user_ids: List[int]) -> Dict[int, UserModel]:
        async with self.users_repository.transaction():
            users: List[UserModel] = await self.users_repository.get_by_ids(user_ids)
            users_map: Dict = {}

            for user in users:
                users_map[user.id] = user

            return users_map