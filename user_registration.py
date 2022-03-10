from sqlalchemy import create_engine
from sqlmodel import Session, create_engine, select

import schemas

sqlite_file_name = "databaze1.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True,)

def select_users():
    with Session(engine) as session:   
        statement = select(schemas.users)   
        results = session.exec(statement)   
        users_db = {}
        for user in results:   
            users_db.update({user.username: {        
            "username": user.username,
            "full_name": user.full_name,
            "email": user.full_name,
            "hashed_password": user.hashed_pass,
            "disabled": user.disabled}})
        return users_db

def create_users(username, full_name, email, hashed_pass, disabled: schemas.Disabled):  # zmenit disabled na enum string True/False
    user = schemas.users(username=username, full_name=full_name, email=email, hashed_pass=hashed_pass, disabled=disabled.value)
    with Session(engine) as session:  
        session.add(user)  
        session.commit()