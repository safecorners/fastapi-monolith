import time
from datetime import datetime
from typing import Any, Dict, Final

from fastapi import HTTPException, status
from jose import JWTError, jwt


class JWTHandler:

    SECRET_KEY : Final[str]

    def __init__(self, secret_key: str) -> None:
        self.SECRET_KEY = secret_key

    def create_access_token(self, username: str) -> str:
        payload = {"username": username , "expires": time.time() + 3600}

        access_token = jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")

        return access_token

    def verify_access_token(self, access_token: str) -> Dict[str, Any]:
        try:
            data = jwt.decode(access_token, self.SECRET_KEY, algorithms=["HS256"])
            expire = data.get("expires")

            if expire is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No access token supplied",
                )

            if datetime.utcnow() > datetime.utcfromtimestamp(expire):
                raise HTTPException(
                    status.HTTP_403_FORBIDDEN,
                    detail="Token expired",
                )
            
            return data

        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token",
            )