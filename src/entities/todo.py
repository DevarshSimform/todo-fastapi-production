from enum import Enum as PyEnum
from ..database import Base
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    Date,
    Boolean,
    Enum as SQLEnum
)

from zoneinfo import ZoneInfo
from datetime import datetime


class PriorityEnum(str, PyEnum):
    high = "high"
    medium = "medium"
    low = "low"


class TaskStatusEnum(str, PyEnum):
    pending = "pending"
    success = "success"
    failed = "failed"


def now_in_timezone():
    return datetime.now(ZoneInfo("Asia/Kolkata"))

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(String(500))
    priority = Column(SQLEnum(PriorityEnum, name="priority_enum"), nullable=False, default=PriorityEnum.medium)
    due_date = Column(Date)
    status = Column(SQLEnum(TaskStatusEnum, name="status_enum"), nullable=False, default=TaskStatusEnum.pending)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=now_in_timezone)
    updated_at = Column(DateTime(timezone=True), default=now_in_timezone, onupdate=now_in_timezone)