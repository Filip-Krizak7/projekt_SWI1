import fastapi

tags_metadata = [
    {
        "name": "Booking reservations",
        "description": "Api used to book your hotel reservations.",
    }
]

app = fastapi.FastAPI(
    title="Booking service",
    description="something special",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

#@app.get(
#    "/booking",
#    response_model=List
#)