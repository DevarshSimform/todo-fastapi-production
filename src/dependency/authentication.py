import os
import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.auth.model import Token
from ..entities import User
from .db import get_db
from ..exception import CredentialException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")


def get_current_user(
    token: Annotated[Token, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    print("----------Inside dependency------------")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise CredentialException()
    except InvalidTokenError:
        raise CredentialException()

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise CredentialException()
    return user