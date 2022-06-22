import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.services.email_sending.send_email import SendEmail


logger = logging.getLogger(name="auth")


class SendConfirmationCode(BaseService):
    def __init__(self, users_repository: UsersRepository,  send_email=SendEmail()) -> None:
        self.users_repository = users_repository
        self.send_email = send_email

    async def __call__(self, email: str) -> str:
        async with self.users_repository.transaction():
            await self.users_repository.get_by_email(email=email, confirmed=False)

            # Send email for confirm registration
            self.send_email(email=email)

            return "Ok"
