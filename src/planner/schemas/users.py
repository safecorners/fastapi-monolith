from typing import List, Optional

from pydantic import BaseModel, EmailStr

from planner.schemas.events import Event


class User(BaseModel):
    email: EmailStr
    username: str
    password: str
    events: Optional[List[Event]] = None

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "username": "username",
                "events": [],
            }
        }


class UserSignIn(BaseModel):
    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "fastapi@packt.com",
                "password": "strong-password",
                "events": [],
            }
        }
