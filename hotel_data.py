from apify_client import ApifyClient
from datetime import datetime, timedelta
from fastapi import HTTPException
import schemas

from sqlalchemy import create_engine
from sqlmodel import Session, create_engine, select

import schemas

sqlite_file_name = "databaze1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
format = "%Y-%m-%d"

engine = create_engine(sqlite_url, echo=True,)


def get_hotels(city: str, maxPages: int, sortBy: schemas.SortBy, minPrice: int, maxPrice: int, checkIn: str, checkOut: str, rooms: int, adults: int, children: int):

    try:
        datetime.strptime(checkIn, format).date()
        datetime.strptime(checkOut, format).date()
    except ValueError:
        print("This is the incorrect date string format. It should be YYYY-MM-DD")
        return "This is the incorrect date string format. It should be YYYY-MM-DD"

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
        "proxyConfig": {"useApifyProxy": True},
        "extendOutputFunction": "($) => { return {} }",
        "simple": True,
        "checkIn": datetime.strptime(checkIn, format).date(),
        "checkOut": datetime.strptime(checkOut, format).date(),
        "rooms": rooms,
        "adults": adults,
        "children": children,
    }

    client = ApifyClient("apify_api_bxMic6fhnSfVxiBBje61kkVFFOknXw0beIvu")
    run = client.actor("dtrungtin/booking-scraper").call(run_input=run_input)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        hotels.append(item)

    return(hotels)


def create_reservation(username: str, name: str, address: str, price: int, checkIn: str, checkOut: str, room: str, persons: int):

    try:
        datetime.strptime(checkIn, format).date()
        datetime.strptime(checkOut, format).date()
    except ValueError:
        print("This is the incorrect date string format. It should be YYYY-MM-DD")
        raise ValueError

    reservation = schemas.reservations(username=username, name=name, address=address,
                                       price=price, checkIn=checkIn, checkOut=checkOut, room=room, persons=persons)
    statement = select(schemas.reservations)

    with Session(engine) as session:
        results = session.exec(statement)
        for item in results:
            if item == reservation:
                raise HTTPException(
                    status_code=400, detail="Reservation already exists!")
        session.add(reservation)
        session.commit()


def cancel_reservation(user: schemas.User, id: int):
    with Session(engine) as session:
        statement = select(schemas.reservations).where(
            schemas.reservations.id == id and schemas.reservations.username.__eq__(user.username))  #
        results = session.exec(statement)
        deleted_reservation = results.one()

        session.delete(deleted_reservation)
        session.commit()

        print("Deleted reservation: ", deleted_reservation)

        if deleted_reservation is None:  #
            return "There's no your reservation with this ID"


def reservations_from_user(user: schemas.User):
    with Session(engine) as session:
        statement = select(schemas.reservations).where(
            schemas.reservations.username.__eq__(user.username))
        results = session.exec(statement)
        reservation_db = []
        for reservation in results:
            reservation_db.append({
                "_id": reservation.id,
                "name": reservation.name,
                "address": reservation.address,
                "price": reservation.price,
                "checkIn": reservation.checkIn,
                "checkOut": reservation.checkOut,
                "roomType": reservation.room,
                "persons": reservation.persons})

        return reservation_db


# def reservations_from_user(user: schemas.User):
#     with Session(engine) as session:
#         statement = select(schemas.reservations).where(schemas.reservations.username.__eq__(user.username))
#         results = session.exec(statement)
#         reservation_db = {}
#         for reservation in results:
#             reservation_db.update({ reservation.id: {
#             "Name of the Hotel": reservation.name,
#             "Address": reservation.address,
#             "Price": reservation.price,
#             "Check In Date": reservation.checkIn,
#             "Check Out Date": reservation.checkOut,
#             "Room Type": reservation.room,
#             "Number of Persons": reservation.persons}})

#         return reservation_db
