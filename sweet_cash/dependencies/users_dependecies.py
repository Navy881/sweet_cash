from fastapi import Request

from sweet_cash.repositories.tokens_repository import TokenRepository

from sweet_cash.services.users.register_user import RegisterUser
from sweet_cash.services.users.get_access_token import GetAccessToken
from sweet_cash.services.users.login_user import LoginUser
from sweet_cash.services.users.get_current_user import GetCurrentUser
from sweet_cash.services.users.confirm_registration import ConfirmRegistration
from sweet_cash.services.users.send_confirmation_code import SendConfirmationCode
from sweet_cash.services.users.verify_token import VerifyToken
from sweet_cash.services.email.send_confirm_email import SendConfirmRegistrationEmail
from sweet_cash.services.email.send_password_change_email import SendPasswordChangeEmail
from sweet_cash.services.users.password_recovery import PasswordRecovery
from sweet_cash.services.users.get_password_change_from import GetPasswordChangeForm
from sweet_cash.services.users.change_password import ChangePassword
from sweet_cash.services.users.get_users_by_ids import GetUsersByIds

from sweet_cash.dependencies.sc_users_api_dependencies import sc_users_api_dependency


async def token_repository_dependency(request: Request) -> TokenRepository:
    engine = request.app.state.db
    return TokenRepository(engine)


async def send_confirm_email_dependency(request: Request) -> SendConfirmRegistrationEmail:
    smtp = request.app.state.smtp
    return SendConfirmRegistrationEmail(smtp)


async def send_password_change_email_dependency(request: Request) -> SendPasswordChangeEmail:
    smtp = request.app.state.smtp
    return SendPasswordChangeEmail(smtp)


async def register_user_dependency(request: Request) -> RegisterUser:
    return RegisterUser(
        send_email = await send_confirm_email_dependency(request),
        sc_users_api = await sc_users_api_dependency(request)
    )


async def login_user_dependency(request: Request) -> LoginUser:
    return LoginUser(
        tokens_repository = await token_repository_dependency(request),
        sc_users_api = await sc_users_api_dependency(request)
    )


async def get_token_dependency(request: Request) -> GetAccessToken:
    return GetAccessToken(
        tokens_repository = await token_repository_dependency(request)
    )


async def confirm_registration_dependency(request: Request) -> ConfirmRegistration:
    return ConfirmRegistration(
        sc_users_api = await sc_users_api_dependency(request)
    )


async def send_confirmation_code_dependency(request: Request) -> SendConfirmationCode:
    return SendConfirmationCode(
        send_email = await send_confirm_email_dependency(request),
        sc_users_api = await sc_users_api_dependency(request)
    )


async def get_current_user_dependency(request: Request) -> GetCurrentUser:
    return GetCurrentUser(
        tokens_repository = await token_repository_dependency(request)
    )


async def verify_token_dependency(request: Request) -> VerifyToken:
    return VerifyToken(
        tokens_repository = await token_repository_dependency(request)
    )

async def password_recovery_dependency(request: Request) -> PasswordRecovery:
    return PasswordRecovery(
        send_email = await send_password_change_email_dependency(request),
        sc_users_api = await sc_users_api_dependency(request)
    )

async def get_password_change_form_dependency(request: Request) -> GetPasswordChangeForm:
    return GetPasswordChangeForm(
        sc_users_api = await sc_users_api_dependency(request)
    )

async def change_password_dependency(request: Request) -> ChangePassword:
    return ChangePassword(
        sc_users_api = await sc_users_api_dependency(request)
    )

async def get_users_by_ids_dependency(request: Request) -> GetUsersByIds:
    return GetUsersByIds(
        user_id=getattr(request, "user_id"),
        sc_users_api = await sc_users_api_dependency(request)
    )