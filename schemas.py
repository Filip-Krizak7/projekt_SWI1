from datetime import timedelta
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field
from sqlmodel import Field, SQLModel

class users(SQLModel, table=True):
    username: str = Field(primary_key=True)
    full_name: Optional[str] = None
    email: Optional[str] = None
    hashed_pass: str
    disabled: Optional[str] = None

class reservations(SQLModel, table=True):
    username: str
    name: str
    address: str
    price: int
    checkIn: str
    checkOut: str
    room: str
    persons: int
    id: int = Field(primary_key=True)


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