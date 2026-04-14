from app.models.user import UserBase
from sqlmodel import SQLModel
from pydantic import EmailStr
from typing import Optional


class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None


class UserResponse(SQLModel):
    id: int
    username: str
    email: EmailStr
    role: str


class SignupRequest(SQLModel):
    username: str
    email: EmailStr
    password: str
