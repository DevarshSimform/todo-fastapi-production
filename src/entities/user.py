from sqlalchemy import (Column, String, Integer, DateTime)
from ..database import Base

from zoneinfo import ZoneInfo
from datetime import datetime



def now_in_timezone():
    return datetime.now(ZoneInfo("Asia/Kolkata"))


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    username = Column(String, nullable=False)
    firstname = Column(String, nullable=False)
    lastname = Column(String, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True),default=now_in_timezone)