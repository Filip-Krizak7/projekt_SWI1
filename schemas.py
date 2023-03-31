from datetime import timedelta
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field
from sqlmodel import Field, Relationship, Session, SQLModel

class users(SQLModel, table=True):
    username: str = Field(primary_key=True)
    full_name: Optional[str] = None
    email: Optional[str] = None
    hashed_pass: str
    disabled: Optional[str] = None

    reservation: List["reservations"] = Relationship(back_populates="users")
    review: List["reviews"] = Relationship(back_populates="users")
    
class reviews(SQLModel, table=True):
    id: int = Field(primary_key=True)

    username: Optional[str] = Field(default=None, foreign_key="users.usernamme")
    usern: Optional[users] = Relationship(back_populates="review")

    hotel: Optional[str] = None
    text: Optional[str] = None
    rating: int

class reservations(SQLModel, table=True):
    username: str = Field(default=None, foreign_key="users.usernamme")
    usern: Optional[users] = Relationship(back_populates="reservation")

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