from datetime import datetime, timedelta
from pickle import FALSE, TRUE
from typing import Optional
from fastapi import Body, Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

import schemas, user_registration, hotel_data, send_mail, review

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

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)

def fake_decode_token(token):
    user = get_user(user_registration.select_users(), token)
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
    if not current_user.disabled.__eq__("True"):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.get("/")
async def welcome():
    return "Welcome!"


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = user_registration.select_users().get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = schemas.UserInDB(**user_dict)
    password = form_data.password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    del user_dict["hashed_password"]
    return {"access_token": user.username, "token_type": "bearer", "userdata": user_dict}


@app.get("/users/me")
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

@app.get("/show_users")
def show_users():
    return user_registration.select_users()

@app.post("/new_user/{username}/{full_name}/{email}/{hashed_pass}/{disabled}")
def create_user(username: str, full_name: str, email: str, hashed_pass: str, disabled: schemas.Disabled):
    print(disabled)
    user_registration.create_users(username, full_name, email, hashed_pass, disabled)
    send_mail.new_user_mail(username, email, full_name)

#@app.post("/new_user/")
#def create_user(user_data = Body(...)):
    #user_data = jsonable_encoder(user_data)
    #if user_data["disabled"]:
        #user_data["disabled"] = schemas.Disabled(schemas.Disabled.TRUE)
    #else:
        #user_data["disabled"] = schemas.Disabled(schemas.Disabled.FALSE)
    #user_registration.create_users(user_data["username"], user_data["full_name"], user_data["email"], user_data["hashed_pass"], user_data["disabled"])
    #send_mail.new_user_mail(user_data["username"], user_data["email"], user_data["full_name"])
# to return error on frontend, set error in json object as {detail:"Error here..."}

@app.get("/hotel/{city}/{maxPage}/{sortBy}/{minPrice}/{maxPrice}/{rooms}/{adults}/{children}") #{checkIn}/{checkOut}/
def search_hotel(city: str, maxPages: int, sortBy: schemas.SortBy, minPrice: int, maxPrice: int, rooms: int, adults: int, children: int, start_datetime: str, end_datetime: str):
    return hotel_data.get_hotels(city, maxPages, sortBy, minPrice, maxPrice, start_datetime, end_datetime, rooms, adults, children)

@app.post("/reservation/create/{name}/{address}/{price}/{room}/{persons}")
def create_reservation(name: str, address: str, price: int, checkIn: str, checkOut: str, room: str, persons: int, current_user: schemas.User = Depends(get_current_active_user)):
    hotel_data.create_reservation(current_user.username, name, address, price, checkIn, checkOut, room, persons)
    send_mail.reservation_mail(current_user, name, address, price, room, persons, checkIn, checkOut)

@app.get("/reservation/show/")
def user_reservations(current_user: schemas.User = Depends(get_current_active_user)):
    return hotel_data.reservations_from_user(current_user)

@app.get("/review/show/")
def show_reviews():
    return review.get_reviews()

@app.delete("/reservation/cancel/{id}")
def cancel_registration(id: int, current_user: schemas.User = Depends(get_current_active_user)):
    return hotel_data.cancel_reservation(current_user, id)

if __name__ == "__main__": 
    uvicorn.run(app, host="127.0.0.1", port=8000)