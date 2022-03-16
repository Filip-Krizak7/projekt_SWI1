from datetime import date, datetime, timedelta
from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field
from sqlmodel import Field, Session, SQLModel

class users(SQLModel, table=True):
    username: str = Field(primary_key=True)
    full_name: Optional[str] = None
    email: Optional[str] = None
    hashed_pass: str
    disabled: Optional[str] = None

class reservations(SQLModel, table=True):
    url: str
    name: str
    address: str
    price: int
    checkIn: str
    checkOut: str
    room: str
    persons: int
    id: int = Field(primary_key=True)

class Token(BaseModel):
    access_token: str
    token_type: str
    token_expires_in: timedelta

class TokenData(BaseModel):
    username: Optional[str] = None

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(User):
    hashed_password: str

class SortBy(Enum):
    PRICE = "price"
    CLASS = "class"
    DISTANCE = "distance_from_search"
    REVIEW = "bayesian_review_score"
    
class Disabled(Enum):
    FALSE = "False"
    TRUE = "True"