from typing import Annotated

from fastapi import APIRouter, Depends, Form

from ..dependency.db import get_db
from src.entities import User
from sqlalchemy.orm import Session

from .model import (
    UserResponse,
    UserRegister, 
    UserLogin,
    Token,
)
from . import service
from ..dependency.authentication import get_current_user



router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)


@router.post("/register", response_model=UserResponse)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    return service.register_user(user, db)


@router.post("/login", response_model=Token, deprecated=True)
def login_user(user: Annotated[UserLogin, Form()], db: Session = Depends(get_db)) -> Token:
    return service.login_user(user, db)


@router.get("/profile", response_model=UserResponse)
def current_user_profile(user: Annotated[User, Depends(get_current_user)]):
    print("--------Inside current user main------------")
    return service.read_user_me(user)