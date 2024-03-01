from typing import List, Optional

from pydantic import BaseModel, EmailStr

from planner.schemas.events import Event


class User(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    is_active: bool
    
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
