from copy import copy
from datetime import datetime, timedelta
from msilib import Table
import select
from typing import List, Optional

from fastapi import Depends, FastAPI, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
#from jose import JWT
from sqlalchemy import table
from sqlmodel import Field, Session, SQLModel, create_engine, select, insert
import uvicorn
from imp import reload

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

def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)


def fake_decode_token(token):
    user = get_user(select_heroes(), token)
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


async def get_current_active_user(current_user: schemas.User = Depends(get_current_user)): 
    if current_user.disabled.__eq__("True"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = select_heroes().get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = schemas.UserInDB(**user_dict)
    password = form_data.password
    if not password == user.hashed_password:
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

@app.get("/show_users")
def select_heroes():
    with Session(engine) as session:  # 
        statement = select(schemas.users)  # 
        results = session.exec(statement)  # 
        users_db = {}
        for hero in results:  # 
            users_db.update({hero.username: {        
            "username": hero.username,
            "full_name": hero.full_name,
            "email": hero.full_name,
            "hashed_password": hero.hashed_pass,
            "disabled": hero.disabled}})
        return users_db

@app.post("/new_user")
def create_heroes(username: str = Form(...), full_name: str = Form(...), email: str = Form(...), hashed_pass: str = Form(...), disabled: str = Form(...)):  # zmenit disabled na enum string True/False
    hero_1 = schemas.users(username=username, full_name=full_name, email=email, hashed_pass=hashed_pass, disabled=disabled)  # 

    with Session(engine) as session:  # 
        session.add(hero_1)  # 
        session.commit()

if __name__ == "__main__":
    #select_heroes()
    #print(fake_users_db)
    uvicorn.run(app, host="127.0.0.1", port=8000) # nastavit reload na True