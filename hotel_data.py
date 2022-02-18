from apify_client import ApifyClient
import requests

class HotelData:

    client = ApifyClient("apify_api_kY3re4QxTgH4Apsz0xyJVtrYiYmlEB0ahVcm")
    

    # Prepare the actor input --> need to gather this from Reservation API form
    run_input = {
        "search": "Prague",
        "destType": "city",
        "maxPages": 1,
        "sortBy": "distance_from_search",
        "currency": "USD",
        "language": "en-us",
        "minMaxPrice": "100-150",
        "proxyConfig": { "useApifyProxy": True },
        "extendOutputFunction": "($) => { return {} }",
    }

    #req = requests.get(
    #    "api-url",
    #)
    # req = req.json()

    #run_input = {
    #    "search": "Prague",
    #    "destType": "city",
    #    "maxPages": 1,
    #    "sortBy": "distance_from_search",
    #    "currency": "USD",
    #    "language": "en-us",
    #    "minMaxPrice": "100-150",
    #    "proxyConfig": { "useApifyProxy": True },
    #    "extendOutputFunction": "($) => { return {} }",
    #}

    run = client.actor("dtrungtin/booking-scraper").call(run_input=run_input)

    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        print(item)