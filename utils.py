from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel
import os
import jwt

load_dotenv()

SECRET_KEY = os.getenv('jwt_secret_key')
USERNAME = os.getenv('jwt_username')
PASSWORD = os.getenv('jwt_password')


class User(BaseModel):
    username: str


auth = HTTPBearer()

async def decode_token(token: str = Depends(auth)):
    """
    It takes a token as a parameter, decodes it, and returns the user.

    :param token: str = Depends(auth)
    :type token: str
    :return: A user object with the username from the payload.
    """
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY,
                             algorithms=["HS256"])
        user = User(username=payload["sub"])
        return user
    except (jwt.exceptions.DecodeError, jwt.exceptions.ExpiredSignatureError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )
