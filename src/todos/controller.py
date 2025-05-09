from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    Body,
)
from ..dependency.db import get_db
from src.entities import User
from sqlalchemy.orm import Session
from . import (
    TaskIn,
    TaskResponse, 
    TaskComplete,
    TaskRetrieveResponse,
    service
)
from ..dependency.authentication import get_current_user




router = APIRouter(
    prefix="/todos", 
    tags=["Todos"]
)


@router.get("/", response_model=list[TaskResponse])
def get_todos(user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return service.get_todos(user, db)


@router.post("/", response_model=TaskResponse)
def create_todo(task: TaskIn, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return service.create_todo(task, user, db)


@router.get("/{task_id}", response_model=TaskRetrieveResponse)
def get_todo(task_id: int, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return service.get_todo_by_id(task_id, user, db)


@router.put("/{task_id}", response_model=TaskResponse)
def update_todo(task_id: int, task: Annotated[TaskIn, Body()], user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return service.update_todo(task_id, task, user, db)


@router.patch("/{task_id}", response_model=TaskResponse)
def change_todo_status(task_id: int, task: TaskComplete, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return service.change_todo_status(task_id, task, user, db)


@router.delete("/{task_id}")
def delete_todo(task_id: int, user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return service.delete_todo(task_id, user, db)