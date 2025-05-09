import os
import jwt
from typing import Annotated
from src.entities import User
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..exception import UserNotFound, UserCreationException
from fastapi import (
    HTTPException, 
    status, 
    Form
)
from .model import (
    UserRegister, 
    UserResponse, 
    UserLogin, 
    Token
)
from .utils import (
    create_access_token, 
    get_password_hash, 
    verify_password
)



ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

def register_user(user: UserRegister, db: Session):
    db_user = db.query(User).filter(User.email == user.email)
    if db_user.first():
        raise UserCreationException()
    new_user = User(
        email=user.email,
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        password_hash=get_password_hash(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def login_user(user_login: Annotated[UserLogin, Form()], db: Session) -> Token:
    user = db.query(User).filter(User.email == user_login.email).first()
    if not user:
        raise UserNotFound()
    if not verify_password(user_login.password, user.password_hash):
        raise UserNotFound()
    access_token_expires = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )
    return Token(
        access_token=access_token, token_type="bearer"
    )


def read_user_me(current_user):
    print("-------Hello World inside read user me----------")
    return current_user