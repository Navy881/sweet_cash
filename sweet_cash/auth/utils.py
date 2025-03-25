import jwt
import time
from datetime import datetime, timedelta, timezone

from sweet_cash.settings import Settings


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, Settings.SECRET_KEY, algorithms=[Settings.ALGORITHM])
        return decoded_token if decoded_token["exp"] >= time.time() else None
    except:
        return {}
    

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, Settings.SECRET_KEY, algorithm=Settings.ALGORITHM)
    return encoded_jwt
