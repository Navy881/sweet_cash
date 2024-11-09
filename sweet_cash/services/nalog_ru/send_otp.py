import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.users.get_user_by_id import GetUserById

from sweet_cash.integrations.nalog_ru_api import NalogRuApi

from sweet_cash.types.users_types import UserModel

from sweet_cash.errors import APIError


logger = logging.getLogger(name="nalog_ru")


class SendOtp(BaseService):
    def __init__(self,
                 user_id: int,
                 get_user_by_id: GetUserById,
                 nalog_ru_api: NalogRuApi) -> None:
        self.user_id = user_id
        self.get_user_by_id = get_user_by_id
        self.nalog_ru_api = nalog_ru_api

    async def __call__(self) -> None:
        user: UserModel = await self.get_user_by_id(self.user_id)
        if user.phone is None:
            raise APIError(f'User {self.user_id} does not have a phone number')

        await self.nalog_ru_api.send_otp_sms(user.phone)
