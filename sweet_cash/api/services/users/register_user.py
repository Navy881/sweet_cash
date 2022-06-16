
import logging

from sweet_cash.api.services.base_service import BaseService
from sweet_cash.api.repositories.users_repository import UsersRepository
from sweet_cash.api.types.users_types import CreateUserModel, RegisterUserModel
from sweet_cash.api.errors import APIConflict
from sweet_cash.api.services.email_sending.send_email import SendEmail


logger = logging.getLogger(name="auth")


class RegisterUser(BaseService):
    def __init__(self, users_repository: UsersRepository, send_email=SendEmail()) -> None:
        self.users_repository = users_repository
        self.send_email = send_email

    async def __call__(self, user: RegisterUserModel) -> CreateUserModel:
        user_email: str = user.email

        async with self.users_repository.transaction():
            if await self.users_repository.check_exist_by_email(email=user_email):
                raise APIConflict(f'User with email "{user_email}" already exist')

            user: CreateUserModel = await self.users_repository.create_user(user)

            # Send email for confirm registration
            self.send_email(email=user_email)

            return user
