from sqlalchemy import create_engine
from sqlmodel import Session, create_engine, select

import schemas, main

sqlite_file_name = "databaze1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True,)

def write_review(user: schemas.User, hotel: str, text: str, rating: int):
    if rating > 10:
        rating = 10
    elif rating < 0:
        rating = 0

    review = schemas.reviews(username=user.username, hotel=hotel, text=text, rating=rating)
    with Session(engine) as session:  
        session.add(review)  
        session.commit()

def get_reviews():
    with Session(engine) as session:
        reviews = session.exec(select(schemas.reviews)).all()

        return reviews