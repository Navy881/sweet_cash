from fastapi import Request

from sweet_cash.repositories.users_repository import UsersRepository
from sweet_cash.services.users.register_user import RegisterUser
from sweet_cash.services.users.get_access_token import GerAccessToken
from sweet_cash.repositories.tokens_repository import TokenRepository
from sweet_cash.services.users.login_user import LoginUser
from sweet_cash.services.users.get_current_user import GetCurrentUser
from sweet_cash.services.users.confirm_registration import ConfirmRegistration
from sweet_cash.services.users.send_confirmation_code import SendConfirmationCode
from sweet_cash.services.users.verify_token import VerifyToken


async def users_repository_dependency(request: Request) -> UsersRepository:
    engine = request.app.state.db
    return UsersRepository(engine)


async def token_repository_dependency(request: Request) -> TokenRepository:
    engine = request.app.state.db
    return TokenRepository(engine)


async def register_user_dependency(request: Request) -> RegisterUser:
    return RegisterUser(
        users_repository = await users_repository_dependency(request)
    )


async def login_user_dependency(request: Request) -> LoginUser:
    return LoginUser(
        tokens_repository = await token_repository_dependency(request),
        users_repository = await users_repository_dependency(request)
    )


async def get_token_dependency(request: Request) -> GerAccessToken:
    return GerAccessToken(
        tokens_repository = await token_repository_dependency(request)
    )


async def confirm_registration_dependency(request: Request) -> ConfirmRegistration:
    return ConfirmRegistration(
        users_repository = await users_repository_dependency(request)
    )


async def send_confirmation_code_dependency(request: Request) -> SendConfirmationCode:
    return SendConfirmationCode(
        users_repository = await users_repository_dependency(request)
    )


async def get_current_user_dependency(request: Request) -> GetCurrentUser:
    return GetCurrentUser(
        tokens_repository = await token_repository_dependency(request),
        users_repository = await users_repository_dependency(request)
    )


async def verify_token_dependency(request: Request) -> VerifyToken:
    return VerifyToken(
        tokens_repository = await token_repository_dependency(request)
    )