from sqlalchemy import create_engine
from sqlmodel import Session, create_engine, select

import schemas, main

sqlite_file_name = "databaze1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True,)

def write_review(username: str, hotel: str, text: str, rating: int):
    if rating > 10:
        rating = 10
    elif rating < 0:
        rating = 0

    review = schemas.reviews(username=username, hotel=hotel, text=text, rating=rating)
    with Session(engine) as session:  
        session.add(review)  
        session.commit()

def get_reviews():
    with Session(engine) as session:
        statement = select(schemas.reviews)
        results = session.exec(statement)
        reviews_db = []
        for review in results:
            reviews_db.append({
                "_id": review.id,
                "username": review.username,
                "hotel": review.hotel,
                "text": review.text,
                "rating": review.rating})

        if not reviews_db:  
            return "User didn't wrine any reviews!"

        return reviews_db