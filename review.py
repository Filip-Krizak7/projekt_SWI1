from sqlalchemy import create_engine, and_
from sqlmodel import Session, create_engine, select
from sqlalchemy.orm import Session
from sqlmodel import delete
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Depends
from apify_client import ApifyClient
import schemas, main

sqlite_file_name = "databaze1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True,)

def write_review(user: schemas.User, hotel: str, text: str, rating: int):

    if rating > 5:
        rating = 5
    elif rating < 0:
        rating = 0

    with Session(engine) as session:
        # Check if the user has a reservation for the hotel
        existing_reservation = session.execute(
            select(schemas.reservations).where(
                and_(
                    schemas.reservations.username == user.username,
                    schemas.reservations.name == hotel
                )
            )
        ).first()
        if not existing_reservation:
            return "You cannot review a hotel you haven't booked"

        # Check if the user has already left a review for the hotel
        existing_review = session.execute(
            select(schemas.reviews).where(
                and_(
                    schemas.reviews.username == user.username,
                    schemas.reviews.hotel == hotel
                )
            )
        ).first()
        if existing_review:
            return "You have already reviewed this hotel"

        # Create the new review and add it to the database
        review = schemas.reviews(username=user.username, hotel=hotel, text=text, rating=rating)
        session.add(review)
        session.commit()

        return review


def get_reviews():
    with Session(engine) as session:
        # get a list of hotels that have at least one review
        hotels = session.query(schemas.reviews.hotel).distinct().all()

        # create a list to hold the dictionaries representing each hotel and its reviews
        hotel_reviews = []

        # iterate through the list of hotels
        for hotel in hotels:
            # query the reviews for the current hotel
            reviews = session.query(schemas.reviews).filter_by(hotel=hotel[0]).all()

            address = session.query(schemas.reservations.address).filter_by(name=hotel[0]).first()[0]

            # create a dictionary to hold the hotel details and associated reviews
            hotel_dict = {
                "hotel_name": hotel[0],
                "address": address,
                "reviews": []
            }

            # iterate through the reviews and add them to the dictionary
            for review in reviews:
                hotel_dict["reviews"].append({
                    "username": review.username,
                    "text": review.text,
                    "rating": review.rating,
                    "id": review.id
                })

            # add the dictionary to the list of hotel reviews
            hotel_reviews.append(hotel_dict)

        return hotel_reviews




def delete_review(user: schemas.User,id: int):
    with Session(engine) as session:
        statement = delete(schemas.reviews).where(schemas.reviews.id == id and schemas.reviews.username.__eq__(user.username))
        session.execute(statement)
        session.commit()


def update_review(id: int, user: schemas.User, hotel: Optional[str] = None, text: Optional[str] = None, rating: Optional[int] = None):
    with Session(engine) as session:
        review = session.get(schemas.reviews, id)
        if review is None:
            return None
        if review.username != user.username:
            raise HTTPException(status_code=403, detail="You are not allowed to update this review")
        if rating is not None:
            if rating > 5:
                rating = 5
            elif rating < 0:
                rating = 0
            review.rating = rating
        if hotel is not None:
            review.hotel = hotel
        if text is not None:
            review.text = text
        session.add(review)
        session.commit()
        return review


