import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.email.send_confirm_email import SendConfirmRegistrationEmail

from sweet_cash.repositories.users_repository import UsersRepository

from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="auth")


class SendConfirmationCode(BaseService):
    def __init__(self,
                 users_repository: UsersRepository,
                 send_email: SendConfirmRegistrationEmail) -> None:
        self.users_repository = users_repository
        self.send_email = send_email

    async def __call__(self, email: str):
        async with self.users_repository.transaction():
            if not await self.users_repository.check_exist_by_email(email=email):
                raise APIValueNotFound(f'User with email "{email}" not found')

            # Send email for confirm registration
            await self.send_email(email=email)

        return None
