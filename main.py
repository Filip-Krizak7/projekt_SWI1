from fastapi import Depends, FastAPI, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import uvicorn

import schemas, user_registration, hotel_data, send_mail

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


@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = user_registration.select_users().get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    user = schemas.UserInDB(**user_dict)
    password = form_data.password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user

@app.get("/show_users")
def show_users():
    return user_registration.select_users()

@app.post("/new_user/{username}_{full_name}_{email}_{hashed_pass}_{disabled}")
def create_user(username: str, full_name: str, email: str, hashed_pass: str, disabled: schemas.Disabled):
    user_registration.create_users(username, full_name, email, hashed_pass, disabled)
    send_mail.new_user_mail(username, email, full_name)

@app.get("/hotel/{city}_{maxPage}_{sortBy}_{minPrice}_{maxPrice}_{rooms}_{adults}_{children}")
def search_hotel(city: str, maxPages: int, sortBy: schemas.SortBy, minPrice: int, maxPrice: int, rooms: int, adults: int, 
children: int):
    return hotel_data.get_hotels(city, maxPages, sortBy, minPrice, maxPrice, rooms, adults, children)

@app.post("/reservation/create/{name}_{address}_{price}_{room}_{persons}")
def create_reservation(name: str, address: str, price: int, checkIn: str, checkOut: str, room: str, persons: int, current_user: schemas.User = Depends(get_current_active_user)):
    hotel_data.create_reservation(current_user.username, name, address, price, checkIn, checkOut, room, persons)
    send_mail.reservation_mail(current_user, name, address, price, room, persons, checkIn, checkOut)

@app.get("/reservation/show/")
def user_reservations(current_user: schemas.User = Depends(get_current_active_user)):
    return hotel_data.reservations_from_user(current_user)

@app.delete("/reservation/cancel/{id}")
def cancel_registration(id: int, current_user: schemas.User = Depends(get_current_active_user)):
    return hotel_data.cancel_reservation(current_user, id)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)