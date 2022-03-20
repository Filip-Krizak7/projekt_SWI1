from apify_client import ApifyClient
from datetime import datetime, timedelta
from fastapi import HTTPException
import schemas

from sqlalchemy import create_engine
from sqlmodel import Session, create_engine, select

import schemas

sqlite_file_name = "projekt_SWI1/databaze1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True,)

def get_hotels(city: str, maxPages: int, sortBy: schemas.SortBy, minPrice: int, maxPrice: int, rooms: int, adults: int,children: int):

    minMaxPrice = f"{minPrice}-{maxPrice}"
    hotels = []
        
    run_input = {
    "search": city,
    "destType": "city",
    "maxPages": maxPages,
    "sortBy": sortBy.value,
    "currency": "USD",
    "language": "en-us",
    "minMaxPrice": minMaxPrice,
    "proxyConfig": { "useApifyProxy": True },
    "extendOutputFunction": "($) => { return {} }",
    "simple": True,
    "checkIn": datetime.date(datetime.now()),
    "checkOut": datetime.date(datetime.now()) + timedelta(days=1),
    "rooms": rooms,
    "adults": adults,
    "children": children,
    } 

    client = ApifyClient("apify_api_5cpM6jZRBKor2v16lqMLjtR6iEdu8C2ke8DQ")
    run = client.actor("dtrungtin/booking-scraper").call(run_input=run_input)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        hotels.append(item)

    return(hotels)

def create_reservation(username: str, name: str, address: str, price: int, checkIn: str, checkOut: str, room: str, persons: int):
    reservation = schemas.reservations(username=username, name=name, address=address, price=price, checkIn=checkIn, checkOut=checkOut, room=room, persons=persons)
    statement = select(schemas.reservations)

    with Session(engine) as session:  
        results = session.exec(statement) 
        for item in results:
            if item == reservation:
                raise HTTPException(status_code=400, detail="Reservation already exists!")
        session.add(reservation)
        session.commit()

def cancel_reservation(user: schemas.User, id: int):
    with Session(engine) as session:
        statement = select(schemas.reservations).where(schemas.reservations.id == id and schemas.reservations.username.__eq__(user.username))  # 
        results = session.exec(statement)  
        deleted_reservation = results.one()  

        session.delete(deleted_reservation) 
        session.commit()

        print("Deleted reservation: ", deleted_reservation)  

        if deleted_reservation is None:  # 
            return "There's no your reservation with this ID"

def reservations_from_user(user: schemas.User):
    with Session(engine) as session:   
        statement = select(schemas.reservations).where(schemas.reservations.username.__eq__(user.username))
        results = session.exec(statement)   
        reservation_db = {}
        for reservation in results:   
            reservation_db.update({ reservation.id: {       
            "Name of the Hotel": reservation.name,
            "Address": reservation.address,
            "Price": reservation.price,
            "Check In Date": reservation.checkIn,
            "Check Out Date": reservation.checkOut,
            "Room Type": reservation.room,
            "Number of Persons": reservation.persons}})

        return reservation_db