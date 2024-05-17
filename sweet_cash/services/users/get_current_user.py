import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.tokens_repository import TokenRepository
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.types.users_types import TokenModel
from sweet_cash.errors import APIAuthError


logger = logging.getLogger(name="auth")


class GetCurrentUser(BaseService):
    def __init__(self, tokens_repository: TokenRepository, users_repository: UsersRepository) -> None:
        self.tokens_repository = tokens_repository
        self.users_repository = users_repository

    async def __call__(self, token: str = None) -> TokenModel:
        async with self.tokens_repository.transaction():
            token_info: TokenModel = await self.tokens_repository.get_user_by_token(token=token)
        
            if token_info is None:
                raise APIAuthError()

            return token_info
