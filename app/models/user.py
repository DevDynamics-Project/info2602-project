from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING
from pydantic import EmailStr

if TYPE_CHECKING:
    from .routine import Routine


class UserBase(SQLModel):
    username: str = Field(index=True, unique=True)
    email: EmailStr = Field(index=True, unique=True)
    password: str
    role: str = ""


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    routines: list["Routine"] = Relationship(back_populates="user")
