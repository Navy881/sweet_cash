
import logging
from fastapi import APIRouter, Depends, Response

from sweet_cash.dependencies.nalog_ru_dependencies import (
    send_otp_dependency,
    verify_otp_dependency
)
from sweet_cash.services.nalog_ru.send_otp import SendOtp
from sweet_cash.services.nalog_ru.verify_otp import VerifyOtp
from sweet_cash.types.nalog_ru_types import OtpModel
from sweet_cash.auth.auth_bearer import JWTBearer


logger = logging.getLogger(name="nalog_ru_auth")

nalog_ru_api_router = APIRouter()


@nalog_ru_api_router.post("/nalog/otp/send",
                          dependencies=[Depends(JWTBearer())],
                          status_code=204,
                          response_class=Response,
                          tags=["Nalog RU"])
async def send_otp(
        send_otp_: SendOtp = Depends(dependency=send_otp_dependency)
) -> None:
    return await send_otp_()


@nalog_ru_api_router.post("/nalog/otp/verify",
                          dependencies=[Depends(JWTBearer())],
                          response_class=Response,
                          tags=["Nalog RU"])
async def verify_otp(
        body: OtpModel,
        verify_otp_: VerifyOtp = Depends(dependency=verify_otp_dependency)
) -> None:
    return await verify_otp_(body)
