
from fastapi import APIRouter, Depends

from api.dependencies.users_dependecies import (
    register_user_dependency,
    login_user_dependency,
    get_token_dependency
)
from api.services.users.register_user import RegisterUser
from api.services.users.login_user import LoginUser
from api.services.users.get_access_token import GerAccessToken
from api.types.users_types import (
    UserModel,
    RegisterUserModel,
    RefreshTokenModel,
    LoginModel,
    TokenModel,
    GetAccessTokenModel
)

import logging


logger = logging.getLogger(name="events")

auth_api_router = APIRouter()


@auth_api_router.post("/api/v1/auth/register", response_model=UserModel)
async def register_user(
    body: RegisterUserModel, register_user_: RegisterUser = Depends(dependency=register_user_dependency)
) -> UserModel:
    return await register_user_(body)


@auth_api_router.post("/api/v1/auth/login", response_model=RefreshTokenModel)
async def login_user(
    body: LoginModel, login_user_: LoginUser = Depends(dependency=login_user_dependency)
) -> RefreshTokenModel:
    return await login_user_(body)


@auth_api_router.post("/api/v1/auth/token", response_model=TokenModel)
async def login_user(
    body: GetAccessTokenModel, get_token_: GerAccessToken = Depends(dependency=get_token_dependency)
) -> TokenModel:
    return await get_token_(body)


# from flask import Blueprint
# import logging
#
# from api.api import SuccessResponse, jsonbody, features, query_params
# from api.services.users.register_user import RegisterUser
# from api.services.users.login_user import LoginUser
# from api.services.users.get_access_token import GetAccessToken
# from api.services.users.confirm_user import ConfirmUser
# from api.services.email_sending.send_email import SendEmail
#
# logger = logging.getLogger(name="auth")
#
# auth_api = Blueprint('login', __name__)
#
#
# @auth_api.route('/api/v1/auth/register', methods=['POST'])
# @jsonbody(name=features(type=str, required=True),
#           email=features(type=str, required=True),
#           phone=features(type=str, required=True),
#           password=features(type=str, required=True))
# def register(name: str,
#              email: str,
#              phone: str,
#              password: str,
#              register_user=RegisterUser()):
#     return SuccessResponse(register_user(name=name,
#                                          email=email,
#                                          phone=phone,
#                                          password=password))
#
#
# @auth_api.route('/api/v1/auth/login', methods=['POST'])
# @jsonbody(email=features(type=str, required=True),
#           password=features(type=str, required=True))
# def login(email: str,
#           password: str,
#           login_user=LoginUser()):
#     return SuccessResponse(login_user(email=email,
#                                       password=password,
#                                       login_method='email'))
#
#
# @auth_api.route('/api/v1/auth/token', methods=['POST'])
# @jsonbody(refresh_token=features(type=str, required=True))
# def get_token(refresh_token: str,
#               get_access_token=GetAccessToken()):
#     return SuccessResponse(get_access_token(refresh_token=refresh_token))
#
#
# @auth_api.route('/api/v1/auth/confirm', methods=['GET'])
# @query_params(email=features(type=str, required=True),
#               code=features(type=str, required=True))
# def confirm_registration(email: str,
#                          code: str,
#                          confirm_user=ConfirmUser()):
#     return confirm_user(email=email, confirmation_code=code), 200  # return html
#
#
# @auth_api.route('/api/v1/auth/code', methods=['GET'])
# @query_params(email=features(type=str, required=True))
# def send_confirmation_code(email: str,
#                            send_email=SendEmail()):
#     return SuccessResponse(send_email(email=email))
