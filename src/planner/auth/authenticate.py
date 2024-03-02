from typing import cast

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from planner.auth import JWTHandler
from planner.containers import Container

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin")


@inject
def authenticate(token: str = Depends(oauth2_scheme), jwt_handler: JWTHandler = Depends(Provide[Container.jwt_handler]),) -> str:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Sign in for access",
        )
    
    decoded_token = jwt_handler.verify_access_token(token)
    return cast(str, decoded_token["username"])