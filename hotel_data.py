from apify_client import ApifyClient
from datetime import datetime, timedelta
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

    client = ApifyClient("apify_api_kY3re4QxTgH4Apsz0xyJVtrYiYmlEB0ahVcm")
    run = client.actor("dtrungtin/booking-scraper").call(run_input=run_input)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        hotels.append(item)

    return(hotels)

def create_reservation(url: str, name: str, address: str, price: int, checkIn: str, checkOut: str, room: str, persons: int):
    reservation = schemas.reservations
    with Session(engine) as session:  
        session.add(reservation)  
        session.commit()
