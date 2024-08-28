
import logging

from sweet_cash.services.base_service import BaseService
from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.types.users_types import ChangePasswordRequestModel, UserModel, RegisterUserModel
from sweet_cash.auth.utils import decode_jwt
from sweet_cash.errors import APIConflict, APIAuthError


logger = logging.getLogger(name="auth")


class ChangePassword(BaseService):
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    async def __call__(self, request: ChangePasswordRequestModel) -> None:
        user_email: str = request.email

        async with self.users_repository.transaction():
            try:
                payload = decode_jwt(token=request.code)
            except:
                payload = None

            if payload is None:
                raise APIAuthError(f'Invalid token')

            user: UserModel = await self.users_repository.get_by_email(email=user_email)
            if not user.confirmed:
                raise APIConflict(f'Registration for {credits.email} not confirmed')

            new_user_data = RegisterUserModel(
                name=user.name,
                email=user.email,
                phone=user.phone,
                password=request.new_password
            )

            await self.users_repository.update_user(new_user_data)
