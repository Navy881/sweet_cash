import logging
from typing import Dict

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_users_by_ids import GetUsersByIds

from sweet_cash.integrations.nalog_ru_api import NalogRuApi

from sweet_cash.types.users_types import UserModel

from sweet_cash.errors import APIError


logger = logging.getLogger(name="nalog_ru")


class SendOtp(BaseService):
    def __init__(self,
                 user_id: int,
                 get_users_by_ids: GetUsersByIds,
                 nalog_ru_api: NalogRuApi) -> None:
        self.user_id = user_id
        self.get_users_by_ids = get_users_by_ids
        self.nalog_ru_api = nalog_ru_api

    async def __call__(self) -> None:
        users: Dict[int, UserModel] = await self.get_users_by_ids([self.user_id])
        if self.user_id in users.keys() and users[self.user_id].phone is None:
            raise APIError(f'User {self.user_id} does not have a phone number')
        await self.nalog_ru_api.send_otp_sms(users[self.user_id].phone)
