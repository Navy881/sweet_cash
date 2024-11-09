import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.services.email.send_password_change_email import SendPasswordChangeEmail

from sweet_cash.repositories.users_repository import UsersRepository

from sweet_cash.errors import APIConflict


logger = logging.getLogger(name="auth")


class PasswordRecovery(BaseService):
    def __init__(self,
                 users_repository: UsersRepository,
                 send_email: SendPasswordChangeEmail) -> None:
        self.users_repository = users_repository
        self.send_email = send_email

    async def __call__(self, email: str) -> None:
        async with self.users_repository.transaction():
            if not await self.users_repository.check_exist_by_email(email=email):
                raise APIConflict(f'User with email "{email}" is not exist')

            # Send email for change password
            await self.send_email(email=email)

        return None
