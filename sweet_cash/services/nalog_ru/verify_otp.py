import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.repositories.nalog_ru_sessions_repository import NalogRuSessionsRepository
from sweet_cash.integrations.nalog_ru_api import NalogRuApi
from sweet_cash.types.users_types import UserModel
from sweet_cash.types.nalog_ru_types import NalogRuSessionModel, OtpModel
from sweet_cash.errors import APIError


logger = logging.getLogger(name="nalog_ru")


class VerifyOtp(BaseService):
    def __init__(self,
                 user_id: int,
                 user_repository: UsersRepository,
                 nalog_ru_sessions_repository: NalogRuSessionsRepository,
                 nalog_ru_api: NalogRuApi) -> None:
        self.user_id = user_id
        self.nalog_ru_sessions_repository = nalog_ru_sessions_repository
        self.user_repository = user_repository
        self.nalog_ru_api = nalog_ru_api

    async def __call__(self, otp: OtpModel) -> None:
        async with self.user_repository.transaction():
            user: UserModel = await self.user_repository.get_by_id(self.user_id)

        if user.phone is None:
            raise APIError(f'User {self.user_id} does not have a phone number')

        nalog_ru_session: NalogRuSessionModel = await self.nalog_ru_api.verify_otp(phone=user.phone, otp=otp.otp)

        async with self.nalog_ru_sessions_repository.transaction():
            if await self.nalog_ru_sessions_repository.check_exist_by_user_id(self.user_id):
                await self.nalog_ru_sessions_repository.update_nalog_ru_session(user_id=self.user_id,
                                                                                nalog_ru_session=nalog_ru_session)
            else:
                await self.nalog_ru_sessions_repository.create_nalog_ru_session(user_id=self.user_id,
                                                                                nalog_ru_session=nalog_ru_session)

        return None
