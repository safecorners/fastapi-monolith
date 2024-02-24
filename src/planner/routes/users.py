from typing import Dict

from fastapi import APIRouter, HTTPException, status

from planner.schemas.users import User as UserSchema
from planner.schemas.users import UserSignIn as UserSignInSchema

user_router = APIRouter(
    tags=["User"],
)

users = {}


@user_router.post("/signup")
async def sign_new_user(data: UserSchema) -> Dict[str, str]:
    if data.email in users:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with suppled username exists",
        )
    users[data.email] = data
    return {"message": "User successfully registerd!"}


@user_router.post("/signin")
async def sign_user_in(user: UserSignInSchema) -> Dict[str, str]:
    if user.email not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist"
        )
    if users[user.email].password != user.password:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials passed"
        )
    return {"message": "User signed in successfully"}
