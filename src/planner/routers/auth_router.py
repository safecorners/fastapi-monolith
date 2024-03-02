from typing import Dict

from fastapi import APIRouter, Depends

from planner.auth.authenticate import authenticate

auth_router = APIRouter(tags=["Authentication Test"])


@auth_router.get("/protected")
def get_resource(username: str = Depends(authenticate)) ->  Dict[str, str]:
    return {
         "username": username
    }