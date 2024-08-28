
import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.services.email.send_confirm_email import SendConfirmRegistrationEmail
from sweet_cash.types.users_types import RegisterUserResponseModel, RegisterUserModel
from sweet_cash.errors import APIConflict


logger = logging.getLogger(name="auth")


class RegisterUser(BaseService):
    def __init__(self, users_repository: UsersRepository, send_email: SendConfirmRegistrationEmail) -> None:
        self.users_repository = users_repository
        self.send_email = send_email

    async def __call__(self, user: RegisterUserModel) -> RegisterUserResponseModel:
        user_email: str = user.email

        async with self.users_repository.transaction():
            if await self.users_repository.check_exist_by_email(email=user_email):
                raise APIConflict(f'User with email "{user_email}" already exist')

            user: RegisterUserResponseModel = await self.users_repository.create_user(user)

            # Send email for confirm registration
            await self.send_email(email=user_email)

            return user
