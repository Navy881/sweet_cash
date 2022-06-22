
import logging
from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse

from sweet_cash.dependencies.users_dependecies import (
    register_user_dependency,
    login_user_dependency,
    get_token_dependency,
    confirm_registration_dependency,
    send_confirmation_code_dependency
)
from sweet_cash.services.users.register_user import RegisterUser
from sweet_cash.services.users.login_user import LoginUser
from sweet_cash.services.users.get_access_token import GerAccessToken
from sweet_cash.services.users.confirm_registration import ConfirmRegistration
from sweet_cash.services.users.send_confirmation_code import SendConfirmationCode
from sweet_cash.types.users_types import (
    CreateUserModel,
    RegisterUserModel,
    RefreshTokenModel,
    LoginModel,
    TokenModel,
    GetAccessTokenModel
)

logger = logging.getLogger(name="users")

auth_api_router = APIRouter()


@auth_api_router.post("/auth/register", response_model=CreateUserModel, tags=["Auth"])
async def register_user(
    body: RegisterUserModel, register_user_: RegisterUser = Depends(dependency=register_user_dependency)
) -> CreateUserModel:
    return await register_user_(body)


@auth_api_router.post("/auth/login", response_model=RefreshTokenModel, tags=["Auth"])
async def login_user(
    body: LoginModel, login_user_: LoginUser = Depends(dependency=login_user_dependency)
) -> RefreshTokenModel:
    return await login_user_(body)


@auth_api_router.post("/auth/token", response_model=TokenModel, tags=["Auth"])
async def get_token(
    body: GetAccessTokenModel, get_token_: GerAccessToken = Depends(dependency=get_token_dependency)
) -> TokenModel:
    return await get_token_(body)


@auth_api_router.get("/auth/confirm", response_class=HTMLResponse, tags=["Auth"])
async def confirm_registration(
        email: str,
        code: str,
        confirm_registration_: ConfirmRegistration = Depends(dependency=confirm_registration_dependency)
) -> HTMLResponse:
    return await confirm_registration_(email=email, confirmation_code=code)


@auth_api_router.get("/auth/code", tags=["Auth"])
async def send_confirmation_code(
        email: str,
        send_confirmation_code_: SendConfirmationCode = Depends(dependency=send_confirmation_code_dependency)
) -> str:
    return await send_confirmation_code_(email)
