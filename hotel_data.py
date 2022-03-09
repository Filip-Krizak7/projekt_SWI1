from apify_client import ApifyClient
from datetime import datetime, timedelta
import requests

def get_hotels(city: str, maxPages: int, sortBy: str, minPrice: int, maxPrice: int, rooms: int, adults: int,children: int):

    minMaxPrice = f"{minPrice}-{maxPrice}"
        
    run_input = {
    "search": city,
    "destType": "city",
    "maxPages": maxPages,
    "sortBy": sortBy,
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
        return item

#get_hotels("Prague", 1, "price", 100, 150, 1, 1, 0)