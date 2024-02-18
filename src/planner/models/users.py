from typing import List, Optional

from beanie import Document, Link
from pydantic import BaseModel, EmailStr

from planner.models.events import Event


class User(Document):
    email: EmailStr
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

    class Settings:
        name = "users"


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


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
