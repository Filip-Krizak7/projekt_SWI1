from apify_client import ApifyClient

# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_kY3re4QxTgH4Apsz0xyJVtrYiYmlEB0ahVcm")

# Prepare the actor input
run_input = {
    "search": "New York",
    "maxPages": 2,
    "sortBy": "distance_from_search",
    "currency": "USD",
    "language": "en-us",
    "minMaxPrice": "100-150",
    "proxyConfig": { "useApifyProxy": True },
    "extendOutputFunction": "($) => { return {} }",
}

# Run the actor and wait for it to finish
run = client.actor("dtrungtin/booking-scraper").call(run_input=run_input)

# Fetch and print actor results from the run's dataset (if there are any)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)