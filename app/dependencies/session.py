from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.database import get_db   # or wherever your get_db is

SessionDep = Annotated[Session, Depends(get_db)]