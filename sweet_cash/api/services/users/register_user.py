
import logging

from api.services.base_service import BaseService
from api.repositories.users_repository import UserRepository
from api.types.users_types import UserModel, RegisterUserModel
from api.errors import APIConflict

logger = logging.getLogger(name="users")


class RegisterUser(BaseService):
    def __init__(self, users_repository: UserRepository) -> None:
        self.users_repository = users_repository

    async def __call__(self, user: RegisterUserModel) -> UserModel:
        async with self.users_repository.transaction():
            if await self.users_repository.check_exist_by_email(email=user.email):
                raise APIConflict
            return await self.users_repository.create_user(user)


# import logging
#
# from api.api import check_email_format, check_password_format, check_phone_format
# from api.models.users import UserModel
# from api.services.email_sending.send_email import SendEmail
# import api.errors as error
#
# logger = logging.getLogger(name="auth")
#
#
# class RegisterUser(object):
#
#     def __call__(self, email: str, name: str, phone: str, password: str, send_email=SendEmail()):
#         if not check_email_format(email):
#             raise error.APIParamError('Invalid email format')
#
#         if not check_phone_format(phone):
#             raise error.APIParamError('Invalid phone format')
#
#         if not check_password_format(password):
#             raise error.APIParamError('Invalid password format')
#
#         user = UserModel.get_user(email)
#
#         if user is not None:
#             logger.info(f'User tried to register with an already registered email {email}')
#             raise error.APIConflict('Email already registered')
#
#         user = UserModel(name=name,
#                          email=email,
#                          phone=phone,
#                          password=password)
#         user.create()
#
#         logger.info(f'Created new user {user.id}')
#
#         logger.info(f'User {user.id} registered with email {email}')
#
#         send_email(email=email)
#
#         return "Ok"
