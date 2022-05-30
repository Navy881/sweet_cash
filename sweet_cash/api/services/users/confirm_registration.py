import logging
import jwt
import time
from fastapi.responses import HTMLResponse

from api.services.base_service import BaseService
from api.repositories.users_repository import UsersRepository
from api.types.users_types import UserModel
from settings import Settings

logger = logging.getLogger(name="users")


class ConfirmRegistration(BaseService):
    def __init__(self, users_repository: UsersRepository) -> None:
        self.users_repository = users_repository

    async def __call__(self, email: str, confirmation_code: str) -> HTMLResponse:
        async with self.users_repository.transaction():
            user: UserModel = await self.users_repository.get_by_email(email=email, confirmed=False)

            try:
                payload = self.decode_jwt(token=confirmation_code)
            except:
                payload = None

            if not payload:
                return HTMLResponse(open('sweet_cash/templates/fail_confirmation.html', 'r').read())

            await self.users_repository.confirm_user(user.id)

            return HTMLResponse(open('sweet_cash/templates/success_confirmation.html', 'r').read())

    @staticmethod
    def decode_jwt(token: str) -> dict:
        try:
            decoded_token = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
            return decoded_token if decoded_token["exp"] >= time.time() else None
        except:
            return {}


# import logging
# from flask_jwt_extended import decode_token
#
# from api.models.users import UserModel
# import api.errors as error
#
# logger = logging.getLogger(name="auth")
#
#
# class ConfirmUser(object):
#
#     def __call__(self, email: str, confirmation_code: str):
#
#         user = UserModel.get_user(email=email)
#
#         if user is None:
#             logger.warning(f'User with email {email} is trying to confirm registration')
#             raise error.APIValueNotFound(f'User with email {email} not found')
#
#         # try:
#         #     decode_token(encoded_token=confirmation_code)
#         # except Exception as e:
#         #     return open('templates/fail_confirmation.html', 'r').read()
#
#         user.update(confirmed=True)
#
#         logger.info(f'User {user.id} confirmed')
#
#         return open('templates/success_confirmation.html', 'r').read()
