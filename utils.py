from cachetools import TTLCache
from datetime import timedelta
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel
from services import get_info_credito
import json
import jwt
import os

load_dotenv()

SECRET_KEY = os.getenv('jwt_secret_key')
USERNAME = os.getenv('jwt_username')
PASSWORD = os.getenv('jwt_password')
CACHE_TIME = int(os.getenv('cache_time'))


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


def process_credit_info(id):
    """
    It takes a credit id, gets the credit info from the database, and returns the credit info as a JSON
    object

    :param id: The id of the credit
    :return: A JSON object
    """
    info_credito = get_info_credito(id)[0]
    return json.loads(json.dumps(info_credito))


cache = TTLCache(maxsize=100, ttl=timedelta(days=CACHE_TIME).total_seconds())
