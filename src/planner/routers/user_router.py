from typing import Dict, List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from planner.containers import Container
from planner.exceptions import (
    DuplicatedError,
    InvalidUsernameOrPasswordError,
    NotFoundError,
)
from planner.models import User
from planner.schemas.token import Token as TokenResponse
from planner.schemas.user import User as UserResponse
from planner.schemas.user import UserSignUp as UserSignUpRequest
from planner.services import UserService

user_router = APIRouter(tags=["User"])

@inject
def sign_up(payload: UserSignUpRequest, user_service: UserService = Depends(Provide[Container.user_service]),) -> Dict[str, str]:
    try:
        user_service.sign_up(payload.email, payload.password)
    except DuplicatedError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with supplied username exists"
        )

    return {"message": "User created successfully."}


@user_router.post("/signin", response_model=TokenResponse)
@inject
def sign_in(payload: OAuth2PasswordRequestForm = Depends(), user_service: UserService = Depends(Provide[Container.user_service])) -> TokenResponse:
    try :
        return user_service.sign_in(payload.username, payload.password)
    
    except InvalidUsernameOrPasswordError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )


@user_router.get("/users", response_model=List[UserResponse])
@inject
def get_list(
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> List[User]:
    return user_service.get_users()


@user_router.get("/users/{user_id}", response_model=UserResponse)
@inject
def get_by_id(
    user_id: int,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        return user_service.get_user_by_id(user_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@user_router.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
@inject
def add(
    user_service: UserService = Depends(
        Provide[Container.user_service],
    ),
) -> User:
    return user_service.create_user()


@user_router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def remove(
    user_id: int,
    user_service: UserService = Depends(Provide[Container.user_service]),
) -> Response:
    try:
        user_service.delete_user_by_id(user_id)
    except NotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
