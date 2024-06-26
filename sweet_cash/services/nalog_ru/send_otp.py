import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.integrations.nalog_ru_api import NalogRuApi
from sweet_cash.types.users_types import UserModel
from sweet_cash.errors import APIError


logger = logging.getLogger(name="nalog_ru")


class SendOtp(BaseService):
    def __init__(self,
                 user_id: int,
                 user_repository: UsersRepository,
                 nalog_ru_api: NalogRuApi) -> None:
        self.user_id = user_id
        self.user_repository = user_repository
        self.nalog_ru_api = nalog_ru_api

    async def __call__(self) -> None:
        async with self.user_repository.transaction():
            user: UserModel = await self.user_repository.get_by_id(self.user_id)

        if user.phone is None:
            raise APIError(f'User {self.user_id} does not have a phone number')

        await self.nalog_ru_api.send_otp_sms(user.phone)
