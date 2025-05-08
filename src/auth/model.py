from pydantic import BaseModel, EmailStr, Field
from datetime import datetime




class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    created_at: datetime


class UserRegister(BaseModel):
    email: EmailStr
    username: str
    firstname: str
    lastname: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr = Field(alias="username")
    password: str
    # username: EmailStr | None = None


class Token(BaseModel):
    access_token: str
    token_type: str
