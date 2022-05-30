import time

import jwt
from fastapi import Request, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from api.dependencies.users_dependecies import get_current_user_dependency
from api.services.users.get_current_user import GetCurrentUser
from api.types.users_types import TokenModel

from settings import Settings


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}


class JWTBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request,
                       get_current_user_: GetCurrentUser = Depends(dependency=get_current_user_dependency)):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme")

            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token")

            current_token: TokenModel = await get_current_user_(token=credentials.credentials)
            setattr(request, "user_id", current_token.user_id)

            return credentials.credentials

        else:
            raise HTTPException(status_code=403, detail="Invalid authentication code")

    @staticmethod
    def verify_jwt(jwtoken: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None

        if payload:
            is_token_valid = True

        return is_token_valid
