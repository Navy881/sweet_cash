import logging
from typing import List, Dict, Union

from sweet_cash.services.base_service import BaseService

from sweet_cash.integrations.sc_users_api import SCUsersApi

from sweet_cash.types.users_types import UserModel, SCUserApiUserModel

from sweet_cash.errors import BaseError


logger = logging.getLogger(name="users")


class GetUsersByIds(BaseService):
    def __init__(self,
                 user_id: int,
                 sc_users_api: SCUsersApi) -> None:
        self.user_id = user_id
        self.sc_users_api = sc_users_api

    async def __call__(self, user_ids: List[int]) -> Dict[int, UserModel]:
        async with self.sc_users_api.get_stub():
            response: Union[List[SCUserApiUserModel], BaseError] = \
                await self.sc_users_api.get_user_by_ids(user_ids)
            if isinstance(response, BaseError):
                raise response

            users: List[SCUserApiUserModel] = response

        users_map: Dict = {}
        for user in users:
            users_map[user.id] = user

        return users_map
