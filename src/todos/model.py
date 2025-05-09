from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime, date
from enum import Enum
from ..entities import PriorityEnum, TaskStatusEnum



class TaskIn(BaseModel):
    title: str
    description: str | None = None
    priority: PriorityEnum | None = PriorityEnum.medium
    due_date: date | None = None

    class Config:
        # This ensures that Pydantic serializes the date as "YYYY-MM-DD" (without time)
        json_encoders = {
            date: lambda value: value.strftime('%Y-%m-%d')  # Format date as "YYYY-MM-DD"
        }

    @field_validator('due_date')
    def check_due_date(cls, value):
        if value and value < date.today():
            raise ValueError('Due date must be in the future')
        return value
    
    @model_validator(mode="after")
    def change_case(self):
        self.title = self.title.lower()
        self.description = self.description.lower()
        return self


class TaskResponse(BaseModel):
    title: str
    description: str | None = None
    priority: PriorityEnum
    due_date: date | None
    status: TaskStatusEnum
    created_at : datetime
    updated_at: datetime

    class Config:
        json_encoders = {
            date: lambda value: value.strftime('%Y-%m-%d'),
            datetime: lambda value: value.strftime("%Y-%m-%d %H:%M:%S")
        }

class TaskRetrieveResponse(TaskResponse):
    id: int
    is_completed: bool

class TaskComplete(BaseModel):
    is_completed: bool