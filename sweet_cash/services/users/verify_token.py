
import logging
from datetime import datetime

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.tokens_repository import TokenRepository
from sweet_cash.types.users_types import VerifyTokenModel, TokenInfoModel, TokenModel
from sweet_cash.errors import APIValueNotFound


logger = logging.getLogger(name="auth")


class VerifyToken(BaseService):
    def __init__(self, tokens_repository: TokenRepository) -> None:
        self.tokens_repository = tokens_repository

    async def __call__(self, input: VerifyTokenModel) -> TokenInfoModel:
        async with self.tokens_repository.transaction():
            token_data: TokenModel = await self.tokens_repository.get_user_by_token(input.token)
            
            if token_data.expire_at < datetime.now():
                raise APIValueNotFound("Valid token not found")

            return TokenInfoModel(**token_data.dict())
