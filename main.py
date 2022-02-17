from apify_client import ApifyClient
import pymysql

connection = pymysql.connect(host="localhost",user="root",passwd="",database="test")
cursor = connection.cursor()

client = ApifyClient("apify_api_kY3re4QxTgH4Apsz0xyJVtrYiYmlEB0ahVcm")

# Prepare the actor input
run_input = {
    "search": "Prague",
    "destType": "city",
    "maxPages": 2,
    "sortBy": "distance_from_search",
    "currency": "USD",
    "language": "en-us",
    "minMaxPrice": "100-150",
    "proxyConfig": { "useApifyProxy": True },
    "extendOutputFunction": "($) => { return {} }",
}

run = client.actor("dtrungtin/booking-scraper").call(run_input=run_input)

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)

insert_reservation = "INSERT INTO reservations(customer_ID, check_in_date, check_out_date, hotel, price) VALUES('1', '2022-04-06', '2022-04-09', 'Park In', '139');"
cursor.execute(insert_reservation)

connection.commit()
connection.close()