
import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.tokens_repository import TokenRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.types.users_types import RefreshTokenModel, LoginModel


logger = logging.getLogger(name="auth")


class LoginUser(BaseService):
    def __init__(self, tokens_repository: TokenRepository, users_repository: UsersRepository) -> None:
        self.tokens_repository = tokens_repository
        self.users_repository = users_repository

    async def __call__(self, credits: LoginModel) -> RefreshTokenModel:
        async with self.users_repository.transaction():
            user = await self.users_repository.get_by_email(email=credits.email)
            self.users_repository.check_password(password=user.password, given_password=credits.password)

        async with self.tokens_repository.transaction():
            data = {"user_id": user.id, "login_method": "email"}

            if await self.tokens_repository.check_exist_token_by_user(user_id=user.id):
                token = await self.tokens_repository.get_token_by_user(user_id=user.id)
                return await self.tokens_repository.update_access_token(refresh_token=token.refresh_token, item=data)

            return await self.tokens_repository.create_access_token(item=data)
