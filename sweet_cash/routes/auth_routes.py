
import logging
from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse

from sweet_cash.dependencies.users_dependecies import (
    register_user_dependency,
    login_user_dependency,
    get_token_dependency,
    confirm_registration_dependency,
    send_confirmation_code_dependency,
    verify_token_dependency,
    password_recovery_dependency,
    get_password_change_form_dependency,
    change_password_dependency
)
from sweet_cash.services.users.register_user import RegisterUser
from sweet_cash.services.users.login_user import LoginUser
from sweet_cash.services.users.get_access_token import GerAccessToken
from sweet_cash.services.users.confirm_registration import ConfirmRegistration
from sweet_cash.services.users.send_confirmation_code import SendConfirmationCode
from sweet_cash.services.users.verify_token import VerifyToken
from sweet_cash.services.users.password_recovery import PasswordRecovery
from sweet_cash.services.users.get_password_change_from import GetPasswordChangeForm
from sweet_cash.services.users.change_password import ChangePassword
from sweet_cash.types.users_types import (
    RegisterUserResponseModel,
    RegisterUserModel,
    LoginModel,
    TokenModel,
    GetAccessTokenModel,
    VerifyTokenModel,
    TokenInfoModel,
    LoginResponseModel,
    ChangePasswordRequestModel
)

logger = logging.getLogger(name="users")

auth_api_router = APIRouter()
auth_pages_router = APIRouter()


@auth_api_router.post("/auth/register", response_model=RegisterUserResponseModel, tags=["Auth"])
async def register_user(
    body: RegisterUserModel, register_user_: RegisterUser = Depends(dependency=register_user_dependency)
) -> RegisterUserResponseModel:
    return await register_user_(body)


@auth_api_router.post("/auth/login", response_model=LoginResponseModel, tags=["Auth"])
async def login_user(
    body: LoginModel, login_user_: LoginUser = Depends(dependency=login_user_dependency)
) -> LoginResponseModel:
    return await login_user_(body)


@auth_api_router.post("/auth/token", response_model=TokenModel, tags=["Auth"])
async def get_token(
    body: GetAccessTokenModel, get_token_: GerAccessToken = Depends(dependency=get_token_dependency)
) -> TokenModel:
    return await get_token_(body)


@auth_api_router.get("/auth/code", response_class=JSONResponse, tags=["Auth"])
async def send_confirmation_code(
        email: str,
        send_confirmation_code_: SendConfirmationCode = Depends(dependency=send_confirmation_code_dependency)
) -> JSONResponse:
    await send_confirmation_code_(email)
    return JSONResponse(status_code=200, content={'message': 'Ok'})


@auth_api_router.post("/auth/token/verify", response_model=TokenInfoModel, tags=["Auth"])
async def verify_token(
    body: VerifyTokenModel, verify_token_: VerifyToken = Depends(dependency=verify_token_dependency)
) -> TokenInfoModel:
    return await verify_token_(body)


@auth_api_router.post("/auth/password/recovery", response_class=JSONResponse, tags=["Auth"])
async def password_recovery(
        email: str,
        password_recovery_: PasswordRecovery = Depends(dependency=password_recovery_dependency)
) -> JSONResponse:
    await password_recovery_(email=email)
    return JSONResponse(status_code=200, content={'message': 'Ok'})


@auth_api_router.post("/auth/password/change", response_class=JSONResponse, tags=["Auth"])
async def change_password(
        body: ChangePasswordRequestModel,
        change_password_: ChangePassword = Depends(dependency=change_password_dependency)
) -> JSONResponse:
    await change_password_(body)
    return JSONResponse(status_code=200, content={'message': 'Ok'})


@auth_pages_router.get("/confirm", response_class=HTMLResponse, tags=["HTML pages"])
async def confirm_registration(
        email: str,
        code: str,
        confirm_registration_: ConfirmRegistration = Depends(dependency=confirm_registration_dependency)
) -> HTMLResponse:
    return await confirm_registration_(email=email, confirmation_code=code)


@auth_pages_router.get("/changePassword", response_class=HTMLResponse, tags=["HTML pages"])
async def get_password_change_form(
        request: Request,
        email: str,
        code: str,
        get_password_change_form_: GetPasswordChangeForm = Depends(dependency=get_password_change_form_dependency)
) -> HTMLResponse:
    return await get_password_change_form_(request=request, email=email, confirmation_code=code)