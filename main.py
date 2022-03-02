from copy import copy
from datetime import datetime, timedelta
from msilib import Table
import select
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from jose import JWT
from passlib.context import CryptContext
from sqlalchemy import table
from sqlmodel import Field, Session, SQLModel, create_engine, select, insert
import uvicorn

import schemas

tags_metadata = [
    {
        "name": "Booking reservations",
        "description": "Api used to book your hotel reservations.",
    }
]

app = FastAPI(
    title="Booking service",
    description="something special",
    version="1.0.0",
)

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)): #prepsat protoze disable je ted string
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = schemas.UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

@app.get("/hello")
def hello():
    hello = "Hello world!"
    return hello

sqlite_file_name = "databaze1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True,)

def create_heroes():  # 
    hero_1 = schemas.users(username="filipk", full_name="Filip Křižák", email="sadasdsavdbds@asdsd.com", hashed_pass="fakehashedsecret", disabled="False")  # 

    with Session(engine) as session:  # 
        session.add(hero_1)  # 
        session.commit()

@app.get("/show_users")
def select_heroes():
    with Session(engine) as session:  # 
        statement = select(schemas.users)  # 
        results = session.exec(statement)  # 
        for hero in results:  # 
            print(hero)
#def select_heroes():
 #   with Session(engine) as session:
  #      heroes = session.exec(select(schemas.users)).all()
   #     return heroes

@app.post("/new_user")
def create_new_user():
    create_heroes()

if __name__ == "__main__":
    #print(fake_users_db)
    select_heroes()
    #uvicorn.run(app, host="127.0.0.1", port=8000)